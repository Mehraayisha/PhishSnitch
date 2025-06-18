from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.models import Profile
from quiz.models import UserRank,Quiz,QuizSubmission,Question
from django.contrib.auth.decorators import login_required,user_passes_test
import datetime
import math
from .models import Message

def home(request):
    leaderboard_users=UserRank.objects.order_by('rank')[:3]
    context = {"leaderboard_users":leaderboard_users}

    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.filter(user=user_object).first()  # safe fetch

        context = {"user_profile": user_profile,"leaderboard_users":leaderboard_users}
    
    return render(request, 'welcome.html', context)
@login_required(login_url='login')
def leaderboaard_view(request):

    leaderboard_users=UserRank.objects.order_by('rank')
    user_object=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_object)

    context={"leaderboard_users":leaderboard_users,"user_profile": user_profile}
    return render(request,"leaderboard.html",context)
def is_superuser(user):
    return user.is_superuser
@user_passes_test(is_superuser)
@login_required(login_url='login')
def dashborad_view(request):
    user_object=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_object)
    total_users=User.objects.all().count()
    total_quizzes=Quiz.objects.all().count()
    total_quiz_submit=QuizSubmission.objects.all().count()
    total_questions=Question.objects.all().count()
    
    today_users=User.objects.filter(date_joined__date=datetime.date.today()).count()
    today_quizzes_obj=Quiz.objects.filter(created_at__date=datetime.date.today())
    today_quizzes=Quiz.objects.filter(created_at__date=datetime.date.today()).count()
    today_quiz_submit=QuizSubmission.objects.filter(submitted_at__date=datetime.date.today()).count()
    today_questions=0
    for quiz in today_quizzes_obj:
        today_questions+=quiz.question_set.count()


    gain_users=gain_percentage(total_users,today_users)
    gain_quizzes=gain_percentage(total_quizzes,today_quizzes)
    gain_quiz_submit=gain_percentage(total_quiz_submit,today_quiz_submit)
    gain_questions=gain_percentage(total_questions,today_questions)
    
    messages=Message.objects.filter(created_at__date=datetime.date.today()).order_by('-created_at')


    context={"user_profile": user_profile,      "total_users":total_users,"total_quizzes":total_quizzes,"total_quiz_submit":total_quiz_submit,"total_questions":total_questions,"today_users":today_users,"today_quizzes":today_quizzes,"today_quiz_submit":today_quiz_submit,"today_questions":today_questions ,
    "gain_users":gain_users,"gain_quizzes":gain_quizzes,"gain_quiz_submit":gain_quiz_submit,"gain_questions":gain_questions,
    "messages" :messages
             }
    return render(request,'dashboard.html',context)
def gain_percentage(total,today):
    if total > 0 and today > 0:
       gain = math.floor((today/total)*100)
       return gain
def about_view(request):
    if request.user.is_authenticated:
       user_object=User.objects.get(username=request.user)
       user_profile=Profile.objects.get(user=user_object)
       context={"user_profle":user_profile}
    else:
        context={}
    return render(request,'about.html',context)
def blogs_view(request):
    if request.user.is_authenticated:
       user_object=User.objects.get(username=request.user)
       user_profile=Profile.objects.get(user=user_object)
       context={"user_profle":user_profile}
    else:
        context={}
    return render(request,'blogs.html',context)
@login_required(login_url='login')
def blog_view(request,blog_id):
    
    user_object=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_object)
    context={"user_profle":user_profile}
    
    return render(request,'blog.html',context)
def contact_view(request):
    if request.user.is_authenticated:
       user_object=User.objects.get(username=request.user)
       user_profile=Profile.objects.get(user=user_object)
       context={"user_profle":user_profile}
    else:
        context={}
    return render(request,'contact.html',context)
def terms_conditions_view(request):
    if request.user.is_authenticated:
       user_object=User.objects.get(username=request.user)
       user_profile=Profile.objects.get(user=user_object)
       context={"user_profle":user_profile}
    else:
        context={}
    return render(request,'terms-conditions.html',context)
def downloads_view(request):
    if request.user.is_authenticated:
       user_object=User.objects.get(username=request.user)
       user_profile=Profile.objects.get(user=user_object)
       context={"user_profle":user_profile}
    else:
        context={}
    return render(request,'downloads.html',context)