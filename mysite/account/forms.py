#author:Haoqiu Wu Time 19.2.27

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    # password check will happen when we calling is_valid() method
    # add two more fileds that donot exist in User model
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)

    # this is the model for specifically for the user model(already defined in the auth framework),
    # but only includes three fields of all. also, those fields will be validated according like other form fields
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')#usrname is defined as unique=true, so users cannot register same username

    # any methods prefix wih clean_<field> will tell django to validate this <field> and raise exception if errors happen
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match.')
        # if <field> is valid, right password will return
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('first_name','last_name','email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('photo','date_of_birth',)