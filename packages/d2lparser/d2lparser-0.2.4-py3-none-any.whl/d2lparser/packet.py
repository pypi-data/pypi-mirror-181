from enum import Enum
from typing import Any


class PacketType(Enum):
    GET_FIRMWARE = 1
    PUSH_JSON = 3
    GET_HORLOGE = 5


class D2LPacket():
    def __init__(self, header: dict, payload: dict, unencrypted: bytearray = None) -> None:
        self._header = header
        self._payload = payload
        self._unencrypted = unencrypted

    @property
    def header(self) -> dict:
        return self._header

    @header.setter
    def header(self, header: dict):
        self._header = header

    @property
    def payload(self) -> dict:
        return self._payload

    @payload.setter
    def payload(self, payload: Any):
        self._payload = payload

    @property
    def unencrypted(self) -> bytearray:
        return self._unencrypted

    @property
    def id_d2l(self) -> str:
        return self._header["idD2L"]

    @id_d2l.setter
    def id_d2l(self, id_d2l):
        self._header["idD2L"] = id_d2l

    @property
    def packet_type(self):
        return self._header["typePayload"]

    @id_d2l.setter
    def id_d2l(self, packet_type):
        self._header["typePayload"] = packet_type
