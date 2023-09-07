from enum import Enum

from models import UserType


class APIScope(str, Enum):
    ALL = "all"  # access to all endpoints


DEFAULT_USER_SCOPES: dict[UserType, set[set]] = {
    UserType.PLIXA_SUPERUSER: {APIScope.ALL},
    UserType.PLIXA_STAFF: set(),
    UserType.PLATFORM_USER: set(),
}
