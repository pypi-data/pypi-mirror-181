from __future__ import annotations

import asyncio
from typing import Union, Awaitable, Callable
from .message import Message


class Handler:
    # Because of using asyncio.Future, Handler need be created in envent loop
    # times handler can be triggered, minus for unlimited
    times: int = -1

    # wait timeout, minus for unlimited
    time_out: Union[int, None] = None
    match: Callable[[Message], bool]
    body: Callable[[Client, Message], Awaitable[None]]  # type: ignore # noqa

    fut: asyncio.Future

    def __init__(self,
                 body: Callable[[Client, Message], Awaitable[None]],  # type: ignore # noqa
                 match: Callable[[Message], bool],
                 done_callback: Callable[[asyncio.Future], None] = None,  # type: ignore # noqa
                 times: int = -1,
                 timeout: Union[int, None] = 60
                 ):
        self.match = match
        self.body = body
        self.times = times
        self.time_out = timeout

        loop = asyncio.get_running_loop()
        self.fut = loop.create_future()
        if done_callback is not None:
            self.fut.add_done_callback(done_callback)

    async def __call__(self, client: Client, msg: Message):  # type: ignore # noqa
        msg.handler = self
        try:
            await asyncio.wait_for(
                self.body(client, msg),
                timeout=self.time_out,
            )
        except TimeoutError as e:
            client.logger.error(f"handler {handler} for message {msg} timeout")
            self.fut.set_exception(e)
            return
        if self.times > 0:
            self.times -= 1
        if self.times == 0 and not self.fut.done():
            self.fut.set_result(None)

    def cancle(self, exp=None, value=None):
        self.times = 0
        if not self.fut.done():
            if exp is not None:
                if self.times > 0 or self.time_out is not None:
                    # Only raise exception for time limited handler, It's Ok?
                    self.fut.set_exception(exp)
                    return

            self.fut.set_result(value)

    def wait_completed(self) -> asyncio.Future:
        return self.fut


def handler(*args, **kwargs):
    if len(args) == 1 and callable(args[0]):
        # return Handler instance always matched
        return Handler(body=args[0], match=lambda msg: True)

    times = kwargs.pop('times', -1)
    time_out = kwargs.pop('timeout', 60)
    match = kwargs.pop('match')

    def inner_decrotator(body):
        # return Handler instance
        return Handler(body=body,
                       match=match,
                       times=times,
                       timeout=time_out)
    # return Callable decorator
    return inner_decrotator
