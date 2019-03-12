#author:Haoqiu Wu Time 19.3.11
from django.urls import path
from . import views

app_name='mlmodels'

urlpatterns=[
    path('chatbot_page/',views.chatbot_page,name='chatbot_page'),
    path('chat/',views.chat,name='chat'),
]