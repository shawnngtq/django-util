import logging
from typing import Optional

from django.core.validators import RegexValidator

logger = logging.getLogger(__name__)

is_numeric = RegexValidator(r"^[0-9]*$", "Only numbers, leading zeros are ok.")
"""RegexValidator: Validates that a string contains only numeric characters.

This validator ensures that the input string consists solely of digits (0-9).
Leading zeros are permitted in the input.

Examples:
    Valid inputs: "123", "001", "0", ""
    Invalid inputs: "12a", "-1", "1.0", "1,000"

Attributes:
    regex (str): The regular expression pattern "^[0-9]*$"
    message (str): The error message displayed when validation fails
"""


def django_validate_email(
    email: str,
    whitelist_domains: list[str] | None = None,
) -> str | None:
    """Validates an email address using Django's validator.

    Args:
        email (str): Email address to validate.
        whitelist_domains (Optional[List[str]]): List of allowed email domains.

    Returns:
        Optional[str]: The validated email address if valid, None if invalid.

    Examples:
        >>> django_validate_email("valid@email.com")
        'valid@email.com'
        >>> django_validate_email("valid@email.com", whitelist_domains=["email.com"])
        'valid@email.com'
        >>> print(django_validate_email("valid@email.com", whitelist_domains=["other.com"]))
        None
    """
    from django.core.validators import validate_email

    try:
        validate_email(email)
        if whitelist_domains:
            domain = email.split("@")[1].lower()
            if domain not in whitelist_domains:
                logger.warning(f"Email domain {domain} not in whitelist")
                return None
        return email
    except Exception as e:
        logger.debug(f"Email validation failed: {e}")
        return None


def django_validate_url(
    url: str,
    allowed_schemes: list[str] | None = None,
) -> str | None:
    """Validates a URL using Django's URL validator.

    Args:
        url (str): URL to validate.
        allowed_schemes (Optional[List[str]]): List of allowed URL schemes (e.g., ['http', 'https']).

    Returns:
        Optional[str]: The validated URL if valid, None if invalid.
    """
    from django.core.validators import URLValidator

    validator = URLValidator(
        schemes=allowed_schemes if allowed_schemes else ["http", "https", "ftp", "ftps"]
    )
    try:
        validator(url)
        return url
    except Exception as e:
        logger.debug(f"URL validation failed: {e}")
        return None


def django_validate_phone(
    phone: str,
    region: str | None = None,
) -> str | None:
    """Validates and formats a phone number using Django's phone number field.

    Args:
        phone (str): Phone number to validate.
        region (Optional[str], optional): Region code for parsing local numbers. Defaults to None.

    Returns:
        Optional[str]: The phone number in E.164 format if valid, None if invalid.

    Examples:
        >>> django_validate_phone("+1234567890")
        '+1234567890'
        >>> print(django_validate_phone("invalid"))
        None

    Note:
        Requires django-phonenumber-field package to be installed.
    """
    from phonenumber_field.phonenumber import PhoneNumber

    try:
        return PhoneNumber.from_string(phone).as_e164
    except Exception:
        try:
            return PhoneNumber.from_string(phone, region=region).as_e164
        except Exception as e:
            logger.error(e)
            return None
