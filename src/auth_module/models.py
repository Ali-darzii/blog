from django.contrib.auth import user_logged_in
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator
from rest_framework.exceptions import ValidationError
from utils.models import BaseModel


class User(BaseModel):
    last_login = None
    date_joined = None
    _username_validator = UnicodeUsernameValidator()
    _validate_email = EmailValidator()

    def __init__(self, username, first_name=None, last_name=None, email=None, is_active=True, is_staff=False, is_superuser=False):
        self.username: str = username
        self.first_name: str | None = first_name
        self.last_name: str | None = last_name
        self.email = email
        self.password: str | None = None
        self.is_active: bool = is_active
        self.is_staff: bool = is_staff
        self.is_superuser: bool = is_superuser

    def __str__(self):
        return self.username

    @classmethod
    def _normalize_email(cls, email):
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        return email

    @property
    def is_admin(self):
        return self.is_superuser and self.is_staff

    @property
    def is_authenticated(self):
        raise NotImplemented

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def _clean(self):
        self._username_validator(self.username)
        if self.email:
            self.email = self._normalize_email(self.email)
            self._validate_email(self.email)
        if not self.password:
            raise ValidationError("Password is required")

    def insert_one(self):
        self._clean()
        return super(User, self).insert_one()