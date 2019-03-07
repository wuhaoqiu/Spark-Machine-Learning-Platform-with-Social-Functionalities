#author:Haoqiu Wu Time 19.2.26
# the power of custom template is that you can access and display data directly in the template regardless of how view works
# customized filter is useful for formatting texts,
# more see https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/#writing-custom
# template-filters.
# more about customized tag, see /howto/custom-template-tags/
from django import template
from ..models import Article
from django.db.models import Count

from django.utils.safestring import mark_safe
import markdown

register=template.Library()

# we have created a new template tag called "total_articles" by registering it in Library, which can return the total # of published articles
# .simple_tag() processes the data and return a string
@register.simple_tag
def total_articles():
    return Article.published_set.count()

# .inclusin_tag() processes the data and returns a rendered template
# 这里，我们先用inclusiontag（）制定了要渲染的template，然后在function里把数据取了出来，通过return把取出来的数据放进了template里
# 最后把这个用数据渲染过的template返回
@register.inclusion_tag('article/articles/latest_articles.html')
def show_latest_articles(count=5):
    latest_articles=Article.published_set.order_by('-publish_time')[:count]
    return {'latest_articles':latest_articles}


@register.simple_tag
def show_most_popular_articles(count=5):
    return Article.objects.annotate(num_of_comments=Count('article_comments')).order_by('-num_of_comments')[:count]

# create a new customized filter named markdown not markdown_format
@register.filter(name="markdown")
def markdown_format(text):
    # user mark_safe to mark our markdown content as safe HTML, otherwise, django by default doesnot trust any HTML contents
    return mark_safe(markdown.markdown(text))