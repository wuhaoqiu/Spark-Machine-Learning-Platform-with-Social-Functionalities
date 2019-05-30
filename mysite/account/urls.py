#author:Haoqiu Wu Time 19.2.27
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from images.views import user_created_images,user_liked_images


urlpatterns=[
    # path('login/',views.user_login,name='login'),
    path('',views.user_dashboard,name='user_dashboard'),
    path('user_article_list/',views.user_article_list,name='user_article_list'),
    path('user_liked_images/',user_liked_images,name='user_liked_images'),
    path('user_created_images/',user_created_images,name='user_created_images'),
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    # the reason why templates of below two views donot need .is_authenticated is that these two views have been decorated by login_required
    path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    # reset password urls
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/',views.register,name='register'),
    path('edit/',views.edit,name='edit'),
    path('users/', views.user_list, name='user_list'),



]