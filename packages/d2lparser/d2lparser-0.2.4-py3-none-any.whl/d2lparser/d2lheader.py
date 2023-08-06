

from enum import Enum

#############
#   ENUMS   #
#############


class D2LError(Enum):
    SUCCESS = 0b00000000
    ERROR = 0b10000000


class D2LRequestResponse(Enum):
    REQUEST = 0b00000000
    RESPONSE = 0b10000000

###############
#   CLASSES   #
###############


class D2LHeaderData(dict):
    BLOCK_SIZE = 16
    HEADER_SIZE = 38

    PROTOCOL_VERSION = 3
    KEY = 1
