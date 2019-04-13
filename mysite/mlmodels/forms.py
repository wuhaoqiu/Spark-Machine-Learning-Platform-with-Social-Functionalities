#author:Haoqiu Wu Time 19.4.12
from django import forms

class UploadMatForm(forms.Form):
    file=forms.FileField()