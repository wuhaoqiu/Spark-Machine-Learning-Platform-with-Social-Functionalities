#author:Haoqiu Wu Time 19.3.1
# by setting this file, 用户现在不仅可以使用username来登录，还可以使用email来登录
# django default AUTHETICATE_BACKEND is ['django.contrib.auth.backends.ModelBackend']
# see more on https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#otherauthentication-sources.
# if you set more than one autenticate sources, only when all of them fails, authetication will fail, otherwise django will check each of them in order

from django.contrib.auth.models import User
# add this setting class to setting.py
class EmailAuthBackend(object):
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, username=None,password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None