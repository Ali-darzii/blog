from django.contrib.auth import user_logged_in
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator
from rest_framework.exceptions import ValidationError
from utils.base_model import BaseModel
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

class New(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.title


class User(BaseModel):
    _username_validator = UnicodeUsernameValidator()
    _validate_email = EmailValidator()

    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

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

    def clean(self):
        super(User, self).clean()
        self._username_validator(self.username)
        if self.email:
            self.email = self._normalize_email(self.email)
            self._validate_email(self.email)
        if not self.password:
            raise ValidationError("Password is required")
