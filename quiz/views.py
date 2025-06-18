from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Quiz,Category,QuizSubmission
from django.contrib import messages
# Create your views here.
@login_required(login_url='login')
def all_quiz_view(request):
    user_object=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_object)
    quizzes=Quiz.objects.order_by('-created_at')
    categories=Category.objects.all()
    context={"user_profile" : user_profile,"quizzes" : quizzes,"categories":categories}
    return render(request,'all-quiz.html',context)
@login_required(login_url='login')
def search_view(request,category):
    user_object=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_object)
    categories=Category.objects.all()
    if category != "":
       quizzes=Quiz.objects.filter(category__name=category)
    else:
       quizzes=Quiz.objects.order_by('-created_at')

    context={"user_profile" : user_profile,"quizzes" : quizzes,"categories":categories}
    return render(request,'all-quiz.html',context)
@login_required(login_url='login')
def quiz_view(request,quiz_id):
    user_object=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_object)
    quiz=Quiz.objects.filter(id=quiz_id).first()
    total_questions=quiz.question_set.all().count()
    if  request.method == "POST":
        score=int(request.POST.get('score',0))
        if QuizSubmission.objects.filter(user=request.user,quiz=quiz).exists():
            messages.success(request,f"this time you got {score} out of {total_questions}")
            return redirect('quiz',quiz_id)
        submission=QuizSubmission(user=request.user,quiz=quiz,score=score)
        submission.save()
        messages.success(request,f"Quiz submitted succesfully. You got {score} out of {total_questions}")
        return redirect('quiz',quiz_id)
    
    if quiz != None:
        context={"user_profile":user_profile,"quiz":quiz}
    else :
        return redirect('all_quiz')
    
    
    return render(request,'quiz.html',context)