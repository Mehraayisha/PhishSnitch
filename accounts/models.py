from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,null=True,verbose_name='User_Object')
    # email_address=models.CharField(max_length=55,unique=True,verbose_name='User_Email')
    bio=models.TextField(blank=True,null=True)
    profile_image=models.ImageField(upload_to='profile_images',default='userdefault.png',blank=True,null=True,verbose_name='Profile_Pic')
    location=models.CharField(max_length=100,blank=True,null=True)
    GENDER=(
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    )
    gender=models.CharField(max_length=6,choices=GENDER,blank=True,null=True)
    rank=models.IntegerField(null=True,blank=True,editable=True,default=0)
    total_score = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}" 