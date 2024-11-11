from vkHWApp import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('ask/', views.new_question, name='newQuestion'),
    path('login/', views.login, name="login"),
    path('signup/', views.sign_up, name='signUp'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('settings/', views.settings, name='settings'),
    path('tag/<str:tag>/', views.tag_view, name='tagView'),
    path('hot/', views.hot_questions, name='hotQuestions'),
    path('admin/', admin.site.urls),
]
