# User,Group,Permission
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

# this will create one more table called Profile, 并不是在原User table里直接增加
class Profile(models.Model):
    # instead of inheritance, we use OneToOneField to extend models, so this is usually used in a child model
    # Using settings.AUTH_USER_MODEL to relate profile with auth.user model
    # get_user_model will attempt to retrieve the model class at the moment your app is imported the first time.
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth=models.DateField(blank=True, null=True)
    # in order to upload images, we need to add some lines in settings.py
    photo=models.ImageField(upload_to='users/%Y/%m/%d/', blank=True,default='default/default_profile.png')

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

