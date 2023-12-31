from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_util.fields import UpperTextField, complex_fields, related_fields


# abstract
class Profile(models.Model):
    """
    Profile model extend Django User model

    Reference
    ---------
    - https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Base(models.Model):
    """
    The ideal abstract base model

    Reference
    ---------
    - https://docs.djangoproject.com/en/3.0/topics/db/models/#abstract-base-classes
    - https://stackoverflow.com/a/16838663

    Metadata

    - https://dataedo.com/kb/data-glossary/what-is-metadata

    User tracker

    - https://docs.djangoproject.com/en/3.1/topics/class-based-views/generic-editing/#models-and-request-user
    - https://stackoverflow.com/questions/5611410/related-name-argument-not-working-as-expected-in-django-model
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    # The field ConcreteModel.created_by was declared with a lazy reference to 'django_util.profile', but app 'django_util' doesn't provide model 'profile'.
    # The field ConcreteModel.updated_by was declared with a lazy reference to 'django_util.profile', but app 'django_util' doesn't provide model 'profile'.
    # created_by = models.ForeignKey(
    #     Profile,
    #     editable=False,
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     related_name="%(class)s_created_by",
    # )
    # updated_by = models.ForeignKey(
    #     Profile,
    #     editable=False,
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     related_name="%(class)s_updated_by",
    # )
    # data_source = UpperTextField(
    #     blank=True,
    #     default="",
    # )
    note = UpperTextField(
        blank=True,
        default="",
    )
    # if default=1, model formset will become required as it is no longer empty, exclude version_number in formset
    # version_number = models.PositiveBigIntegerField(
    #     blank=True,
    #     default=1,
    #     null=True,
    # )
    is_admin_verified = models.BooleanField(
        default=False,
        editable=False,
    )

    class Meta:
        abstract = True

    @staticmethod
    def get_base_meta_field_list() -> list:
        return sorted(
            [
                "created_at",
                "updated_at",
            ]
        )

    @staticmethod
    def get_extra_meta_field_list() -> list:
        return sorted(
            [
                # "created_by",
                # "updated_by",
                # "data_source",
                "note",
                # "version_number",
                "is_admin_verified",
            ]
        )

    @classmethod
    def get_field_list(cls):
        return sorted([field.name for field in cls._meta.get_fields()])

    @classmethod
    def get_field_list_without_extra_meta(cls):
        return sorted(
            list(set(cls.get_field_list()) - set(cls.get_extra_meta_field_list()))
        )

    @classmethod
    def get_field_list_without_meta(cls):
        return sorted(
            list(
                set(cls.get_field_list())
                - set(cls.get_base_meta_field_list())
                - set(cls.get_extra_meta_field_list())
            )
        )

    @classmethod
    def get_related_field_list(cls):
        field_list = []
        for field in cls._meta.get_fields():
            if isinstance(field, related_fields):
                field_list.append(field.name)
        return sorted(field_list)

    @classmethod
    def get_complex_field_list(cls):
        field_list = []
        for field in cls._meta.get_fields():
            if isinstance(field, complex_fields):
                field_list.append(field.name)
        return sorted(field_list)


class BasePublicContribute(Base):
    """
    Enhanced abstract base model, use if data can be edited by public
    """

    is_verified = models.BooleanField(
        default=False,
    )
    is_hidden = models.BooleanField(
        default=False,
    )

    class Meta:
        abstract = True


class EmailHttpRequest(Base):
    """
    Abstract model that stores email and HttpRequest fields
    """

    email = models.EmailField(
        db_index=True,
    )
    campaign = UpperTextField(
        blank=True,
        default="",
    )
    http_referrer = UpperTextField(
        blank=True,
        default="",
    )
    http_user_agent = UpperTextField(
        blank=True,
        default="",
    )
    remote_addr = models.GenericIPAddressField(
        blank=True,
        null=True,
    )
    remote_host = UpperTextField(
        blank=True,
        default="",
    )

    class Meta:
        abstract = True
