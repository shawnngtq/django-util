import importlib.util
import unittest

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase

from django_util.models import Profile
from django_util.utility import get_django_countries_dict
from django_util.validators import (
    django_validate_email,
    django_validate_phone,
    django_validate_url,
)


# Create your tests here.
def user_example1(**kwargs):
    """Creates and returns a test user with default credentials.

    Args:
        **kwargs: Additional fields to be passed to User.objects.create()

    Returns:
        User: A newly created User instance with default username and password
    """
    user = User.objects.create(username="your_username", password="your_password")
    user.save()
    return user


class UserModelTests(TestCase):
    """Test suite for User model functionality.

    Tests basic user creation and field validation.
    """

    def test_user(self):
        """Test basic user creation and field values.

        Ensures:
            - User instance is created successfully
            - Username matches expected value
            - Password matches expected value
        """
        u1 = user_example1()
        self.assertTrue(isinstance(u1, User))
        self.assertEqual(u1.username, "your_username")
        self.assertEqual(u1.password, "your_password")


class ProfileModelTests(TestCase):
    """Test suite for Profile model functionality.

    Tests profile creation and its relationship with User model.
    """

    def test_profile(self):
        """Test profile creation and association with user.

        Ensures:
            - Profile is created automatically with user
            - Profile is correctly associated with user
            - Default balance is set to 0
        """
        u1 = user_example1()
        p1 = Profile.objects.get(id=1)
        self.assertTrue(isinstance(p1, Profile))
        self.assertEqual(u1.profile, p1)
        self.assertEqual(p1.balance, 0)


class ValidatorTests(SimpleTestCase):
    """Test suite for the moved data-manipulation validator helpers."""

    def test_validate_email(self):
        self.assertEqual(django_validate_email("valid@email.com"), "valid@email.com")
        self.assertEqual(
            django_validate_email("valid@email.com", whitelist_domains=["email.com"]),
            "valid@email.com",
        )
        self.assertIsNone(
            django_validate_email("valid@email.com", whitelist_domains=["other.com"])
        )
        self.assertIsNone(django_validate_email("not-an-email"))

    def test_validate_url(self):
        self.assertEqual(
            django_validate_url("https://example.com"),
            "https://example.com",
        )
        self.assertIsNone(django_validate_url("not a url"))

    @unittest.skipUnless(
        importlib.util.find_spec("phonenumber_field"),
        "requires django-phonenumber-field",
    )
    def test_validate_phone(self):
        self.assertEqual(django_validate_phone("+1234567890"), "+1234567890")
        self.assertIsNone(django_validate_phone("invalid"))

    @unittest.skipUnless(
        importlib.util.find_spec("django_countries"),
        "requires django-countries",
    )
    def test_get_django_countries_dict(self):
        code_name, name_code = get_django_countries_dict()
        self.assertIn("US", code_name)
        self.assertEqual(code_name["US"], code_name["US"].upper())
        self.assertEqual(name_code[code_name["US"]], "US")
