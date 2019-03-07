from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

from taggit.managers import TaggableManager
# Create your models here.
# customer manager,https://docs.djangoproject.com/en/2.1/topics/db/managers/
# related name https://docs.djangoproject.com/en/2.1/topics/db/queries/#backwards-related-objects
# more about manytoone in django  /db/examples/many_to_one/

class CustomizedArticleManager(models.Manager):
    def get_queryset(self):
        return super(CustomizedArticleManager,self).get_queryset()


class Article(models.Model):
    # ARTICLE_STATUS=(
    #     ('D','Drafted'),
    #     ('P','Published'),
    # )
    label_in_url=models.SlugField(max_length=100,
                                  unique_for_date='publish_time')
    title=models.CharField(max_length=100)
    # when we want to retrieve objects related to a user, we can use "user.posted_articles.all()"
    author=models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='posted_articles',
                             )
    article_content=models.TextField()
    publish_time=models.DateTimeField(default=timezone.now)
    # create_time=models.DateTimeField(auto_now_add=True)
    # status=models.CharField(max_length=20,
    #                         choices=ARTICLE_STATUS)

    # customer manager,https://docs.djangoproject.com/en/2.1/topics/db/managers/
    objects=models.Manager()
    published_set=CustomizedArticleManager()
    # this tags manager will allow to add,remove tags
    tags=TaggableManager()

    class Meta:
        ordering=('-publish_time',)
        db_table='article_from_user'
        unique_together=(('id','author'),)

    def __str__(self):
        return self.title

    #later will use this method to help templates to link to specific articles
    def get_absolute_url(self):
        # using self information in Article table as parameters to fill in corresponding variables in path formula
        # in article\urls.py.article_detail, path('<int:year>/<int:month>/<int:day>/<slug:label_in_url>',

        # also, here the the namespace "article" corresponds to
        # the namespace defined in the mysite/rls.py, this is instance namespace
        #so here we can see that different models can use different instance namespace to
        #use differenct url path to access a single view


        return reverse('article:article_detail',
                       args=[
                           self.publish_time.year,
                           self.publish_time.month,
                           self.publish_time.day,
                           self.label_in_url
                       ])

class Comment(models.Model):
    article=models.ForeignKey(Article,on_delete=models.CASCADE,related_name='article_comments')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='posted_comments',null=True
                             )
    # name=models.CharField(max_length=40)
    # email=models.EmailField()
    comment_content=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    # active=models.BooleanField(default=True)

    class Meta:
        ordering=('created',)
        def __str__(self):
            return "Commented from on {}".format(self.article)