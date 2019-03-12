"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('article/', include('article.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from account.views import main_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', main_page,name='main_page'),
    #first article is application namespcae, second article is instance namespace,
    # each app can only have one application name, but can have multiple instance names
    path('articles/',include('article.urls',namespace='article')),
    path('account/',include('account.urls')),
    path('social-auth/',include('social_django.urls',namespace='social')),#in order to make this work, edit /etc/hosts
    path('images/',include('images.urls',namespace='images')),
    path('mlmodels/',include('mlmodels.urls',namespace='mlmodels'))
]

if settings.DEBUG:
    # this static helper fuction aims at helping developer debug static files when developing
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



