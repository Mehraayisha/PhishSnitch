from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.models import profile

def home(request):
    context = {}

    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile = profile.objects.filter(user=user_object).first()  # safe fetch

        context = {"user_profile": user_profile}
    
    return render(request, 'welcome.html', context)
