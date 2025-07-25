from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from accounts.models import Profile
from quiz.models import UserRank,Quiz,QuizSubmission,Question
from django.contrib.auth.decorators import login_required,user_passes_test
import datetime
import math
from django.db.models import Count,Q
from .models import Message,Blog
from django.contrib import messages
from django.db.models.functions import ExtractYear
import requests
from django.shortcuts import render
import os
import feedparser
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages


def home(request):
    leaderboard_users=UserRank.objects.order_by('rank')[:3]
    context = {"leaderboard_users":leaderboard_users}
    
    return render(request, 'welcome.html', context)
@login_required 
def leaderboaard_view(request):

    leaderboard_users=UserRank.objects.order_by('rank')
    

    context={"leaderboard_users":leaderboard_users}
    return render(request,"leaderboard.html",context)
def is_superuser(user):
    return user.is_superuser
@user_passes_test(is_superuser)
@login_required 
def dashborad_view(request):
    
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


    context={     "total_users":total_users,"total_quizzes":total_quizzes,"total_quiz_submit":total_quiz_submit,"total_questions":total_questions,"today_users":today_users,"today_quizzes":today_quizzes,"today_quiz_submit":today_quiz_submit,"today_questions":today_questions ,
    "gain_users":gain_users,"gain_quizzes":gain_quizzes,"gain_quiz_submit":gain_quiz_submit,"gain_questions":gain_questions,
    "messages" :messages
             }
    return render(request,'dashboard.html',context)
def gain_percentage(total,today):
    if total > 0 and today > 0:
       gain = math.floor((today/total)*100)
       return gain
def about_view(request):
    
    return render(request,'about.html')
def blogs_view(request):
    year_blog_count=Blog.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).order_by('-year').filter(status='public')
    blogs=Blog.objects.filter(status='public').order_by('-created_at')
    
    context={"blogs":blogs,"year_blog_count":year_blog_count}
    return render(request,'blogs.html',context)
@login_required 
def blog_view(request,blog_id):
    
    
    blog=get_object_or_404(Blog,pk=blog_id)
    context={"blog":blog}
    
    return render(request,'blog.html',context)
def contact_view(request):
    
    
    
    if request.method=='POST':
         subject = request.POST.get('subject')
         message = request.POST.get('message')
         if subject is not None and message is not None :
             form=Message.objects.create(user=request.user,subject=subject,message=message)
             messages.success(request,"We got your message.We will resolve your query soon.")
             return redirect('profile',request.user.username)
         else:
             return redirect('contact')

    return render(request,'contact.html')
@user_passes_test(is_superuser)
@login_required 
def message_view(request,id):
    
    message=get_object_or_404(Message,pk=id)
    if not message.is_read:
        message.is_read=True
        message.save()

    context={"message":message}
    return render(request,"message.html",context)
def terms_conditions_view(request):
    
    return render(request,'terms-conditions.html')
def downloads_view(request):
    
    return render(request,'downloads.html')
def search_users_view(request):
    query=request.GET.get('q')
    if query:
        users=User.objects.filter(
            Q(username__icontains=query)| Q(first_name__icontains=query)| Q(last_name__icontains=query)
        ).order_by('date_joined')
    else:
        users=[]
   
    context={"query":query,"users":users}
    
    return render(request,"search-user.html",context)
def custom_404(request,exception):
    return render(request,'404.html',status=404)


def breach_checker(request):
    result = {}
    error = None

    if request.method == 'POST':
        query = request.POST.get('query', '').strip()

        if query:
            url = f"https://leakcheck.io/api/public?check={query}"

            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()

                    if data.get('success') and data.get('found', 0) > 0:
                        result = {
                            'found': data.get('found'),
                            'fields': data.get('fields', []),
                            'sources': data.get('sources', [])
                        }
                    elif data.get('success') and data.get('found', 0) == 0:
                        error = "✅ Your email was not found in any known breaches. You're safe!"
                    else:
                        error = "⚠️ Email not found in database or unknown error."
                else:
                    error = f"API Error {response.status_code}: {response.text}"
            except Exception as e:
                error = f"Something went wrong: {str(e)}"

    return render(request, 'breach_checker.html', {
        'result': result,
        'error': error
    })
def cyber_news_view(request):
    rss_url = "https://www.darkreading.com/rss.xml"  # You can replace this
    feed = feedparser.parse(rss_url)

    news_items = []
    for entry in feed.entries[:5]:  # Only showing 5 articles
        news_items.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.summary,
        })

    return render(request, 'cyber_news.html', {'news_items': news_items})
