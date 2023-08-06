from __future__ import annotations

from random import randint
from typing import List, Dict, Union, Optional

# TODO: Batch Queue
batch_queue: Dict[str, Message] = dict()


class Message:
    tags: Dict[str, Union[str, bool]]
    command: str
    params: List[str]

    # only exist when received message from server
    prefix: Optional[str]

    handler: Optional["Handler"] = None  # type: ignore # noqa

    # used for BATCH command
    _messages: List[Message]

    def __init__(self, command: str,
                 params: List[str] = [],
                 tags: Dict[str, Union[str, bool]] = dict(),
                 prefix: Optional[str] = None):  # type: ignore # noqa
        self.command = command
        self.params = params if len(params) != 0 else list()
        self.tags = tags if len(tags) != 0 else dict()
        self.prefix = prefix
        self._messages = list()

        self.sender = None

    def __repr__(self) -> str:
        return '<' + self.encode().strip().decode() + '>'

    @property
    def label(self) -> Union[str, bool, None]:
        return self.tags.get('label')

    @label.setter
    def label(self, value: Union[str, bool]):
        self.tags['label'] = value

    @property
    def name(self) -> Optional[str]:
        if self.prefix is None:
            return None

        prefix = self.prefix[1:] if self.prefix.startswith(':') else self.prefix
        return prefix.split('!')[0]

    @property
    def user(self) -> Optional[str]:
        if self.prefix is None:
            return None
        prefix = self.prefix[1:] if self.prefix.startswith(':') else self.prefix
        parts = prefix.split('!')
        if len(parts) > 1:
            return parts[1].split('@')[0]
        return None

    @property
    def host(self) -> Optional[str]:
        if self.prefix is None:
            return None
        prefix = self.prefix[1:] if self.prefix.startswith(':') else self.prefix
        parts = prefix.split('!')
        if len(parts) > 1:
            parts = parts[1].split('@')
            if len(parts) > 1:
                return parts[1]
        return None

    def encode(self) -> bytes :
        msg_tags = ''
        for tag_k in self.tags:
            if isinstance(self.tags[tag_k], str):
                msg_tags += f';{tag_k}={self.tags[tag_k]}'
            elif isinstance(self.tags[tag_k], bool):
                msg_tags = msg_tags + f";+{tag_k}" if self.tags[tag_k] else msg_tags
        if msg_tags != '':
            msg_tags = '@' + msg_tags.strip(';')
        if ' ' in self.params[-1]:
            params_str = ' '.join(self.params[:-1]) + f' :{self.params[-1]}'
        else:
            params_str = ' '.join(self.params)
        return f"{msg_tags} {self.command} {params_str}\r\n".encode()

    def batch(self) -> Optional[List[Message]]:
        if self.command.upper() == 'BATCH':
            return self._messages
        else:
            return None

    @classmethod
    def decode(cls, msg: str) -> Optional[Message]:
        # message is optional because of BATCH command
        tags: Dict[str, Union[str, bool]] = dict()
        prefix: Optional[str] = None
        params: Optional[List[str]] = None
        command: str

        if msg.startswith('@'):
            tags = dict()
            tag_str, msg = msg.split(' ', 1)
            raw_tags = tag_str[1:].split(';')
            for tag in raw_tags:
                if '=' in tag:
                    k, v = tag.split('=', 2)
                    tags[k] = v
                else:
                    tags[tag] = True

        if msg.startswith(':'):
            prefix, msg = msg.split(' ', 1)

        params = msg.split(':', 1)
        if len(params) == 2:
            trailing = params[1]
            params = params[0].split()
            params.append(trailing)
        else:
            params = params[0].split()

        command = params.pop(0)

        message = cls(command=command,
                      params=params,
                      tags=tags,
                      prefix=prefix)

        if command == 'BATCH' or tags.get('batch') is not None:
            return cls._batch_update(message)

        return message

    @classmethod
    def _batch_update(cls, msg: Message) -> Optional[Message]:
        # if is a batch command
        if msg.command.upper() == 'BATCH':
            assert len(msg.params) > 0 and (msg.params[0][0] == '-' or msg.params[0][0] == '+')
            batch_id = msg.params[0][1:]
            if msg.params[0][0] == '+':
                # create new batch queue
                batch_queue[batch_id] = msg
                msg = None
            elif msg.params[0][0] == '-':
                # a batch queue end
                msg = batch_queue.pop(batch_id)

        if msg is not None and 'batch' in msg.tags:
            # is a subcommand of a batch
            batch_id = str(msg.tags.get('batch'))
            assert batch_id in batch_queue, f"can not find batch {batch_id}"
            batch_queue[batch_id]._update(msg)
            return None
        else:
            return msg

    def _update(self, msg: Message):
        self._messages.append(msg)


def newPrivMsg(target: str, msg: str, label: Optional[str] = None) -> Message:
    # remove linebreak at start and end
    msg = msg.strip('\n')

    if '\n' not in msg:
        message = Message("PRIVMSG", [target, msg])
        if label is not None:
            message.label = label
        return message
    else:
        # TODO: generate unique lable
        batch_label = str(randint(0, 1000))
        message = Message("BATCH", [f'+{batch_label}', 'draft/multiline', target])
        for line in msg.split('\n'):
            message._messages.append(Message('PRIVMSG', [target, line], tags={'batch': batch_label}))
        return message


def newNotice(target: str, notice: str, label: Optional[str] = None) -> Message:
    message = Message("NOTICE", [target, notice])
    if label is not None:
        message.label = label
    return message
