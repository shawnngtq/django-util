import logging
import os
import sys
from typing import Optional

from django.utils.functional import lazy
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)


def init_django(
    django_dir: str,
    project_name: str | None = None,
) -> None:
    """Initializes Django environment for external Python scripts or notebooks.

    Args:
        django_dir (str): Path to Django project directory.
        project_name (Optional[str]): Name of the Django project. If None, will check DJANGO_PROJECT env var.

    Raises:
        ValueError: If project_name is not provided and DJANGO_PROJECT environment variable is not set.
        ImportError: If Django cannot be imported or setup fails.
    """
    try:
        import django
    except ImportError as e:
        logger.error(f"Failed to import Django: {e}")
        raise ImportError("Django is not installed") from e

    project_name = project_name or os.environ.get("DJANGO_PROJECT")
    if not project_name:
        raise ValueError(
            "Set an environment variable: `DJANGO_PROJECT=your_project_name` or call `init_django(your_project_name)`"
        )

    try:
        sys.path.insert(0, django_dir)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{project_name}.settings")
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        django.setup()
    except Exception as e:
        logger.error(f"Failed to setup Django: {e}")
        raise


def get_django_countries_dict() -> tuple[dict[str, str], dict[str, str]]:
    """Retrieves dictionaries mapping country codes to names and vice versa.

    Returns:
        Tuple[Dict[str, str], Dict[str, str]]: A tuple containing:
            - code_name: Dict mapping country codes to uppercase country names
            - name_code: Dict mapping uppercase country names to codes

    Raises:
        ImportError: If django-countries package is not installed.
    """
    try:
        from django_countries import countries
    except ImportError as e:
        logger.error("django-countries package is not installed")
        raise ImportError("Please install django-countries package") from e

    code_name = {k: v.upper() for k, v in dict(countries).items()}
    name_code = {v: k for k, v in code_name.items()}
    return code_name, name_code


def is_object_creator(object, profile):
    """Check if the given profile is the creator of the object.

    Args:
        object: The object to check ownership of.
        profile: The profile to verify as the creator.

    Returns:
        bool: True if the profile is the creator of the object, False otherwise.
    """
    return object.profile == profile


mark_safe_lazy = lazy(mark_safe, str)
"""Deprecated: A lazy wrapper for mark_safe function.

This function is deprecated and obsolete as of Django 4.1. It was previously used
to create lazy versions of marked-safe strings, typically for form help text with HTML.

See:
    https://docs.djangoproject.com/en/4.1/releases/4.1/#utilities
"""
