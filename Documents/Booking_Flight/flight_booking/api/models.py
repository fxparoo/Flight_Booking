from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email not set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault('user', False)
        extra_fields.setdefault('is_superuser', False)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user


ROLES = (
    ('user', 'User'),
    ('admin', 'Admin'),

)


class AppUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=150, blank=False)
    category = models.CharField(max_length=150, blank=True)
    ticket_id = models.CharField(max_length=255, blank=True)
    modified = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=150, choices=ROLES, null=True)
    destination = models.CharField(max_length=150, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'

    objects = UserManager()
