from enum import Enum


class RoleType(Enum):
    ADMIN = 1
    VIEWER = 2
    DISABLE = 3


class PaymentStatus(Enum):
    PAID = 1
    UNPAID = 2
    ERROR = 3
