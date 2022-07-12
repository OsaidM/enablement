import random
from django.shortcuts import render, redirect
import bcrypt
from .models import User, Message, Reply
# from django.contrib.auth import get_user_model as User
from django.contrib import messages
# Create your views here.


def index(request):
    if 'user_id' in request.session:    
        del request.session['user_id']
    return render(request, 'dashboard/index.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'dashboard/signin.html')
    if request.method == 'POST':
        errors = User.objects.siginin_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/signin')
        logged_user = User.objects.get(email = request.POST['email'])
        request.session['user_id']=logged_user.id
    return redirect('/dashboard')

def register_render(request):
    return render(request, 'dashboard/register.html')

def register_user(request):
    if request.method == 'POST':
        print(dir(User))
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

            return redirect('/register')

        password=request.POST['password']
        pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name=request.POST['first_name'],
         last_name=request.POST['last_name'], 
         username=str(random.randint(0,100)),
         email=request.POST['email'],
         password=pw_hash,
         user_level = 9 if len(User.objects.all()) ==0 else 1
         )
        # new_user = User.objects.create(first_name=request.POST['first_name'],
        # last_name=request.POST['last_name'],
        # email=request.POST['email'], 
        # password=pw_hash,
        # user_level = 9 if len(User.objects.all()) ==0 else 1
        # )
        request.session['user_id']=new_user.id
        return redirect ('/dashboard')
    return redirect('/register')

def users_new(request):
    if request.method == 'GET':
        try:
            if User.objects.get(id = request.session['user_id']).user_level == 9:
                return render(request, 'dashboard/new_user.html')
        except:
            return redirect('/logout')
    return redirect('/dashboard')

def users_edit(request):
    if request.method == 'POST':
        try:
            is_admin = User.objects.get(id = request.session['user_id'])
            context = {
                'user': User.objects.get(id = request.POST['user_id']),
                'logged_user_level': is_admin.user_level
            }
            return render(request, 'dashboard/edit_user.html', context)
        except:
            return redirect('/logout')
    return redirect('/dashboard')




def users_show(request, user_id):
    if request.method == 'GET':
        try:
            context = {
                'user' : User.objects.get(id = user_id),
                'user_messages': User.objects.get(id = user_id).messages.all()
            }
            return render(request, 'dashboard/show_user.html', context)
        except:
            return redirect('/logout')
    return redirect('/dashboard')

def new_user(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

            return redirect('/register')

        password=request.POST['password']
        pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'], 
        password=pw_hash,
        user_level = 9 
        )
        return redirect ('/dashboard')
    return redirect('/new/user')

def message_user(request):
    if request.method == 'POST':
        if 'message' in request.POST.keys():
            user = User.objects.get(id = request.POST["user_id"])
            Message.objects.create(content = request.POST["message"], user = user, author= User.objects.get(id = request.session["user_id"]))
            return redirect (f'/users/show/{request.POST["user_id"]}')
    return redirect('/logout')

def message_reply(request):
    if request.method == 'POST':
        if 'reply' in request.POST.keys():
            Reply.objects.create(content = request.POST["reply"],
            user = User.objects.get(id = request.session["user_id"]), 
            message=Message.objects.get(id = request.POST["message_id"]))
            return redirect (f'/users/show/{request.POST["user_id"]}')
    return redirect('/logout')

def edit_user_info(request, user_id):
    if request.method == 'POST':
        try:
            this_user = User.objects.get(id = user_id)
            if 'description' in request.POST.keys():
                this_user.decription = request.POST['description']
                this_user.save()
                return redirect('/users/edit')
            if 'password' in request.POST.keys():
                if request.POST['password'] != request.POST['confirm_password']:
                    messages.error(request, "please confirm your password")
                    return redirect('/dashboard')
                pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
                this_user.password = pw_hash
                this_user.save()
                return redirect('/users/edit')
            if 'email' in request.POST.keys():
                this_user.email = request.POST['email']
                this_user.first_name = request.POST['first_name']
                this_user.last_name = request.POST['last_name']
                this_user.save()
                return redirect('/users/edit')
        except:
            return redirect('/dashboard')
    return redirect('/logout')

def admin_edit_user_info(request, user_id):
    if request.method == 'POST':
        try:
            this_user = User.objects.get(id = user_id)
            if 'password' in request.POST.keys():
                if request.POST['password'] != request.POST['confirm_password']:
                    messages.error(request, "please confirm your password")
                    return redirect('/dashboard')
                pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
                this_user.password = pw_hash
                this_user.save()
                return redirect('/users/edit')
            if 'email' in request.POST.keys():
                this_user.email = request.POST['email']
                this_user.first_name = request.POST['first_name']
                this_user.last_name = request.POST['last_name']
                this_user.save()
                return redirect('/users/edit')
        except:
            return redirect('/dashboard')
    return redirect('/logout')


def dashboard(request):
    try:
        this_user = User.objects.get(id = request.session['user_id'])
    except:
        return redirect('/')
    context = {
        'current_user': this_user,
        'allusers': User.objects.exclude(id = this_user.id)
    }
    return render(request, 'dashboard/dashboard.html', context=context)

def remove_user(request, user_id):
    this_user = User.objects.get(id = user_id)
    this_user.delete()
    return redirect('/dashboard')

def logout(request):
    del request.session['user_id']
    return redirect('/')
