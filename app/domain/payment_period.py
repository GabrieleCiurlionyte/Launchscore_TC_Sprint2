from enum import Enum

class PaymentPeriod(str, Enum):
    MONTHLY = "Monthly"
    YEARLY = "Yearly"
    ONE_TIME = "One-time"
    FREE = "Free"
    NOT_SURE = "Not sure"