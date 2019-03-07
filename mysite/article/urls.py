#author:Haoqiu Wu Time 19.2.21
from django.urls import path
from . import views
from . import search_view

#defile app namespace
app_name='article'

urlpatterns=[
    #first url pattern match donot capture any parameters
    path('',views.article_list,name='article_list'),
    #angel brackest used to capture parameter in the request URL
    #here this patterm will match .../2019/2/12/django-post,
    #then call this view function with corresponding arguments-
    # views.article_detail (request,year=2019,month=2,day=12,article="django-post)"
    path('tag/<slug:tag_slug>/',views.article_list,name='article_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:label_in_url>',
         views.article_detail,
         name='article_detail'),
    path('<int:article_id>/share/',views.share_article,name='article_share'),
    path(r'search/', search_view.ArticleSearchView(), name='haystack_search'),

]