from enum import Enum

class MonetizationModel(str, Enum):
    SUBSCRIPTION = "Subscription"
    FREEMIUM = "Freemium"
    ADS = "Ads"
    ONE_TIME_PURCHASE = "One-time purchase"
    IN_APP_PURCHASES = "In-app purchases"
    MARKETPLACE_FEE = "Marketplace fee"
    NOT_SURE = "Not sure"