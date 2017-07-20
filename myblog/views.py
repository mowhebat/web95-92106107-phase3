from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from myblog.admin import PostCreationForm, PostGetForm, BlogGetForm, CommentCreationForm, CommentGetForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myblog.models import Post, Blog
from django.template import RequestContext
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from myauth.models import MyUser

# Create your views here.

EXPIRY_TIME = timedelta(hours=3)

@csrf_exempt
def post(request, ID):
    user = MyUser.objects.get(token=request.META['HTTP_X_TOKEN'])
    d = (user.expiry + EXPIRY_TIME).replace(tzinfo=None)

    if d >= datetime.now():

        if request.method == 'POST':
            form = PostCreationForm(request.POST)

            if form.is_valid():
                post = form.save(commit=False)
                blog = Blog.objects.get(id=ID)
                post.author = user
                post.blog = blog
                post.save()
                return JsonResponse({'status': 0, 'post_id': blog.post.all().count()})
            else:
                if ('title' in form.errors):
                    return JsonResponse({'status': -1, 'message': form.errors['title'][0]})
                elif ('summery' in form.errors):
                    return JsonResponse({'status': -1, 'message': form.errors['summery'][0]})
                elif ('text' in form.errors):
                    return JsonResponse({'status': -1, 'message': form.errors['text'][0]})

        elif request.method == 'GET':
            form = PostGetForm(request.GET)

            if form.is_valid():
                reqsted_id = form.cleaned_data.get('id')
                blog = Blog.objects.get(id=ID)
                if blog.post.all().count() < reqsted_id:
                    return JsonResponse({'status': -1, 'message': 'post id does not exist'})

                post = blog.post.all()[reqsted_id - 1]
                token = {}
                token['id'] = post.id
                token['title'] = post.title
                token['summery'] = post.summery
                token['text'] = post.text
                token['datetime'] = post.date.strftime("%a %b %d %H:%M:%S %Y")
                return JsonResponse({'status': 0, 'post': token})
            else:
                if ('id' in form.errors):
                    return JsonResponse({'status': -1, 'message': form.errors['id'][0]})




@csrf_exempt
def blog(request, ID):
    user = MyUser.objects.get(token=request.META['HTTP_X_TOKEN'])
    d = (user.expiry + EXPIRY_TIME).replace(tzinfo=None)

    if d >= datetime.now():

        if request.method == 'GET':
            form = BlogGetForm(request.GET)

            if form.is_valid():

                l=[]
                blog = Blog.objects.get(id=ID)

                if blog.post.all().exists():

                    if (form.cleaned_data.get('count')):
                        count = form.cleaned_data.get('count')
                    else:
                        count = blog.post.all().count()

                    if (form.cleaned_data.get('offset')):
                        offset = form.cleaned_data.get('offset')
                    else:
                        offset = 0

                    for post in blog.post.order_by('-id')[offset:count+offset]:
                        token = {}
                        token['id'] = post.id
                        token['title'] = post.title
                        token['summery'] = post.summery
                        token['datetime'] = post.date.strftime("%a %b %d %H:%M:%S %Y")
                        l.append(token)
                return JsonResponse({'status': 0, 'posts': l})
            else:
                return JsonResponse({'status': -1, 'message': form.errors})



@csrf_exempt
def add_comment(request, ID):
    user = MyUser.objects.get(token=request.META['HTTP_X_TOKEN'])
    d = (user.expiry + EXPIRY_TIME).replace(tzinfo=None)

    if d >= datetime.now():

        if request.method == 'POST':
            form = CommentCreationForm(request.POST)

            if form.is_valid():
                blog = Blog.objects.get(id=ID)
                post_id = int(request.POST.get('post_id'))
                if blog.post.all().count() < post_id:
                    return JsonResponse({'status': -1, 'message': 'post id does not exist'})
                cm = form.save(commit=False)
                cm.author = user
                cm.post = blog.post.all()[post_id-1]
                cm.post.blog = blog
                cm.save()
                token = {}
                token['datetime'] = cm.date.strftime("%a %b %d %H:%M:%S %Y")
                token['text'] = cm.text
                return JsonResponse({'status': 0, 'comment': token})
            else:
                if ('post_id' in form.errors):
                    return JsonResponse({'status': -1, 'message': form.errors['post_id'][0]})
                elif ('text' in form.errors):
                    return JsonResponse({'status': -1, 'message': form.errors['text'][0]})


@csrf_exempt
def get_comments(request, ID):
    user = MyUser.objects.get(token=request.META['HTTP_X_TOKEN'])
    d = (user.expiry + EXPIRY_TIME).replace(tzinfo=None)

    if d >= datetime.now():

        if request.method == 'GET':
            form = CommentGetForm(request.GET)

            if form.is_valid():

                l=[]
                blog = Blog.objects.get(id=ID)
                post_id = form.cleaned_data.get('post_id')
                if blog.post.all().count() < post_id:
                    return JsonResponse({'status': -1, 'message': 'post id does not exist'})
                if blog.post.all().exists():
                    post = blog.post.all()[post_id-1]
                    
                    if post.comment.all().exists():

                        if (form.cleaned_data.get('count')):
                            count = form.cleaned_data.get('count')
                        else:
                            count = post.comment.all().count()

                        if (form.cleaned_data.get('offset')):
                            offset = form.cleaned_data.get('offset')
                        else:
                            offset = 0

                        for cm in post.comment.order_by('-id')[offset:count + offset]:
                            token = {}
                            token['text'] = cm.text
                            token['datetime'] = cm.date.strftime("%a %b %d %H:%M:%S %Y")
                            l.append(token)
                return JsonResponse({'status': 0, 'comments': l})
            else:
                if ('post_id' in form.errors):
                    return JsonResponse({'status': -1, 'message': form.errors['post_id'][0]})