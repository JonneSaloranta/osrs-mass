from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def _create_user(self, email, name, lastname, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')
        if not lastname:
            raise ValueError('Users must have a lastname')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            lastname=lastname,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, name, lastname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, name, lastname, password, **extra_fields)
    
    def create_superuser(self, email, name, lastname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, name, lastname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(db_index=True, max_length=255, unique=True)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname']

    class Meta:
        ordering = ['id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'