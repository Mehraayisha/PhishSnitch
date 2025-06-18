from django.urls import path
from . import views
urlpatterns =[
  path('',views.home,name='home'),
  path('leaderboard',views.leaderboaard_view,name='leaderboard'),
  path('dashboard',views.dashborad_view,name='dashboard'),
  path('about',views.about_view,name='about'),
  path('blogs',views.blogs_view,name='blogs'),
  path('downloads',views.downloads_view,name='downloads'),
  path('terms_and_conditions',views.terms_conditions_view,name='terms_and_conditions'),
  path('contact',views.contact_view,name='contact'),
  path('blogs/<str:blog_id>',views.blog_view,name='blog')
 ]