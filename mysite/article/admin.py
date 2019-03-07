from django.contrib import admin

from .models import Article,Comment

# Register your models here.
"""
Here this decorator equals to admin.resigter(Article)(CustomizedArticle)
"""
@admin.register(Article)
class CustomizedArticle(admin.ModelAdmin):
    list_display = ('id','title','label_in_url','author','publish_time',)
    list_filter = ('publish_time','author')
    search_fields=('title','article_content')
    prepopulated_fields={'label_in_url':('title',)}
    date_hierarchy = 'publish_time'
    ordering=('publish_time',)
    raw_id_fields = ('author',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','article','created','comment_content')
    list_filter = ('created','user')
    search_fields = ('comment_content','user')


