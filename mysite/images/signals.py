#author:Haoqiu Wu Time 19.3.3

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image
# Although denormalize can sometimes improve performance, pls consider database indexes, query optimization, and caching, before starting to denormalize your data.
# using Django.signal to denormalize data, see more  https://docs.djangoproject.com/en/2.0/ref/signals/
# useful ones are pre_save():registed function will work eachtime when calling save(),
# pre_delete(),m2m_changed(): registered function will work each time when one ManyToMantyFiled changes
# this is synchronous
# here we use @receiver to register users_like_changed function as a receiver to let it work each time when sender sends signal, here Image.users_like changes
# we still need to register our receivers by importing signals modeule inside the read() method in configuration class, check images.apps.py
@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()