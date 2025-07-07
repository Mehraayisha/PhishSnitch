from django.db import models
import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import Sum
from accounts.models import Profile

class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='category_images',null=True,blank=True,default='bg3.png')
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Quiz(models.Model):
    MODE_CHOICES = [
        ('PRACTICE', 'Practice (MCQ)'),
        ('TIMED', 'Timed (MCQ)'),
        ('TF', 'True/False'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    quiz_file = models.FileField(upload_to='quiz/')
    created_at = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='PRACTICE')
    
    uploaded_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title


class Question(models.Model):
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.text[:50]}, {self.text[:20]}"
    


@receiver(post_save, sender=Quiz)#call this function everytime a sender(Quiz) object is created
def import_quiz_after_save(sender, instance, created, **kwargs):
    if instance.quiz_file:
        try:
            df = pd.read_excel(instance.quiz_file.path)
            df.columns = df.columns.str.strip()#remove the whitespace in begining and end of all the columns in df

            for _, row in df.iterrows():#_ is used to ignore the index(iterrow returns index and row value)
                question_text = row['Question']
                correct_answer = str(row['Answer']).strip().upper()

                question, _ = Question.objects.get_or_create(
                    quiz=instance,
                    text=question_text
                )

                # Remove old choices to avoid duplicates
                Choice.objects.filter(question=question).delete()

                # TF Mode
                if instance.mode == 'TF':
                    Choice.objects.create(question=question, text=row['A'], is_correct=correct_answer == 'A')
                    Choice.objects.create(question=question, text=row['B'], is_correct=correct_answer == 'B')

                # MCQ Modes (practice or timed)
                else:
                    Choice.objects.create(question=question, text=row['A'], is_correct=correct_answer == 'A')
                    Choice.objects.create(question=question, text=row['B'], is_correct=correct_answer == 'B')
                    Choice.objects.create(question=question, text=row['C'], is_correct=correct_answer == 'C')
                    Choice.objects.create(question=question, text=row['D'], is_correct=correct_answer == 'D')

        except Exception as e:
            print("Error while importing quiz:", e)

    if instance.quiz_file:
        try:
            #  print("Importing questions from Excel...")
            df = pd.read_excel(instance.quiz_file.path)
            df.columns = df.columns.str.strip()  # Strip any spaces

            for _, row in df.iterrows():
                question_text = row['Question']
                choice1 = row['A']
                choice2 = row['B']
                choice3 = row['C']
                choice4 = row['D']
                correct_answer = str(row['Answer']).strip().upper()

                question, _ = Question.objects.get_or_create(quiz=instance, text=question_text)

                Choice.objects.get_or_create(question=question, text=choice1, is_correct=correct_answer == 'A')
                Choice.objects.get_or_create(question=question, text=choice2, is_correct=correct_answer == 'B')
                Choice.objects.get_or_create(question=question, text=choice3, is_correct=correct_answer == 'C')
                Choice.objects.get_or_create(question=question, text=choice4, is_correct=correct_answer == 'D')

        except Exception as e:
            print("Error while importing quiz:", e)



class QuizSubmission(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    score=models.IntegerField()
    submitted_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user},{self.quiz.title}"
    

    
class UserRank(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    rank=models.IntegerField(null=True,blank=True)
    total_score=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return f"{self.rank},{self.user.username}"
@receiver(post_save, sender=QuizSubmission)   
def updated_leaderboard(sender,instance,created,**kwargs):
     if created:
         update_leaderboard() 





def update_leaderboard():
    user_scores = (
        QuizSubmission.objects
        .values('user')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score')
    )

    rank = 1
    for entry in user_scores:
        user_id = entry['user']
        total_score = entry['total_score']

        profile, created = Profile.objects.get_or_create(user_id=user_id)
        profile.total_score = total_score
        profile.rank = rank
        profile.save()

        rank += 1

    
    
    
