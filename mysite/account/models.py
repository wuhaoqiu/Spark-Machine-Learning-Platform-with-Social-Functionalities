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
    photo=models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)



# # this is a intermediary model for this many to many relationship, use it when you want to add extra features for your many to many relationship
# class Contact(models.Model):
#     # follower
#     user_from = models.ForeignKey('auth.User',related_name='rel_from_set',on_delete=models.CASCADE)
#     # being followed
#     user_to = models.ForeignKey('auth.User',related_name='rel_to_set',on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True,db_index=True)
#
#     class Meta:
#         ordering = ('-created',)
#
#     def __str__(self):
#         return '{} follows {}'.format(self.user_from,self.user_to)

# now that we have built the intermediary, its time to tell 那两个有关系的Model 来使用这个intermediary to construct relationship
# here because <User> is built by system, so we canot modify it, instead, dynamically add this manytomanyfield that need to be built through <Contact> to the class
# also, tell django this relationship is not symmetric, which means a follows b, b donot need to follow a
# also, when we using intermediay, when we want to delete or remove a relatioship, we can only remove corresponding <Contact> instance instead of directly chaning <User> instance
# Fianlly warning, this adding method is not recommened, the better way is
# 1. adding this to <Profile> model
# 2. using django customized model https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#specifying-a-custom-user-model
# User.add_to_class('following', models.ManyToManyField('self',through=Contact, related_name='followers',symmetrical=False))