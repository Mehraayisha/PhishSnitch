from django.contrib import admin
from .models import Quiz,Category,Question,Choice
# Register your models here.
admin.site.register(Quiz)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Choice)


