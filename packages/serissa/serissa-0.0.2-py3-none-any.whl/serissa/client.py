from __future__ import annotations
import logging
import asyncio
import base64
import itertools
from typing import List, Set, Dict, Tuple, Optional, Union

from .log import initLogger
from .message import Message
from .handler import Handler


class Client:
    server: str
    port: int = 6697
    ssl: bool = True

    nickname: Optional[str] = None

    reader: Optional[asyncio.StreamReader]
    writer: Optional[asyncio.StreamWriter]
    logger: logging.Logger

    _watcher: Optional[asyncio.Task] = None
    _internal_tasks: List[asyncio.Task]

    channels: Set[str] = set()

    response_handlers: Dict[str, Handler]

    available_cap: List[str]
    requested_cap: List[str]

    is_logined: bool = False

    CONST_CAP: List[str] = ['draft/multiline']
    _newlabel = itertools.count(start=1)

    def __init__(self,
                 server: str,
                 port: int = 6697,
                 ssl: bool = True,
                 log_level: int = logging.WARNING,
                 log_output: Union[str, int] = 1,
                 ):
        self.server = server
        self.port = port
        self.ssl = ssl

        # logger can be replaced if you need create multiple bots in one project
        # else all bots' logger are the same, which got by __name__
        self.logger = initLogger(log_level, log_output)

        self.reader, self.writer = None, None

        self.response_handlers = dict()
        self.available_cap = list()
        self.requested_cap = list()

        self._internal_tasks = list()

    def new_label(self) -> str:
        return str(next(self._newlabel))

    @property
    def is_open(self):
        return (self.reader is not None
                and not self.reader.at_eof()
                and self.writer is not None)

    async def connect(self) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        if not self.is_open:
            self.logger.info(f'connect to {self.server}:{self.port}')
            self.reader, self.writer = await asyncio.open_connection(self.server, self.port, ssl=self.ssl)

        return self.reader, self.writer  # type: ignore

    async def load_available_capabilities(self, timeout: int = 30) -> List[str]:
        assert self.nickname is not None

        async def cap_ls_handler(cli: Client, msg: Message):
            self.available_cap += msg.params[-1].split()
            if msg.params[-2] != '*' and msg.handler is not None:
                self.logger.info(f'available capabilities: [{" ".join(self.available_cap)}]')
                msg.handler.cancle()
        handler = Handler(
            body=cap_ls_handler,
            # response: CAP <nick> LS [*] :<cap>*
            # response is not end if msg has optional "*"
            match=lambda msg: msg.command.upper() == 'CAP' and len(msg.params) > 2 and msg.params[1].upper() == 'LS',
            timeout=timeout,
        )
        self.regist_handler(handler)
        await self.send(Message('CAP', ['LS', '302']))
        await self.send(Message('NICK', [self.nickname]))
        await self.send(Message('USER', [self.nickname, '*', '0', self.nickname]))

        # capabilities loaded or timeout
        await handler.wait_completed()
        return self.available_cap

    async def _reqCap(self, *args: str) -> bool:
        if self.is_logined:
            self.logger.error("can not request capability after login")
            return False
        if len(self.available_cap) == 0:
            await self.load_available_capabilities()

        available_cap_key = [cap.split('=', 1)[0] for cap in self.available_cap]
        for cap in args:
            if cap not in available_cap_key:
                self.logger.warning(f'capability {cap} may unavailable')

        for cap in self.CONST_CAP:
            if cap in available_cap_key:
                args += (cap,)

        async def cap_req_handler(cli: Client, msg: Message):
            # TODO: cap start with '-' means disable capability
            self.requested_cap += msg.params[-1].split()
            self.logger.info(f'requested capability: {" ".join(self.requested_cap)}')

        handler = Handler(
            body=cap_req_handler,
            match=lambda msg: msg.command.upper() == 'CAP' and len(msg.params) > 2 and msg.params[1].upper() == 'ACK',
            times=1,
        )
        self.regist_handler(handler)

        await self.send(Message('CAP', ['REQ', ' '.join(args)]))
        try:
            await handler.wait_completed()
        except TimeoutError:
            return False
        return True

    async def login(self,
                    nickname: str,
                    password: Optional[str] = None,
                    sasl: bool = True,
                    response_invite: bool = True,
                    capabilities: List[str] = []):
        self.nickname = nickname

        self.logger.info(f"bot {nickname} connecting")

        if sasl and 'sasl' not in capabilities:
            capabilities.append('sasl')
        if response_invite:
            capabilities.append('invite-notify')

            async def invite_handler(cli, msg: Message):
                if len(msg.params) > 1 and msg.params[0] == cli.nickname:
                    await cli.send(Message("JOIN", msg.params[1:]))

            self.regist_handler(Handler(
                body=invite_handler,
                match=lambda msg: msg.command.upper() == 'INVITE',
                timeout=None,
            ))

        await self._reqCap(*capabilities)
        if password:
            if not sasl:
                await self.send(Message('PASS', [password]))
            else:
                # TODO:
                # 1. Check sasl PLAIN is available cap
                # 2. cap-notify
                passwd = base64.b64encode(
                    b'\x00' + self.nickname.encode() + b'\x00' + password.encode()
                ).decode()
                await self.send(Message('AUTHENTICATE', ['PLAIN']))
                await self.send(Message('AUTHENTICATE', [passwd]))

        await self.send(Message('CAP', ['END']))
        await self.send(Message('MODE', [self.nickname, '+B']))

        # TODO: set is_logined in handler
        self.logger.info(f'bot {nickname} logined')
        self.is_logined = True

    async def _handle_msg(self, msg: Message):
        self.response_handlers = {k: v for k, v in self.response_handlers.items() if not v.fut.done()}
        handlers = [handler for handler in self.response_handlers.values() if handler.match(msg)]
        try:
            await asyncio.gather(*[handler(self, msg) for handler in handlers])  # type: ignore
        except TimeoutError:
            self.logger.warning(f"message handle timeout {msg}")
        except asyncio.CancelledError:
            self.logger.warning('canceling handling handler')
            for handler in handlers:
                handler.cancle()

    async def _watch(self):
        while self.is_open:
            try:
                raw = (await self.reader.readline()).decode('utf-8').strip()
                self.logger.debug(f'receive: {raw}')
                msg = Message.decode(raw)
                if msg is not None:
                    # TODO: append to handler quene
                    asyncio.create_task(self._handle_msg(msg))
            except asyncio.CancelledError:
                self.logger.info(f'client {self.nickname} task killed')
                return

    async def start(self, ):
        await self.connect()

        async def ping():
            try:
                while True:
                    await asyncio.sleep(60)
                    await self.send(Message('PING', ['serissa']))
            except asyncio.CancelledError:
                return
        self._internal_tasks.append(asyncio.create_task(ping()))

        async def join_handler(cli, msg: Message):
            new_chans = set(msg.params[0].split(','))
            cli.logger.info(f'channel {", ".join(new_chans)} joined')
            cli.channels |= new_chans
        self.regist_handler(Handler(
            body=join_handler,
            match=lambda msg: msg.command.upper() == 'JOIN',
            timeout=None,
        ))

        async def pong_handler(cli, msg: Message):
            assert self.nickname is not None

            await cli.send(Message("PONG", [self.nickname, *msg.params]))
        self.regist_handler(Handler(
            body=pong_handler,
            match=lambda msg: msg.command.upper() == 'PING',
            timeout=None,
        ))

        self._watcher = asyncio.create_task(self._watch())

    async def send(self, msg: Message):
        _, writer = await self.connect()
        self.logger.debug(f'send: {msg}')
        if msg.command.upper() == 'BATCH':
            assert len(msg.params) > 0 and msg.params[0].startswith('+'), "invalid BATCH parameters"
            writer.write(msg.encode())
            sub_msg = msg.batch()
            if sub_msg is not None:
                for m in sub_msg:
                    writer.write(m.encode())
            writer.write(Message('BATCH', [f'-{msg.params[0][1:]}']).encode())
        else:
            writer.write(msg.encode())
        await writer.drain()

    async def wait(self):
        if self._watcher is not None:
            await self._watcher
        else:
            self.logger.error('no awaitable task')
        self.logger.warning("client closed")

    async def quit(self, msg: str = ''):
        self.logger.info('stoping backgrond task')
        if self._watcher is not None:
            self._watcher.cancel()
            await self._watcher

        self.logger.info('canceling handler')
        for handler in self.response_handlers:
            handler.cancle(asyncio.CancelledError)

        self.logger.info('send quit message')
        await self.send(Message('QUIT', [msg]))
        if self.writer is not None:
            self.writer.close()

        self.reader = self.writer = None

        self.logger.info('irc connection closed')

    def regist_handler(self, handler: Handler, name: Optional[str] = None) -> str:
        if name is None:
            name = str(id(handler))
        self.response_handlers[name] = handler
        return name

    def unregist_handler(self, name: str):
        self.response_handlers.pop(name)
