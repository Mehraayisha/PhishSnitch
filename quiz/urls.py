from django.urls import path
from . import views
urlpatterns =[
  path('all_quiz',views.all_quiz_view,name='all_quiz'),
  path('categories/',views.category_view,name='category_view'),
  path('search/<str:category>',views.search_view,name='search'),
  path('<int:quiz_id>',views.quiz_view,name='quiz'),
  path('<int:submission_id>/result/',views.quiz_result_view,name='quiz_result'),
  

 ]