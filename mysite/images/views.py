from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from common.decorators import ajax_required

import redis
from django.conf import settings
# connect to redis
r=redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator=Paginator(images,6)
    page=request.GET.get('page')
    try:
        one_page_images=paginator.page(page)
    except PageNotAnInteger:
        one_page_images=paginator.page(1)
    except EmptyPage:
        #retrieve the last page content if page number beyond range
        one_page_images=paginator.page(paginator.num_pages)
    return render(request,'images/image/list_ajax.html',{'images': one_page_images})

@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            # create a new image instance by using form.save()
            new_item = form.save(commit=False)
            # assign current user to the item so that we can know who uploads this image
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')
            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
        else:
            messages.error(request,'fail to upload')
    else:
        # assume data comes from GET method using js tool, containing a url and title attributes
        form = ImageCreateForm()
    return render(request,'images/image/create.html',{'section': 'images','form': form})

def image_detail(request,id,slug):
    image=get_object_or_404(Image,id=id,slug=slug)
    # increment view times of an image by one
    # this method can increment the value of given key by one, if this key doesnt exist, then create one
    # using : to separate is the naming convention of Redis, object_type:id:object's attribute
    # so this will operate each time when this view is called
    total_views=r.incr('image:{}:views'.format(image.id))
    # store the number of how many people view this image into a set called image_ranking, in this set, each item key is its id,
    # then each time this view is called, increment view time by 1,also, this set is globally
    r.zincrby('image_ranking',image.id,1)
    return render(request,'images/image/detail.html',{'section':'images',
                                                      'image':image,
                                                      'total_views':total_views})


# only allow post for this view, if method is not post, return a 405 httpresponsenotallowed object
# add ajax_required so that users cannot directly access images/like to change likes
@require_POST
@login_required
@ajax_required
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                # this add() methods will not duplicate it if the request.user has already in the relationship set
                image.users_like.add(request.user)
            else:
                # this remove() will do nothing if the request.user is not in the relationship set at all
                # another userful method for many to many relationship is clear()
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except Exception:
            raise Exception
    return JsonResponse({'status':'error'})

@login_required
def image_ranking(request):
    # retrieve all elements in the ranking set called image_ranking from redis, slice so that only need first 10
    image_ranking = r.zrange('image_ranking', 0, -1,desc=True)[:10]
    # retrieve theri id number and store into a list called image_ranking_ids
    image_ranking_ids = [int(id) for id in image_ranking]
    # retrieve true image objects from MySQL
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    # 根据该image在imagerankingids里的位置来排序， python list.index(object)可以返回该object在该list中的位置
    most_viewed.sort(key=lambda x:image_ranking_ids.index(x.id))
    return render(request,
    'images/image/ranking.html',
    {'section': 'images',
    'most_viewed': most_viewed})