import sys
import logging
from typing import Union


def initLogger(level: int = logging.WARNING, output: Union[int, str] = 1, name: str = __name__) -> logging.Logger:
    logger: logging.Logger = logging.getLogger(__name__)

    ch: Union[logging.FileHandler, logging.StreamHandler]
    if isinstance(output, int):
        if output == 1 :
            ch = logging.StreamHandler(sys.stdout)
        elif output == 2:
            ch = logging.StreamHandler(sys.stderr)
        else:
            assert False, f"invalid logger output stream: {output}"
    elif isinstance(output, str):
        ch = logging.FileHandler(output)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(level)
    return logger
