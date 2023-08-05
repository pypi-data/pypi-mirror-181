from abc import ABC, abstractmethod
from loguru import logger

from .bc_reader import BCReader
from .epp import EPP


class POSAPI(object):

    # http://1.192.147.32:8889/pos-proxy
    def __init__(self, url: str, token: str, pwd: str):
        super(POSAPI, self).__init__()
        self.url = url
        self.token = token
        self.pwd = pwd


class POS(ABC):

    _batch = None

    def __init__(self, bcr: BCReader, epp: EPP, device: str, merchant: str) -> None:
        super().__init__()
        self.bcr = bcr
        self.epp = epp
        self.device = device
        self.merchant = merchant

    @abstractmethod
    def sign_in(self) -> str:
        pass

    @abstractmethod
    def sign_out(self) -> None:
        pass

    @abstractmethod
    def pay(self, amount: int) -> dict:
        pass

    def __enter__(self):
        if POS._batch:
            return

        POS._batch = self.sign_in

    def __exit__(self):
        if not POS._batch:
            return

        try:
            self.sign_out()
        except Exception as e:
            logger.debug(e)

        POS._batch = None
