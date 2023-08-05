import base64
import requests

from loguru import logger

from .pos import POS, POSAPI
from .bc_reader import BCReader
from .epp import EPP


class CCBPos(POS):

    def __init__(self, bcr: BCReader, epp: EPP, api: POSAPI, device: str, merchant: str) -> None:
        super().__init__(bcr, epp, device, merchant)
        self.api_url = api.url
        self.api_token = api.token
        self.api_pass = api.pwd

    def sign_in(self) -> str:
        r = requests.post(self.api_url,
                          auth=(self.api_token, self.api_pass),
                          data={
                              "tranCode": "0800",
                              "device": self.device,
                              "merchant": self.merchant
                          })

        b62 = base64.decodebytes(r.text.encode()).hex()
        wkey = b62[:32]
        wkeysum = b62[32:40]
        mkey = b62[40:56]
        mkeysum = b62[56+16:80]
        logger.debug('pin key: {}, mac key: {}', wkey, mkey)

        with self.epp as epp_:
            r = epp_.write_pin_key(wkey)
            logger.debug('write_pin_key {}, {}', r, wkeysum)

            if r.lower() != wkeysum:
                raise RuntimeError('Failed to write PIN key')

            r = epp_.write_mac_key(mkey)
            logger.debug('write_mac_key {}, {}', r, mkeysum)
            if r.lower() != mkeysum:
                raise RuntimeError('Failed to write MAC key')

    def sign_out(self) -> None:
        requests.post(self.api_url,
                      auth=(self.api_token, self.api_pass),
                      data={
                          "tranCode": "0820",
                          "device": self.device
                      })

    def pay(self, amount: int) -> dict:
        if amount < 1:
            raise RuntimeError('The amount must be greater than zero')

        bci = None
        with self.bcr as bcr_:
            bci = bcr_.read_info(amount)
            logger.debug("bci: {}", bci)

        if not bci:
            raise RuntimeError('Failed to read card information')

        pin = None
        with self.epp as epp_:
            pin = epp_.read_pin(bci.pan)
            logger.debug('pin: {}', pin)

        if not pin:
            raise RuntimeError('Failed to read PIN')

        r = requests.post(self.api_url,
                          auth=(self.api_token, self.api_pass),
                          data={
                              "tranCode": "02002",
                              'amount': amount,
                              "accountSN": bci.pan,
                              "track2": bci.track2,
                              "device": self.device,
                              "password": pin,
                              "ic55": bci.ic55
                          })
        map = r.json()
        h = base64.decodebytes(map['data'].encode()).hex()
        logger.debug(h)

        mac = None
        with self.epp as epp_:
            mac = epp_.read_mac(h)
            logger.debug('mac: {}', mac)

        if not mac:
            raise RuntimeError('Failed to calculate MAC')

        r = requests.post(self.api_url,
                          auth=(self.api_token, self.api_pass),
                          data={
                              "tranCode": "0000",
                              "id": map['id'],
                              "mac": mac[:16]
                          })
        logger.debug(r.text)
