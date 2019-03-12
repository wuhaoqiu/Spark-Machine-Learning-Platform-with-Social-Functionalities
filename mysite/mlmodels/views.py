from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_POST

from common.decorators import ajax_required


@require_POST
@login_required
@ajax_required
def chat(request):
    from .model_chatbot import reply
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