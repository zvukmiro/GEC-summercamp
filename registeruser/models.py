from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse


# Create your models here.
class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, first_name, last_name, address, phone, **extra_fields):

        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user_obj = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone,
            **extra_fields,
            )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_user(self, username, email, password, first_name, last_name, address, phone, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, first_name, last_name, address, phone, **extra_fields)

    def create_superuser(self, username, email, password, first_name, last_name, address, phone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, first_name, last_name, address, phone, **extra_fields)

    def _update_user(self, last_name, email, address, phone, **extra_fields):

        email = self.normalize_email(email)
        user_obj = self.model(
            email=email,
            last_name=last_name,
            address=address,
            phone=phone,
            **extra_fields,
            )
        user_obj.save(using=self._db)
        return user_obj

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length = 55)
    last_name = models.CharField(max_length = 55)
    address = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 15, help_text='digits only, no brackets or dashes')

    # USERNAME_FIELD = 'email' if you are changing login
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'address', 'phone']
    # Username & Password are required by default.
    objects = CustomUserManager()

    def get_full_name(self):
        return self.first_name, self.last_name

    def __str__(self):
        return f'{ self.first_name } { self.last_name }  (contact  { self.email })'

    def get_absolute_url(self):
        return reverse('parent-detail', args=[str(self.id)])
        # return reverse('parent-detail', kwargs={'pk': self.id})

    def user_id(self):
        return self.id

    def user_is_loggeduser(self, pk):
        return self.id==pk

    @property
    def is_admin(self):
        return self.admin

    def balance(self):
        # return aggregate([p.price for p in self.camps.all()])
        return sum([p.total_price() for p in self.children.all()])
        balance.short_description = 'Dollars'
