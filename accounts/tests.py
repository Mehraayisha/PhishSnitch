from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from quiz.models import QuizSubmission,Quiz,Category
from django.urls import reverse
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

       url=reverse('profile',args=[self.user.username])
       response=self.client.get(url)

       self.assertEqual(response.status_code,200)
       self.assertTemplateUsed(response,'profile.html')
       self.assertEqual(response.context['user_profile2'],self.profile)
       self.assertIn(self.submission,response.context['submissions'])
    def test_profile_view_redirect(self):
       url=reverse('profile',args=[self.user.username])
       response=self.client.get(url)
       self.assertRedirects(response,f'/user/login?next={url}')


