#author:Haoqiu Wu Time 19.3.2
from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=('title','description','image')
        # instead directly allowing user to type url, we make this input hiddem,
        # and then provide a js tool to let user input url and pass this url as a parameter to our form
        # widgets={
        #     'url':forms.HiddenInput,
        # }

#     # customized attribute clean method, and this will only be invoked when calling .is_valid()
#     def clean_url(self):
#         # form object will not have this celaned_data attribute unitl .is_valid() is called
#         url=self.cleaned_data['url']
#         valid_extentions=['jpg','jpeg','png']
#         extention=url.rsplit('.',1)[1].lower()
#         # here is just a very simple validation method, later you can extend this for more complicated methods
#         if extention not in valid_extentions:
#             raise forms.ValidationError('the image format provided by given url doesnot have valid extention')
#
#         return url
#
#     # by overriding save() method to download image and save it every time
#     def save(self, force_insert=False,commit=True,force_update=False):
#         # create a new image instance
#         image=super(ImageCreateForm,self).save(commit=False)
#         image_url=self.cleaned_data['url']
#         # only split once
#         image_name='{}.{}'.format(slugify(image.title),image_url.rsplit('.',1))[1].lower()
# #         download the image
#         response=request.urlopen(image_url)
#         # only update image filed of an image instance by instantiating it using downloaded content
#         image.image.save(image_name,ContentFile(response.read()),save=False)
#         if commit:
#             image.save()
#
#         return image

