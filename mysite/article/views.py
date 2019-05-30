from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Article,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import ShareEmailForm,CommentForm,SearchForm,ArticleForm
# from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from taggit.models import Tag


# for more aggregation function, read /topics/db/aggregation/
# Create your views here.

# tag_slug comes with the URL of this request
@login_required
def article_list(request, tag_slug=None):

    all_articles=Article.objects.all()
    tag=None

    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        all_articles=all_articles.filter(tags__in=[tag])

    # each page only display 6 posts
    paginator=Paginator(all_articles,3)
    page=request.GET.get('page')
    try:
        one_page_articles=paginator.page(page)
    except PageNotAnInteger:
        one_page_articles=paginator.page(1)
    except EmptyPage:
        #retrieve the last page content if page number beyond range
        one_page_articles=paginator.page(paginator.num_pages)

    new_article = None

    if request.method == 'POST':
        article_form = ArticleForm(data=request.POST)
        if article_form.is_valid():
            # comment_form.save can create a comment object,but donot save to database immediatley
            new_article = article_form.save(commit=False)
            new_article.author = request.user
            cd = article_form.cleaned_data
            from django.utils import timezone
            from django.contrib import messages
            if not Article.objects.filter(publish_time=timezone.now()).filter(label_in_url=cd.get('label_in_url')).exists():
                new_article.save()
                for each_tag in cd.get('tags'):
                    new_article.tags.add(each_tag)
                messages.success(request, 'profile and user information updated successfully')
                from django.http.response import HttpResponseRedirect
                from django.urls import reverse
                return HttpResponseRedirect(reverse('article:article_list'))
            else:
                messages.error(request, 'updated failed, may because duplicate slug today')

    # if this view is called by GET method, then render a brand new form
    else:
        article_form = ArticleForm()

    return render(request,
                  'article/articles/article_list.html',
                  {'articles':one_page_articles,
                   'tag':tag,
                   'article_form':article_form})

@login_required
def article_detail(request,year,month,day,label_in_url):
    # query the Article table using filter as below
    article=get_list_or_404(Article,label_in_url=label_in_url,
                           publish_time__year=year,
                           publish_time__month=month,
                           publish_time__day=day,
                           )[0]

    # list active comments
    comments=article.article_comments.all()

    # each page only display 6 posts
    paginator = Paginator(comments, 6)
    page = request.GET.get('page')
    try:
        one_page_comments = paginator.page(page)
    except PageNotAnInteger:
        one_page_comments = paginator.page(1)
    except EmptyPage:
        # retrieve the last page content if page number beyond range
        one_page_comments = paginator.page(paginator.num_pages)

    new_comment=None

    if request.method=='POST':
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            # comment_form.save can create a comment object,but donot save to database immediatley
            new_comment=comment_form.save(commit=False)
            new_comment.article=article
            new_comment.user=request.user
            new_comment.save()

            # prevent submitting same forms again when refresh page
            from django.http.response import HttpResponseRedirect
            from django.urls import reverse
            return HttpResponseRedirect(reverse('article:article_detail',
                       args=[
                           article.publish_time.year,
                           article.publish_time.month,
                           article.publish_time.day,
                           article.label_in_url
                       ]))
    # if this view is called by GET method, then render a brand new form
    else:
        comment_form=CommentForm()

    # flat=True, let tuple returned by values_list() to a python list
    article_tags_list=article.tags.values_list('id',flat=True)
    similar_articles=Article.published_set.filter(tags__in=article_tags_list).exclude(id=article.id)

        # use Count() to generate a new filed to those retrieved articles, named same_tags, then
        # order those articles by this new attribute - same_tags
    similar_articles=similar_articles.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish_time')[:3]


    # use the object returned by above filter to render detail.html
    return render(request,'article/articles/article_detail.html',
                  {'article':article,
                   'comments':one_page_comments,
                   'new_comment':new_comment,
                   'comment_form':comment_form,
                   'similar_articles':similar_articles,})

