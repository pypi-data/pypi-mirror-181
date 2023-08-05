from abc import ABC, abstractmethod
from loguru import logger


class EPP(ABC):

    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def clear_keys(self) -> None:
        pass

    @abstractmethod
    def write_device_key(self, hex_data: str) -> str:
        pass

    @abstractmethod
    def write_master_key(self, hex_data: str) -> str:
        pass

    @abstractmethod
    def write_pin_key(self, hex_data: str) -> str:
        pass

    @abstractmethod
    def write_mac_key(self, hex_data: str) -> str:
        pass

    @abstractmethod
    def read_pin(self, card_no: str, timeout: int = 60) -> str:
        pass

    @abstractmethod
    def on_key_press(self, cnt: int = 0) -> None:
        pass

    @abstractmethod
    def read_mac(self, hex_data: str) -> str:
        pass

    def __enter__(self):
        self.open()

    def __exit__(self):
        try:
            self.close()
        except Exception as e:
            logger.debug(e)
