from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
# Create your models here.

class UserProfile(models.Model):
    phone_regex = RegexValidator( regex =r'^\+?1?\d{9,14}$', message = "Phone number must be entered in the format:'9999999999'.exactly 10 digis allowed.")
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    #address = models.CharField(max_length=100, default='')
    contact = models.CharField(validators=[phone_regex],max_length=10,unique=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)



    