from enum import Enum

class PermissionUser(Enum):
    AUTHORIZED_USER = "AUTHORIZED_USER"
    EVERYONE = "EVERYONE"
    ADMIN = "ADMIN"