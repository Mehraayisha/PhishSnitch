from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Profile
from .models import Quiz,Category,QuizSubmission
from django.contrib import messages

# Create your views here.
@login_required 
def all_quiz_view(request):
    
    quizzes=Quiz.objects.order_by('-created_at')
    categories=Category.objects.all()
    context={"quizzes" : quizzes,"categories":categories}
    return render(request,'all-quiz.html',context)
@login_required 
def search_view(request,category):
    
    categories=Category.objects.all()
    if category != "":
       quizzes=Quiz.objects.filter(category__name=category)
    else:
       quizzes=Quiz.objects.order_by('-created_at')

    context={"quizzes" : quizzes,"categories":categories}
    return render(request,'all-quiz.html',context)
@login_required 
def quiz_view(request,quiz_id):
    
    quiz=get_object_or_404(Quiz,pk=quiz_id)
    
    if  request.method == "POST":
        score=int(request.POST.get('score',0))
        
        submission=QuizSubmission(user=request.user,quiz=quiz,score=score)
        submission.save()
        
        return redirect('quiz_result',submission_id=submission.id)
    
    
    
    return render(request,'quiz.html',{'quiz':quiz})
@login_required
def quiz_result_view(request,submission_id):
    submission=get_object_or_404(QuizSubmission,pk=submission_id)
    context={"submission":submission}
    return render(request,'quiz-result.html',context)

def category_view(request):
    query = request.GET.get("q", "")
    if query:
        categories = Category.objects.filter(name__icontains=query)
    else:
        categories = Category.objects.all()

    context = {"categories": categories, "query": query}
    return render(request, 'quiz_category.html', context)

