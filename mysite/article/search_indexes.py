#author:Haoqiu Wu Time 19.2.26
from haystack import indexes
from .models import Article
import datetime

# https://django-haystack.readthedocs.io/en/master/tutorial.html#

class ArticleIndex(indexes.SearchIndex,indexes.Indexable):
    text=indexes.CharField(document=True,use_template=True)
    # author=indexes.CharField(model_attr='author')
    # title=indexes.CharField(model_attr='title')
    # article_content=indexes.CharField(model_attr='article_content')
    # publish_time=indexes.DateTimeField(model_attr='publish_time')

    def get_model(self):
        return Article

    def index_queryset(self,using=None):
        return self.get_model().objects.all()