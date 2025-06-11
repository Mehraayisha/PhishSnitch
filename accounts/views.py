from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import profile
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or not profile.objects.filter(user=request.user).exists():
            auth.logout(request)
        else:
            return redirect('profile', request.user.username)
    if request.method == "POST":
        email= request.POST['email']
        username= request.POST['username']
        password=request.POST['password']

        context={}
        password2=request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already registered try login ")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username already taken ")
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                user_model=User.objects.get(username=username)
                new_profile=profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('profile',user_model.username)

        else :
            messages.info(request,"Password Not Matching ")
            return redirect('register')

    context={}
    return render(request,"register.html",context)

@login_required(login_url='login')
def userprofile(request,username):
    user_object2=User.objects.get(username=username)
    user_profile2=profile.objects.get(user=user_object2)
    user_object=User.objects.get(username=request.user)
    user_profile=profile.objects.get(user=user_object)

    context={"user_profile" : user_profile,"user_profile2": user_profile2}
    return render(request,'profile.html',context)
@login_required(login_url='login')
def editprofile(request):
    user_object =User.objects.get(username=request.user)
    user_profile=profile.objects.get(user=user_object)
    if request.method=="POST":
       #img
       if request.FILES.get('profile_image') != None:
           user_profile.profile_image=request.FILES.get('profile_image')
           user_profile.save()
       #email
       if request.POST.get('email')!=None:
           U=User.objects.filter(email=request.POST.get('email')).first()
           if U == None:
               user_object.email=request.POST.get('email')
               user_object.save()
           else:
               if U != user_object:
                   messages.info(request,"Email already Used")
                   return redirect('edit_profile')
         #username      
       if request.POST.get('username')!=None:
           U=User.objects.filter(username=request.POST.get('username')).first()
           if U == None:
               user_object.username=request.POST.get('username')
               user_object.save()
           else:
               if U != user_object:
                   print("hello")
                   messages.info(request,"username already Used")
                   return redirect('edit_profile')
         #first and last name
       user_object.first_name=request.POST.get('first_name') 
       user_object.last_name=request.POST.get('last_name') 
       user_object.save()
       #bio and gender
       user_profile.location=request.POST.get('location')
       user_profile.gender=request.POST.get('gender')
       user_profile.bio=request.POST.get('bio')
       user_profile.save()
       return redirect('profile',user_object.username)


    
    context={"user_profile":user_profile}
    return render(request,'profile-edit.html',context)

@login_required(login_url='login')
def deleteprofile(request):
    user_object =User.objects.get(username=request.user)
    user_profile=profile.objects.get(user=user_object)
    if request.method=="POST":
        user_profile.delete()
        user_object.delete()
        return render(request,'index.html')
    context={"user_profile":user_profile}
    return render(request,'confirm.html',context)



def login(request):
    if request.user.is_authenticated:
        # If user is superuser or profile doesn't exist, stay on login page
        if request.user.is_superuser or not profile.objects.filter(user=request.user).exists():
            auth.logout(request)
        else:
            return redirect('profile', request.user.username)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                messages.error(request, "Superuser cannot login here.")
                return redirect('login')
            auth.login(request, user)
            return redirect('profile', username)
        else:
            messages.info(request, "Credentials invalid")
            return redirect('login')

    return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

