from enum import Enum

from models import UserType


class APIScope(str, Enum):
    ALL = "all"  # access to all endpoints
    CREATE_USER = "create_user"
    ORGANIZATION_READ = "organization:read"
    ORGANIZATION_WRITE = "organization:write"


DEFAULT_USER_SCOPES: dict[UserType, set[APIScope]] = {
    UserType.PLIXA_SUPERUSER: {APIScope.ALL},
    UserType.PLIXA_STAFF: {APIScope.ORGANIZATION_READ, APIScope.ORGANIZATION_WRITE},
    UserType.PLATFORM_USER: {APIScope.ORGANIZATION_READ, APIScope.ORGANIZATION_WRITE},
}
