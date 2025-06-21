from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message
# Create your tests here.
class MessageModelTest(TestCase):
     def setUp(self):
          self.user=User.objcts.create_user(username='testuser',password='testpass')
          self.message=Message.objects.create(
               user=self.user,
               subject='Message subject',
               message='this is my message'
          )