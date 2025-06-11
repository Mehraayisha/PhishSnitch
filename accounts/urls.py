from django.urls import path
from . import views
urlpatterns = [
  path('register',views.register,name='register'),
  path('profile/<str:username>',views.userprofile,name='profile'),
  path('login',views.login,name='login'),
  path('logout',views.logout,name='logout'),
  path('settings',views.editprofile,name='edit_profile'),
  path('delete',views.deleteprofile,name='delete_profile'),
 ]