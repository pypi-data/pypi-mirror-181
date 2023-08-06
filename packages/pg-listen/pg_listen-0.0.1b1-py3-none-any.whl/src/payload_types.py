import json
from enum import Enum


class PayloadType(str, Enum):
    STRING = 'str'
    INTEGER = 'int'
    DICT = 'dict'


PAYLOAD_ENCODER = {
    str: lambda x: str(x),
    int: lambda x: str(x),
    dict: lambda x: json.dumps(x),
}

PAYLOAD_DECODER = {
    PayloadType.STRING: lambda x: str(x),
    PayloadType.INTEGER: lambda x: int(x),
    PayloadType.DICT: lambda x: json.loads(x),
}
