from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = [
    "TRUE_FALSE_CHOICES",
    "FlatOrPercentChoices",
    "TimeFrequencyChoices",
    "PersonBloodChoices",
    "PersonEducationLevelChoices",
]

TRUE_FALSE_CHOICES = [
    ("", "---"),
    (True, "True"),
    (False, "False"),
]


# Generic
class FlatOrPercentChoices(models.TextChoices):
    """Flat or percent choices for rate calculations.

    Attributes:
        DEFAULT (str): Empty string representing no selection
        FLAT (str): Flat rate option
        PERCENT (str): Percentage rate option
    """

    DEFAULT = "", _("---")
    FLAT = "FLAT", _("Flat")
    PERCENT = "PERCENT", _("Percent")


class TimeFrequencyChoices(models.TextChoices):
    """Time frequency options for recurring events.

    Attributes:
        DEFAULT (str): Empty string representing no selection
        HOURLY (str): Hourly frequency
        DAILY (str): Daily frequency
        WEEKLY (str): Weekly frequency
        MONTHLY (str): Monthly frequency
        QUARTERLY (str): Quarterly frequency
        ANNUALLY (str): Annually frequency
    """

    DEFAULT = "", _("---")
    HOURLY = "HOURLY", _("Hourly")
    DAILY = "DAILY", _("Daily")
    WEEKLY = "WEEKLY", _("Weekly")
    MONTHLY = "MONTHLY", _("Monthly")
    QUARTERLY = "QUARTERLY", _("Quarterly")
    ANNUALLY = "ANNUALLY", _("Annually")


# Person
class PersonBloodChoices(models.TextChoices):
    """Blood type classification options.

    Attributes:
        DEFAULT (str): Empty string representing no selection
        A (str): Blood type A
        B (str): Blood type B
        AB (str): Blood type AB
        O (str): Blood type O
        OTHERS (str): Other blood types
    """

    DEFAULT = "", _("---")
    A = "A", _("A")
    B = "B", _("B")
    AB = "AB", _("AB")
    O = "O", _("O")
    OTHERS = "OTHERS", _("Others")


class PersonEducationLevelChoices(models.TextChoices):
    """Academic achievement level classifications.

    Represents different levels of academic achievement from high school through doctoral degrees.

    References:
        https://study.com/different_degrees.html

    Attributes:
        DEFAULT (str): Empty string representing no selection
        HIGH_SCHOOL (str): High School diploma
        ASSOCIATE (str): Associate degree
        BACHELOR (str): Bachelor's degree
        MASTER (str): Master's degree
        DOCTORAL (str): Doctoral degree
        OTHERS (str): Other education levels
    """

    DEFAULT = "", _("---")
    HIGH_SCHOOL = "HIGH_SCHOOL", _("High School")
    ASSOCIATE = "ASSOCIATE", _("Associate Degree")
    BACHELOR = "BACHELOR", _("Bachelor's Degree")
    MASTER = "MASTER", _("Master's Degree")
    DOCTORAL = "DOCTORAL", _("Doctoral Degree")
    OTHERS = "OTHERS", _("Others")


class PersonEyeColorChoices(models.TextChoices):
    """Eye color classification options.

    References:
        https://en.wikipedia.org/wiki/Eye_color#Eye_color_chart_(Martin_scale)

    Attributes:
        DEFAULT (str): Empty string representing no selection
        AMBER (str): Amber colored eyes
        BLUE (str): Blue colored eyes
        BROWN (str): Brown colored eyes
        GREEN (str): Green colored eyes
        GREY (str): Grey colored eyes
        HAZEL (str): Hazel colored eyes
        RED (str): Red colored eyes
        OTHERS (str): Other eye colors
    """

    DEFAULT = "", _("---")
    AMBER = "AMBER", _("Amber")
    BLUE = "BLUE", _("Blue")
    BROWN = "BROWN", _("Brown")
    GREEN = "GREEN", _("Green")
    GREY = "GREY", _("Grey")
    HAZEL = "HAZEL", _("Hazel")
    RED = "RED", _("Red")
    OTHERS = "OTHERS", _("Others")


class PersonGenderChoices(models.TextChoices):
    """Gender classification options.

    Attributes:
        DEFAULT (str): Empty string representing no selection
        FEMALE (str): Female gender
        MALE (str): Male gender
        OTHERS (str): Other gender identifications
    """

    DEFAULT = "", _("---")
    FEMALE = "FEMALE", _("Female")
    MALE = "MALE", _("Male")
    OTHERS = "OTHERS", _("Others")


class PersonRaceChoices(models.TextChoices):
    """Racial and ethnic classification options.

    References:
        https://grants.nih.gov/grants/guide/notice-files/not-od-15-089.html

    Attributes:
        DEFAULT (str): Empty string representing no selection
        ASIAN (str): Asian racial identification
        BLACK (str): Black or African American racial identification
        HISPANIC (str): Hispanic or Latino ethnic identification
        INDIAN (str): American Indian or Alaska Native racial identification
        ISLANDER (str): Native Hawaiian or Other Pacific Islander racial identification
        WHITE (str): White racial identification
        OTHERS (str): Other racial or ethnic identifications
    """

    DEFAULT = "", _("---")
    ASIAN = "ASIAN", _("Asian")
    BLACK = "BLACK", _("Black Or African American")
    HISPANIC = "HISPANIC", _("Hispanic Or Latino")
    INDIAN = "INDIAN", _("American Indian Or Alaska Native")
    ISLANDER = "ISLANDER", _("Native Hawaiian Or Other Pacific Islander")
    WHITE = "WHITE", _("White")
    OTHERS = "OTHERS", _("Others")


# Payment / Transaction
class PaymentMethodTypeChoices(models.TextChoices):
    """Available payment method options.

    Attributes:
        DEFAULT (str): Empty string representing no selection
        CREDIT_CARD (str): Credit card payment method
        DEBIT_CARD (str): Debit card payment method
        ELECTRONIC_BANK_TRANSFER (str): Bank transfer payment method
        PAYPAL (str): PayPal payment method
        APPLE_PAY (str): Apple Pay payment method
        GOOGLE_PAY (str): Google Pay payment method
    """

    DEFAULT = "", _("---")
    CREDIT_CARD = "CREDIT_CARD", _("Credit Card")
    DEBIT_CARD = "DEBIT_CARD", _("Debit Card")
    ELECTRONIC_BANK_TRANSFER = "BANK_TRANSFER", _("Bank Transfer")
    PAYPAL = "PAYPAL", _("Paypal")
    APPLE_PAY = "APPLE_PAY", _("Apple Pay")
    GOOGLE_PAY = "GOOGLE_PAY", _("Google Pay")


class TransactionGatewayChoices(models.TextChoices):
    """Supported payment processing gateways.

    Attributes:
        DEFAULT (str): Empty string representing no selection
        ADYEN (str): Adyen payment gateway
        ALIPAY (str): Alipay payment gateway
        AMAZON (str): Amazon payment gateway
        AUTHORIZE (str): Authorize.net payment gateway
        BRAINTREE (str): Braintree payment gateway
        CYBERSOURCE (str): Cybersource payment gateway
        INGENICO (str): Ingenico payment gateway
        PAYPAL (str): PayPal payment gateway
        SQUARE (str): Square payment gateway
        STRIPE (str): Stripe payment gateway
        WEPAY (str): WePay payment gateway
        WORLDPAY (str): Worldpay payment gateway
    """

    DEFAULT = "", _("---")
    ADYEN = "ADYEN", _("Adyen")
    ALIPAY = "ALIPAY", _("Alipay")
    AMAZON = "AMAZON", _("Amazon")
    AUTHORIZE = "AUTHORIZE", _("Authorize")
    BRAINTREE = "BRAINTREE", _("Braintree")
    CYBERSOURCE = "CYBERSOURCE", _("Cybersource")
    INGENICO = "INGENICO", _("Ingenico")
    PAYPAL = "PAYPAL", _("Paypal")
    SQUARE = "SQUARE", _("Square")
    STRIPE = "STRIPE", _("Stripe")
    WEPAY = "WEPAY", _("Wepay")
    WORLDPAY = "WORLDPAY", _("Worldpay")


class TransactionStateChoices(models.TextChoices):
    """Transaction processing state options.

    References:
        https://stripe.com/docs/payments/intents#intent-statuses

    Attributes:
        DEFAULT (str): Empty string representing no selection
        REQUIRES_PAYMENT_METHOD (str): Payment method needs to be provided
        REQUIRES_CONFIRMATION (str): Transaction requires confirmation
        REQUIRES_ACTION (str): Additional action required
        PROCESSING (str): Transaction is being processed
        CANCEL (str): Transaction has been cancelled
        SUCCESS (str): Transaction completed successfully
    """

    DEFAULT = "", _("---")
    REQUIRES_PAYMENT_METHOD = "REQUIRES_PAYMENT_METHOD", _("Requires Payment Method")
    REQUIRES_CONFIRMATION = "REQUIRES_CONFIRMATION", _("Requires Confirmation")
    REQUIRES_ACTION = "REQUIRES_ACTION", _("Requires Action")
    PROCESSING = "PROCESSING", _("Processing")
    CANCEL = "CANCEL", _("Cancel")
    SUCCESS = "SUCCESS", _("Success")


class TransactionTypeChoices(models.TextChoices):
    """Transaction classification options.

    Attributes:
        DEFAULT (str): Empty string representing no selection
        PAYMENT (str): Standard payment transaction
        REFUND (str): Refund transaction
        ADJUSTMENT (str): Adjustment transaction
        COUPON (str): Coupon application transaction
        PRORATION (str): Proration transaction
    """

    DEFAULT = "", _("---")
    PAYMENT = "PAYMENT", _("Payment")
    REFUND = "REFUND", _("Refund")
    ADJUSTMENT = "ADJUSTMENT", _("Adjustment")
    COUPON = "COUPON", _("Coupon")
    PRORATION = "PRORATION", _("Proration")


class TransactionEventTypeChoices(models.TextChoices):
    """Transaction lifecycle event types.

    Attributes:
        DEFAULT (str): Empty string representing no selection
        CREATED (str): Transaction has been created
        AUTHORIZED (str): Transaction has been authorized
        CAPTURED (str): Transaction has been captured
        REFUNDED (str): Transaction has been refunded
        FAILED (str): Transaction has failed
    """

    DEFAULT = "", _("---")
    CREATED = "CREATED", _("Created")
    AUTHORIZED = "AUTHORIZED", _("Authorized")
    CAPTURED = "CAPTURED", _("Captured")
    REFUNDED = "REFUNDED", _("Refunded")
    FAILED = "FAILED", _("Failed")
