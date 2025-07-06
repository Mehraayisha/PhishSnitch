from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message
# Create your tests here.
class MessageModelTest(TestCase):
     def setUp(self):
          self.user=User.objects.create_user(username='testuser',password='testpass')
          self.message=Message.objects.create(
               user=self.user,
               subject='Message subject',
               message='this is my message'
          )
          
     def test_message_creation(self):
          #test if equal
          self.assertEqual(self.message.user,self.user)
          self.assertEqual(self.message.subject,'Message subject')
          self.assertEqual(self.message.message,'this is my message')
          
          #test if false
          self.assertFalse(self.message.is_read)
          #test if not none
          self.assertIsNotNone(self.message.created_at)