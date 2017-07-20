from django.shortcuts import render_to_response, render
from django.http import HttpResponse, JsonResponse
from myauth.models import MyUser
from django.views.decorators.csrf import csrf_exempt
from myauth.admin import UserCreationForm, UserLogForm
from django.contrib.auth import authenticate, login, logout
import random, string
from django.middleware import csrf
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from jose import jws

# Create your views here.

@csrf_exempt
def myregister(request):

    if request.method == 'POST':
        # this is the form with the submitted data
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            # the submitted data is correct
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password1 = request.POST.get('password1')

            my_user = MyUser(username=username, email=email, first_name=first_name, last_name=last_name, password=password1)

            # this is a new user with the same email and password
            # than the currently logged-in user. It's not what you want
            # and it won't work if you're not logged-in
            my_user.save()
            return JsonResponse({'status':0})
    else:
        form = UserCreationForm()

    if ( 'username' in form.errors ):
        return JsonResponse({'status': -1, 'message': form.errors['username'][0]})
    elif ( 'first_name' in form.errors ):
        return JsonResponse({'status': -1, 'message': form.errors['first_name'][0]})
    elif ( 'last_name' in form.errors ):
        return JsonResponse({'status': -1, 'message': form.errors['last_name'][0]})
    elif ( 'email' in form.errors ):
        return JsonResponse({'status': -1, 'message': form.errors['email'][0]})
    elif ( 'password1' in form.errors ):
        return JsonResponse({'status': -1, 'message': form.errors['password1'][0]})
    elif ( 'password2' in form.errors ):
        return JsonResponse({'status': -1, 'message': form.errors['password2'][0]})



@csrf_exempt
def mylogin(request):

    if request.method == 'POST':
        # this is the form with the submitted data
        form = UserLogForm(data=request.POST)

        if form.is_valid():
            # the submitted data is correct
            username = request.POST.get('username')
            password = request.POST.get('password')
            if MyUser.objects.filter(username=username, password=password).exists():
                user = MyUser.objects.get(username=username, password=password)
                user.token = \
                    ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(64))
                user.expiry = datetime.now()
                user.save(update_fields=["token"])
                user.save(update_fields=["expiry"])

                if user.is_active:
                #    login(request, user)
                    return JsonResponse({'status': 0, 'token': user.token})
    else:
        form = UserLogForm()

    if ( 'username' in form.errors ):
        return JsonResponse({'status': -1, 'message': form.errors['username'][0]})
    elif ( 'password' in form.errors ):
        return JsonResponse({'status': -1, 'message': form.errors['password'][0]})


EXPIRY_TIME = timedelta(hours=3)
@csrf_exempt
def myblogid(request):

    user = MyUser.objects.get(token=request.META['HTTP_X_TOKEN'])
    d = (user.expiry + EXPIRY_TIME).replace(tzinfo=None)

    if d >= datetime.now():

        if user.blog.all().exists():
            blog = user.blog.all()[0]
            return JsonResponse({'status': 0, 'blog_id': blog.id})

    return JsonResponse({'status': -1})