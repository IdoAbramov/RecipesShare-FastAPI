from enum import Enum

class RoleID(Enum):
    ADMIN = 1
    REGULAR = 2

class RoleName(Enum):
    ADMIN = "admin"
    REGULAR = "regular user"

MAX_LOGIN_ATTEMPTS = 5

