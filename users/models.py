import os
import uuid
import binascii

from django.db import models
from .data import set_password, check_password
from django.contrib.auth.base_user import (AbstractBaseUser, BaseUserManager)
from localflavor.us.models import USStateField, USZipCodeField, USSocialSecurityNumberField
from localflavor.us.us_states import STATE_CHOICES

from binascii import unhexlify
from Paymenypayfort import settings

# Create your models here.
def profile_image(instance, filename):
    file = filename.split('.')[-1]
    name = '%s.%s' % (instance.user_id, file)
    path = 'profile_images/'
    return os.path.join(path, name)


def temp_profile_image(instance, filename):
    file = filename.split('.')[-1]
    name = '%s.%s' % (instance.id, file)
    path = 'temp_profile_images/'
    return os.path.join(path, name)




class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Please provide email.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True  # set by b
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self._create_user(email, password, **extra_fields)


class Users(AbstractBaseUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    ssn = USSocialSecurityNumberField(max_length=11, default=None)
    zipcode = USZipCodeField(max_length=10)
    password = models.CharField(max_length=128)
    state = USStateField(max_length=2, choices=STATE_CHOICES,default=None)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to=profile_image, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_on = models.DateTimeField()
    last_accessed_on = models.DateTimeField()
    mobile_verification_status = models.BooleanField(default=False)
    email_verification_status = models.BooleanField(default=False)
    address = models.TextField(max_length=400, default=None)
    termsconditions = models.BooleanField(default=False)
    remember_me = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

    def set_password(self, raw_password):
        self.password = set_password(raw_password)

    def check_password(self, raw_password):
        check_password(self.password, raw_password)




class TempUser(models.Model):
    full_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    ssn = USSocialSecurityNumberField(max_length=11, default=None)
    zipcode = USZipCodeField(max_length=10)
    state = USStateField(max_length=2, choices=STATE_CHOICES, default=None)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to=profile_image, null=True, blank=True)
    mobile_token = models.CharField(max_length=4)
    email_token = models.CharField(max_length=50, null=True)
    created_on_mobile = models.DateTimeField()
    created_on_email = models.DateTimeField()
    email_verification_status = models.BooleanField(default=False)
    mobile_verification_status = models.BooleanField(default=False)
    address = models.TextField(max_length=400, default=None)
    termsconditions = models.BooleanField(default=False)
    remember_me = models.BooleanField(default=False)

    def __str__(self):
        return str(self.phone_number)

class ResetPassword(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    mobile_token = models.CharField(max_length=4, blank=True, null=True)
    email_token = models.CharField(max_length=50, blank=True, null=True)
    created_on_mobile = models.DateTimeField(blank=True, null=True)
    created_on_email = models.DateTimeField(blank=True, null=True)
    mobile_verification_status = models.BooleanField(default=False)
    email_verification_status = models.BooleanField(default=False)


    def __str__(self):
        return str(self.user)


class Token(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
            return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

class ProfileImage(models.Model):
    profile_image = models.ImageField(upload_to=temp_profile_image, null=True, blank=True)
# Create your models here.
