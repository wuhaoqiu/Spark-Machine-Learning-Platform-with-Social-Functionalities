# Generated by Django 2.0.5 on 2019-03-03 16:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='images_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
