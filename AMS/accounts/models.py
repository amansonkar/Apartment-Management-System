from __future__ import unicode_literals
from django.db import models, transaction
from django.contrib.auth.models import(
    User, AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import regex_phone
from django.utils import timezone
#from .db_models import *
# Create your models here.
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete = models.CASCADE)
#     name = models.CharField(max_length=50, blank=True)
#     flat_number = models.TextField(max_length=10)
#     door_number = models.TextField(max_length=10, blank=True)
#     recent_photo = models.ImageField(upload_to=user_directory_path)
#     id_proof = models.FileField(upload_to=user_directory_path)
#     father_name = models.CharField(max_length=50)
#     mother_name = models.CharField(max_length=50)
#     occupation = models.TextField(max_length=50)
#     communication_address = models.TextField(max_length=300)
#     communication_address_proof = models.FileField(upload_to=user_directory_path)
#     permanent_address = models.TextField(max_length=300)
#     permanent_address_proof = models.FileField(upload_to=user_directory_path)
#     mobile_number = models.CharField(max_length=10)
#     flat_occupancy_status = models.BooleanField(default=False)
#     copy_of_sale_deed = models.FileField(upload_to=user_directory_path)

# class TenantProfile(models.Model):
#     userprofile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50, blank=True)
#     father_name = models.CharField(max_length=50, blank=True)
#     mother_name = models.CharField(max_length=50, blank=True)
#     occupation = models.TextField(max_length=50, blank=True)
#     id_proof = models.FileField(upload_to=user_directory_path, blank=True)
#     recent_photo = models.ImageField(upload_to=user_directory_path, blank=True)
#     permanent_address = models.TextField(max_length=300, blank=True)
#     permanent_address_proof = models.FileField(upload_to=user_directory_path, blank=True)
#     mobile_number = models.CharField(max_length=10, blank=True)
#     email_id = models.EmailField(max_length=50, blank=True)
#     vehicle_type = models.TextField(max_length=30, blank=True)
#     vehicle_registration_number = models.CharField(max_length=30, blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()

class OTP(models.Model):
    contact = models.CharField(max_length=10, validators=[regex_phone()])
    is_otp_verified = models.BooleanField(default=False)

# class PasscodeVerify(models.Model):
#     mobile = models.IntegerField(primary_key=True)
#     passcode = models.CharField(max_length = 7,default='0000')
#     is_verified = models.BooleanField(default=False)
#     created_on = models.DateTimeField(auto_now_add=True)
 
#     def __str__(self):
#         return (str(self.mobile) + ',' + self.passcode)

# class UserBaseManager(models.Manager):
#     def get_by_natural_key(self,mobile):
#         return self.get(mobile = mobile)


# class UserBase(models.Model):
#     mobile = models.IntegerField(primary_key=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     token = models.CharField(max_length = 50,default = 'xyz')
#     is_active = models.BooleanField(default = False)
#     is_vendor = models.BooleanField(default=False)
    
#     REQUIRED_FIELDS =['email','door_number']
#     USERNAME_FIELD = 'mobile'

#     def is_active_user(self):
#         return self.is_active

#     def is_vendor(self):
#         return self.is_vendor

#     def __str__(self):
#         return self.mobile

# class User_OTP(models.Model):
#     mobile_number=models.CharField(max_length=10)
#     OTP = models.CharField(max_length=6, blank=True, null=True, default=None)

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, password=password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=40, unique=True)
    contact = models.CharField(max_length=10, validators=[regex_phone()])
    door_number = models.TextField(max_length=10)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=20,default='abc')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contact','door_number']

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        return self



class UserDetail(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    flat_number = models.TextField(max_length=10)
    recent_photo = models.ImageField(upload_to=user_directory_path)
    id_proof = models.FileField(upload_to=user_directory_path)
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    occupation = models.TextField(max_length=50)
    communication_address = models.TextField(max_length=300)
    communication_address_proof = models.FileField(upload_to=user_directory_path)
    permanent_address = models.TextField(max_length=300)
    permanent_address_proof = models.FileField(upload_to=user_directory_path)
    mobile_number = models.CharField(max_length=10)
    flat_occupancy_status = models.BooleanField(default=False)
    copy_of_sale_deed = models.FileField(upload_to=user_directory_path)


class ResetPassword(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reset_passwords')
    token = models.CharField(max_length=100, unique=True,error_messages={'unique': 'This token has already been taken.'})
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    