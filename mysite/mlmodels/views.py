from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadMatForm
# Create your views here.
from django.views.decorators.http import require_POST

from common.decorators import ajax_required


@require_POST
@login_required
@ajax_required
def chat(request):
    from mlmodels.chatbot.model_chatbot import reply
    user_input = request.POST.get('input')
    if user_input:
        try:
            response=reply(user_input);
            return JsonResponse({'status': 'ok','response':response})
        except Exception:
            JsonResponse({'status': 'error','response':'sorry, something wrong on server, pls try later.'})
    return JsonResponse({'status': 'error'})



@login_required
def chatbot_page(request):
    return render(request,'mlmodels/chatbot/chatbot.html')



"""
mongo db connection part
"""
from datetime import datetime, date,timedelta
import pymongo
from ast import literal_eval
import numpy as np

dbname = 'movement_shape_predict'
# colname=date.today().strftime('%Y-%m-%d')
colname = 'movement_shape_predict'

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
except:
    print('fail to connect to mongodb, pls check connection')

# collection in databases is named by current date
mydb = myclient[dbname]
collist = mydb.list_collection_names()
mycol = mydb[colname]  # if not exit, mongodb create one for you
if not (colname in collist):
    mycol.insert_one({'time': 'test', 'data': 'test', 'result': 'test'})

previous_time=None
# mongo spark real-time prediction
@login_required
@csrf_exempt
def realtime_shape_predict(request):
    if request.method=='POST':
        global previous_time
        try:
            record = mycol.find_one(sort=[('_id', pymongo.DESCENDING)])
            t = record['time']
            print(previous_time)
            if not (t==previous_time or t=='test'):
                previous_time=t
                result=record['result']
                string_array=record['data']
                num_array = np.array(literal_eval(string_array))
                shape_part = num_array[0][:100]
                string_shape_part = np.array2string(shape_part, precision=5, separator=',', suppress_small=False)
                print(string_shape_part)
                return JsonResponse({'status': 'ok', 'response': result,'time':t,'shape_data':string_shape_part})
            else:
                return JsonResponse({'status': 'error', 'response': 'error'})
        except:
            print('sth wrong,may due to failing to convert data list from string to number')
            return JsonResponse({'status': 'error','response':'error'})
    else:
        return render(request, 'mlmodels/realtime_shape_predict/realtime_shape_predict.html')

"""
end of mongo db connection part
"""

# responsible for prediction
@login_required
@ajax_required
def shape_predict(request):
    from mlmodels.shape_predict.shape_predict_model import predict
    if request.method=='POST':
        result=predict(request.user)
        return JsonResponse({'status': 'ok','response':result})
    else:
        return JsonResponse({'status': 'error','response':"request method is not post"})

# responsible for storing file
@login_required
def shape_predict_page(request):
    from mlmodels.shape_predict.shape_predict_model import store_file
    from django.http.response import HttpResponseRedirect
    from django.urls import reverse
    if request.method=='POST':
        form=UploadMatForm(request.POST,request.FILES)
        if form.is_valid():
            if store_file(request.FILES['file'],request.user):
                messages.success(request, 'upload successfully')
            else:
                messages.error(request,'uploaded file, pls check your file format')
            return HttpResponseRedirect(reverse('mlmodels:shape_predict_page'))
    else:
        form=UploadMatForm()
        return render(request,'mlmodels/shape_predict/shape_predict.html',{'form':form})