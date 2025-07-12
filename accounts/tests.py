from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from quiz.models import QuizSubmission,Quiz,Category

# Create your tests here.
class profileViewTest(TestCase):
    def setUp(self):
     self.user=User.objects.create_user(username='testuser',password="password")
     self.profile=Profile.objects.create(user=self.user,bio="this is bio")
     self.category=Category.objects.create(name="science")
     self.quiz=Quiz.objects.create(
        title="Quiz title",
        description="desc",
        category=self.category,
     )
     self.submission=QuizSubmission.objects.create(user=self.user,quiz=self.quiz,score=7)
    def test_profile_view(self):
       self.client.login(username='testuser',password='password')
       