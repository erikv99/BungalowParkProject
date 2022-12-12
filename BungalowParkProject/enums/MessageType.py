from enum import Enum

class MessageType(Enum):
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    INFO = "INFO"
    NONE = "NONE"