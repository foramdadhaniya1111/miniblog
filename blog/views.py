from django.shortcuts import render,HttpResponseRedirect
from .forms import signupform
from .forms import loginform , Postform
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.
#Home
def home(request):
    posts = Post.objects.all()
    return render(request , 'blog/home.html',{'posts':posts})

#About
def about(request):
    return render(request,'blog/about.html')

#contact
def contact(request):
    return render(request,'blog/contact.html')

#dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#signup
def user_signup(request):
    if request.method == 'POST':
        form = signupform(request.POST)
        if form.is_valid():
            messages.success(request,'Congretulation !! You have Become an author')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = signupform()
    return render(request,'blog/signup.html',{'form':form})


#login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = loginform(request=request , data=request.POST)
            if form.is_valid():
                uname =form.cleaned_data['username']
                upass =form.cleaned_data['password']
                user = authenticate(username=uname , password=upass)
                if user is not None:
                    login(request , user)
                    messages.success(request,'Logged in Successfully!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = loginform()
        return render(request,'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')


#add New Post

def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Postform(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title,desc=desc)
                pst.save()
                messages.success(request,'Add Blog Successfully!!')
                form = Postform()
        else:
            form = Postform()
        return render(request,'blog/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

#update post
def update_post(request , id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = Postform(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request,'Delete Blog Successfully!!')
        else:
            pi = Post.objects.get(pk=id)
            form = Postform(instance=pi)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')
    

#delete post:
def delete_post(request , id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            messages.success(request,'Delete Blog Successfully!!')
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')