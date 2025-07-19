from django.urls import path
from django.conf.urls import handler404
from . import views
handler=views.custom_404
urlpatterns =[
  path('',views.home,name='home'),
  path('leaderboard',views.leaderboaard_view,name='leaderboard'),
  path('dashboard',views.dashborad_view,name='dashboard'),
  path('message/<int:id>',views.message_view,name='message'),
  path('about',views.about_view,name='about'),
  path('blogs',views.blogs_view,name='blogs'),
  path('downloads',views.downloads_view,name='downloads'),
  path('search/users',views.search_users_view,name='search_users'),
  path('terms_and_conditions',views.terms_conditions_view,name='terms_and_conditions'),
  path('contact',views.contact_view,name='contact'),
  path('blogs/<str:blog_id>',views.blog_view,name='blogs'),
  path('breachchecker',views.breach_checker,name='breach_checker'),
  path('cyber-news/', views.cyber_news_view, name='cyber-news'),
 ]