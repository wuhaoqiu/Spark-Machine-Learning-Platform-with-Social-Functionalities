from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, ProfileEditForm, UserEditForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST
# from common.decorators import ajax_required
# # from .models import Contact


# Create your views here.
# about more auth views, see  https://docs.djangoproject.com/en/2.0/topics/auth/default/all-authentication-views.
# about more about message framework, see  https://docs.djangoproject.com/en/2.0/ref/contrib/messages/.
# about more about form.save(), check https://docs.djangoproject.com/en/2.1/topics/forms/modelforms/#the-save-method
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # this authenticate() method will return a user object if the user has been authenticated or None
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    # this login method can set user int the righnt session, authenticate responsible for checking credentilas
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form,})

# this decorator checks whether the user has been authenticated, if so, it executes this view.
# if not, this decorator redirects user to the login URL with GET method using 'next' as parameter
@login_required
def user_dashboard(request):
    return render(request, 'account/user_dashboard.html', {'section': 'user_dashboard'})

def main_page(request):
    from article.models import Article
    top_three_articles=Article.objects.order_by('-publish_time')[:3]
    return render(request, 'index.html',{'articles':top_three_articles})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
    # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
    # instead of saving pure text password, we use set_password to encryption the password and save 加密过的密码
            new_user.set_password(user_form.cleaned_data['password'])
            if check_duplicate(user_form):
                messages.error(request,"email exist")
    # Save the User object
            else:
                new_user.save()
                # after creating a new user, create a profile corresponding to it
                Profile.objects.create(user=new_user)
                from django.http import HttpResponseRedirect
                from django.urls import reverse
                return HttpResponseRedirect(reverse('login'))
    else:
        user_form = UserRegistrationForm()
    #     if method is not post or input is not valid, render register page again
    return render(request,'account/register.html',{'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        # create a form to change the current user/profile by using instance=request.user
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        # when editting, check whether email duplicate
        current_user_email=request.user.email
        if user_form.is_valid() and profile_form.is_valid() and (True if user_form.cleaned_data['email'] == current_user_email else check_duplicate(user_form)):
            # if ModelForm object receive a instance, this will update the existing oebjct, otherwise, this will create and store a new object into the database
            user_form.save()
            profile_form.save()
            # use django message framework to display messages to users's actions
            messages.success(request,'profile and user information updated successfully')
            from django.http.response import HttpResponseRedirect
            from django.urls import reverse
            return HttpResponseRedirect(reverse('edit'))
        else:
            messages.error(request,'updated failed')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def check_duplicate(self):
    if self.is_valid():
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return True
        else:
            return False
    else:
        return True

@login_required
def user_list(request):
    # users = User.objects.filter(is_active=True)
    users = User.objects.filter()
    paginator=Paginator(users,6)
    page=request.GET.get('page')
    try:
        one_page_users=paginator.page(page)
    except PageNotAnInteger:
        one_page_users=paginator.page(1)
    except EmptyPage:
        #retrieve the last page content if page number beyond range
        one_page_users=paginator.page(paginator.num_pages)
    return render(request,'account/user/list.html',{'section': 'people','users': one_page_users})

# @login_required
# def user_detail(request, username):
#     # user = get_object_or_404(User,username=username,is_active=True)
#     user = get_object_or_404(User,username=username)
#     # later we can use this to show images by popularity
#     # images_by_popularity = Image.objects.order_by('-total_likes')
#     return render(request,'account/user/detail.html',{'section': 'people','user': user})

# @ajax_required
# @require_POST
# @login_required
# def user_follow(request):
#     user_id = request.POST.get('id')
#     action = request.POST.get('action')
#     if user_id and action:
#         try:
#             user = User.objects.get(id=user_id)
#             if action == 'follow':
#                 Contact.objects.get_or_create(
#                     user_from=request.user,user_to=user)
#             else:
#                     # add(), remove() methods cant be used because of use of intermediary
#                     Contact.objects.filter(user_from=request.user,user_to=user).delete()
#             return JsonResponse({'status':'ok'})
#         except User.DoesNotExist:
#             return JsonResponse({'status':'error'})
#     return JsonResponse({'status':'error'})
#

@login_required
def user_article_list(request):

    from article.models import Article
    all_articles=Article.objects.filter(author=request.user)
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
                  'account/user/user_article_list.html',
                  {'articles':one_page_articles,})
