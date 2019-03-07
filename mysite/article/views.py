from django.shortcuts import render,get_object_or_404
from .models import Article,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import ShareEmailForm,CommentForm,SearchForm
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from taggit.models import Tag


# for more aggregation function, read /topics/db/aggregation/
# Create your views here.

# tag_slug comes with the URL of this request
@login_required
def article_list(request, tag_slug=None):

    all_articles=Article.objects.all()
    all_tags=Tag.objects.all()
    tag=None

    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        all_articles=all_articles.filter(tags__in=[tag])

    # each page only display 6 posts
    paginator=Paginator(all_articles,6)
    page=request.GET.get('page')
    try:
        one_page_articles=paginator.page(page)
    except PageNotAnInteger:
        one_page_articles=paginator.page(1)
    except EmptyPage:
        #retrieve the last page content if page number beyond range
        one_page_articles=paginator.page(paginator.num_pages)
    return render(request,
                  'article/articles/article_list.html',
                  {'articles':one_page_articles,
                   'tag':tag,
                   'tags':all_tags})

@login_required
def article_detail(request,year,month,day,label_in_url):
    # query the Article table using filter as below
    article=get_object_or_404(Article,label_in_url=label_in_url,
                           publish_time__year=year,
                           publish_time__month=month,
                           publish_time__day=day,
                           )

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

# @login_required
# def share_article(request,article_id):
#     # retrieve artivle by its id
#     article=get_object_or_404(Article,id=article_id)
#     sent=False
#     error=''
#     sender_address='wuhaoqiu360@163.com'
#
#     if request.method=='POST':
#         # submitted data by user is stored in request.Post
#         form=ShareEmailForm(request.POST)
#         if form.is_valid():
#             try:
#                 # .cleaned_data returns a dict containing only
#                 # valid form field data
#                 data_from_form=form.cleaned_data
#                 # use .build_absolute_uri to build a complete URL including
#                 # HTTP shcema and hostname with post url
#                 article_url=request.build_absolute_uri(
#                     article.get_absolute_url()
#                 )
#                 subject="user {} whose email is {} recommends this article {}".format(data_from_form['name'],data_from_form['email'],article.title)
#                 message="read {} at {} \n\n {}'s email_content:{}".format(article.title,article_url,data_from_form['name'],data_from_form['email_content'])
#                 # here i must 给自己抄送y一份, otherwise, will fail to send
#                 send_mail(subject,message,sender_address,[sender_address,data_from_form['to']])
#                 sent=True
#             except Exception:
#                 form=ShareEmailForm()
#                 error='somthing wrong,failed to send email,sorry'
#     else:
#         form=ShareEmailForm()
#
#     return render(request,'article/articles/share.html',
#                       {'article':article,
#                        'form':form,
#                        'sent':sent,
#                        'error':error})

