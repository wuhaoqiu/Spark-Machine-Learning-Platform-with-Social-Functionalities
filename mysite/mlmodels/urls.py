#author:Haoqiu Wu Time 19.3.11
from django.urls import path
from . import views

app_name='mlmodels'

urlpatterns=[
    path('chatbot_page/',views.chatbot_page,name='chatbot_page'),
    path('chat/',views.chat,name='chat'),
    path('shape_predict_page/',views.shape_predict_page,name='shape_predict_page'),
    path('shape_predict',views.shape_predict,name='shape_predict'),
    path('realtime_shape_predict',views.realtime_shape_predict,name='realtime_shape_predict'),
]