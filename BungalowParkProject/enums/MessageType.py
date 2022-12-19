from enum import Enum

class MessageType(Enum):
    WARNING = "alert-warning"
    ERROR = "alert-danger"
    SUCCESS = "alert-success"
    INFO = "alert-info"
    NONE = ""