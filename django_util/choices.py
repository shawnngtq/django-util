"""Django choice field definitions for various data types.

This module provides a collection of choice classes for use with Django models and forms.
Each class inherits from BaseChoices and provides standardized options for different
data types and business domains.

Categories:
    - Generic: Basic choice types like boolean, time frequency, etc.
    - Person: Demographic and personal information choices
    - Payment: Payment and transaction related choices

Example:
    from django_util.choices import TimeFrequencyChoices

    class Subscription(models.Model):
        frequency = models.CharField(
            max_length=50,
            choices=TimeFrequencyChoices.choices,
            default=TimeFrequencyChoices.DEFAULT
        )
"""

from datetime import timedelta
from typing import Dict, List, Optional, Set, Tuple, Union

from django.db import models
from django.utils.translation import gettext_lazy as _

# Choice categories for better organization
GENERIC_CHOICES = [
    "BaseChoices",
    "BooleanChoices",
    "FlatOrPercentChoices",
    "TimeFrequencyChoices",
    "TaskStatusChoices",
    "DataImportStrategy",
]

PERSON_CHOICES = [
    "PersonBloodChoices",
    "PersonEducationLevelChoices",
    "PersonEyeColorChoices",
    "PersonGenderChoices",
    "PersonRaceChoices",
]

PAYMENT_CHOICES = [
    "PaymentMethodTypeChoices",
    "TransactionGatewayChoices",
    "TransactionStateChoices",
    "TransactionTypeChoices",
    "TransactionEventTypeChoices",
]

__all__ = [
    *GENERIC_CHOICES,
    *PERSON_CHOICES,
    *PAYMENT_CHOICES,
]

TRUE_FALSE_CHOICES: List[Tuple[Union[bool, str], str]] = [
    ("", "---"),
    (True, "True"),
    (False, "False"),
]

# Define all metadata outside the classes
PAYMENT_METHODS_REQUIRING_CVV = {"CREDIT_CARD", "DEBIT_CARD"}
PAYMENT_METHODS_REQUIRING_3DS = {"CREDIT_CARD", "DEBIT_CARD"}

EDUCATION_LEVEL_YEARS = {
    "HIGH_SCHOOL": 12,
    "ASSOCIATE": 14,
    "BACHELOR": 16,
    "MASTER": 18,
    "DOCTORAL": 20,
}

TRANSACTION_TYPE_AFFECTS_BALANCE = {"PAYMENT", "REFUND", "ADJUSTMENT"}
TRANSACTION_TYPE_REQUIRES_PROCESSING = {"PAYMENT", "REFUND"}

TRANSACTION_STATE_TRANSITIONS = {
    "": {"REQUIRES_PAYMENT_METHOD"},
    "REQUIRES_PAYMENT_METHOD": {"REQUIRES_CONFIRMATION", "CANCEL"},
    "REQUIRES_CONFIRMATION": {
        "REQUIRES_ACTION",
        "PROCESSING",
        "CANCEL",
    },
    "REQUIRES_ACTION": {"PROCESSING", "CANCEL"},
    "PROCESSING": {"SUCCESS", "CANCEL"},
    "SUCCESS": set(),  # Terminal state
    "CANCEL": set(),  # Terminal state
}


class ChoicesMixin:
    """Mixin providing utility methods for Django choice classes.

    This mixin adds common functionality to choice classes including value validation,
    label retrieval, and choice list manipulation.

    Example:
        class MyChoices(ChoicesMixin, models.TextChoices):
            DEFAULT = "", _("---")
            OPTION_A = "A", _("Option A")
            OPTION_B = "B", _("Option B")

            # Now has access to utility methods:
            MyChoices.is_valid("A")  # Returns True
            MyChoices.get_label("B")  # Returns "Option B"
    """

    @classmethod
    def get_values(cls) -> Set[str]:
        """Return set of all valid choice values.

        Returns:
            Set[str]: A set containing all possible choice values excluding labels.
        """
        return {choice[0] for choice in cls.choices}

    @classmethod
    def get_labels(cls) -> Dict[str, str]:
        """Return mapping of values to their display labels."""
        return {choice[0]: choice[1] for choice in cls.choices}

    @classmethod
    def is_valid(cls, value: str) -> bool:
        """Check if a value is valid for this choice set.

        Args:
            value (str): The choice value to validate.

        Returns:
            bool: True if the value is valid, False otherwise.
        """
        return value in cls.get_values()

    @classmethod
    def get_label(cls, value: str) -> Optional[str]:
        """Get display label for a value."""
        return cls.get_labels().get(value)

    @classmethod
    def exclude_default(cls) -> List[Tuple[str, str]]:
        """Return choices without the DEFAULT option."""
        return [(k, v) for k, v in cls.choices if k != ""]


class FlatOrPercentChoices(ChoicesMixin, models.TextChoices):
    """Choices for flat or percentage values."""

    DEFAULT = "", _("---")
    FLAT = "FLAT", _("Flat")
    PERCENT = "PERCENT", _("Percent")


class TimeFrequencyChoices(ChoicesMixin, models.TextChoices):
    """Choices for time frequency options."""

    DEFAULT = "", _("---")
    DAILY = "DAILY", _("Daily")
    WEEKLY = "WEEKLY", _("Weekly")
    MONTHLY = "MONTHLY", _("Monthly")
    YEARLY = "YEARLY", _("Yearly")


class BooleanChoices(ChoicesMixin, models.TextChoices):
    """Boolean choice options with an empty default."""

    DEFAULT = "", _("---")
    YES = "TRUE", _("Yes")
    NO = "FALSE", _("No")

    @classmethod
    def to_python(cls, value: str) -> Optional[bool]:
        """Convert string value to Python boolean."""
        if value == cls.YES:
            return True
        if value == cls.NO:
            return False
        return None


class TaskStatusChoices(ChoicesMixin, models.TextChoices):
    """Task processing status options.

    Represents different states in a task's lifecycle from creation to completion.

    Attributes:
        PENDING (str): Task is waiting to be processed
        IN_PROGRESS (str): Task is currently being processed
        COMPLETED (str): Task has been successfully completed
        FAILED (str): Task has failed to complete
    """

    DEFAULT = "", _("---")
    PENDING = "PENDING", _("Pending")
    IN_PROGRESS = "IN_PROGRESS", _("In Progress")
    COMPLETED = "COMPLETED", _("Completed")
    FAILED = "FAILED", _("Failed")

    @classmethod
    def is_terminal_state(cls, status: str) -> bool:
        """Check if the status is in a terminal state (completed or failed)."""
        return status in {cls.COMPLETED, cls.FAILED}

    @classmethod
    def is_active_state(cls, status: str) -> bool:
        """Check if the status is in an active state (pending or in progress)."""
        return status in {cls.PENDING, cls.IN_PROGRESS}


class DataImportStrategy(ChoicesMixin, models.TextChoices):
    """Strategy options for handling data imports when records already exist.

    This class defines different approaches for handling duplicate data during import
    operations. Each strategy provides a different behavior for handling conflicts
    with existing records.

    Attributes:
        FAIL (str): Stops the import process if any existing records are found.
            Use when data integrity is critical and duplicates are not allowed.
        REPLACE (str): Overwrites any existing records with new data.
            Use when the imported data should be treated as the source of truth.
        APPEND (str): Adds new records while preserving existing ones.
            Use when maintaining historical data or collecting cumulative data.

    Example:
        class DataImport(models.Model):
            strategy = models.CharField(
                max_length=50,
                choices=DataImportStrategy.choices,
                default=DataImportStrategy.FAIL,
                help_text="Strategy for handling existing records during import"
            )

        # Usage in import logic
        if strategy == DataImportStrategy.FAIL:
            if existing_record:
                raise ImportError("Record already exists")
        elif strategy == DataImportStrategy.REPLACE:
            existing_record.update(new_data)
        elif strategy == DataImportStrategy.APPEND:
            create_new_record(new_data)
    """

    FAIL = "FAIL", _("Fail if exists")
    REPLACE = "REPLACE", _("Replace existing")
    APPEND = "APPEND", _("Append to existing")


# Person
class PersonBloodChoices(ChoicesMixin, models.TextChoices):
    """Blood type classification options.

    Attributes:
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


class PersonEducationLevelChoices(ChoicesMixin, models.TextChoices):
    """Academic achievement level classifications.

    Represents different levels of academic achievement from high school through doctoral degrees.

    References:
        https://study.com/different_degrees.html

    Attributes:
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

    @classmethod
    def get_education_years(cls, level: str) -> int:
        """Return typical years of education for given level."""
        return EDUCATION_LEVEL_YEARS.get(level, 0)


class PersonEyeColorChoices(ChoicesMixin, models.TextChoices):
    """Eye color classification options.

    References:
        https://en.wikipedia.org/wiki/Eye_color#Eye_color_chart_(Martin_scale)

    Attributes:
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


class PersonGenderChoices(ChoicesMixin, models.TextChoices):
    """Gender classification options.

    Attributes:
        FEMALE (str): Female gender
        MALE (str): Male gender
        OTHERS (str): Other gender identifications
    """

    DEFAULT = "", _("---")
    FEMALE = "FEMALE", _("Female")
    MALE = "MALE", _("Male")
    OTHERS = "OTHERS", _("Others")


class PersonRaceChoices(ChoicesMixin, models.TextChoices):
    """Racial and ethnic classification options.

    References:
        https://grants.nih.gov/grants/guide/notice-files/not-od-15-089.html

    Attributes:
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
class PaymentMethodTypeChoices(ChoicesMixin, models.TextChoices):
    """Available payment method options.

    Attributes:
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
    PAYPAL = "PAYPAL", _("PayPal")
    APPLE_PAY = "APPLE_PAY", _("Apple Pay")
    GOOGLE_PAY = "GOOGLE_PAY", _("Google Pay")

    @classmethod
    def requires_cvv(cls, method: str) -> bool:
        """Check if payment method requires CVV."""
        return method in PAYMENT_METHODS_REQUIRING_CVV

    @classmethod
    def requires_3ds(cls, method: str) -> bool:
        """Check if payment method requires 3D Secure."""
        return method in PAYMENT_METHODS_REQUIRING_3DS

    @classmethod
    def card_methods(cls) -> set:
        """Return all card-based payment methods."""
        return {cls.CREDIT_CARD, cls.DEBIT_CARD}

    @classmethod
    def digital_wallet_methods(cls) -> set:
        """Return all digital wallet payment methods."""
        return {cls.PAYPAL, cls.APPLE_PAY, cls.GOOGLE_PAY}


class TransactionGatewayChoices(ChoicesMixin, models.TextChoices):
    """Supported payment processing gateways.

    Attributes:
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


class TransactionStateChoices(ChoicesMixin, models.TextChoices):
    """Transaction processing state options.

    Represents the various states a transaction can be in during its lifecycle,
    from initiation to completion. Implements a state machine pattern where
    transitions between states are strictly controlled.

    References:
        https://stripe.com/docs/payments/intents#intent-statuses

    Attributes:
        REQUIRES_PAYMENT_METHOD (str): Initial state when payment method is needed
        REQUIRES_CONFIRMATION (str): Payment method received, awaiting confirmation
        REQUIRES_ACTION (str): Additional user action needed (e.g., 3DS verification)
        PROCESSING (str): Transaction is being processed by payment provider
        CANCEL (str): Terminal state indicating cancelled transaction
        SUCCESS (str): Terminal state indicating successful completion

    Example:
        # Check if a state transition is valid
        if TransactionStateChoices.can_transition_to(
            "REQUIRES_PAYMENT_METHOD",
            "REQUIRES_CONFIRMATION"
        ):
            # Perform transition
    """

    DEFAULT = "", _("---")
    REQUIRES_PAYMENT_METHOD = "REQUIRES_PAYMENT_METHOD", _("Requires Payment Method")
    REQUIRES_CONFIRMATION = "REQUIRES_CONFIRMATION", _("Requires Confirmation")
    REQUIRES_ACTION = "REQUIRES_ACTION", _("Requires Action")
    PROCESSING = "PROCESSING", _("Processing")
    CANCEL = "CANCEL", _("Cancel")
    SUCCESS = "SUCCESS", _("Success")

    @classmethod
    def can_transition_to(cls, current_state: str, new_state: str) -> bool:
        """Validate if a state transition is allowed.

        Args:
            current_state (str): The current transaction state
            new_state (str): The proposed new state

        Returns:
            bool: True if the transition is allowed, False otherwise

        Example:
            >>> TransactionStateChoices.can_transition_to("PROCESSING", "SUCCESS")
            True
            >>> TransactionStateChoices.can_transition_to("SUCCESS", "PROCESSING")
            False
        """
        return new_state in TRANSACTION_STATE_TRANSITIONS.get(current_state, set())


class TransactionTypeChoices(ChoicesMixin, models.TextChoices):
    """Transaction classification options.

    Attributes:
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

    @classmethod
    def affects_balance(cls, trans_type: str) -> bool:
        """Check if transaction type affects account balance."""
        return trans_type in TRANSACTION_TYPE_AFFECTS_BALANCE

    @classmethod
    def requires_processing(cls, trans_type: str) -> bool:
        """Check if transaction type requires payment processing."""
        return trans_type in TRANSACTION_TYPE_REQUIRES_PROCESSING


class TransactionEventTypeChoices(ChoicesMixin, models.TextChoices):
    """Transaction lifecycle event types.

    Attributes:
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
