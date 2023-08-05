from abc import ABC, abstractmethod
from loguru import logger


class BCInfo(object):

    def __init__(self, pan: str = '', track2: str = '', ic55: str = ''):
        super(BCInfo, self).__init__()
        self.pan = pan  # 主账号
        self.track2 = track2  # 二磙
        self.ic55 = ic55  # 55 域

    def __repr__(self) -> str:
        return 'pan: %s, track2: %s, ic55: %s' % (self.pan, self.track2, self.ic55)


class BCReader(ABC):

    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def read_info(self, amount: int) -> BCInfo:
        pass

    def __enter__(self):
        self.open()

    def __exit__(self):
        try:
            self.close()
        except Exception as e:
            logger.debug(e)
