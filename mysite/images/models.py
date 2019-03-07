from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.

class Image(models.Model):
    # foreign key used for one to many, onetoonefiled used fro one to one relationship, manytomanydield for many to many relationship
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='images_created',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/') #come to see setting.py to check the complete path setting
    description = models.TextField(blank=True)
    # db_index=True can add indexes to this column like primary key <id>,which can speed up querying using this column
    # also, actually, any foreign key or columns that need to be unique are automatically indexed by django system
    created = models.DateField(auto_now_add=True,db_index=True)
    # blank=True means that this filed is not required in the from, so by contrast, if blank=false, this filed must be contained in the field
    # also, when we design a many to many relationship, an extra table will be created using primary keys from both sides，
    # we only need to define one ManyToManyField in of of two tables, this is bidirectional, here, user.images_like and image.users_like
    users_like=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_like', blank=True)

    total_likes=models.PositiveIntegerField(db_index=True,default=0)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)

        super(Image,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail',args=[self.id,self.slug])
