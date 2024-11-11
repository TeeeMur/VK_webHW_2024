"""
URL configuration for vkProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from vkHWApp import views
from django.urls import path, re_path

urlpatterns = [
    path('', views.index, name='index'),
    path('ask/', views.new_question, name='newQuestion'),
    path('login/', views.login, name="login"),
    path('signup/', views.sign_up, name='signUp'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('settings/', views.settings, name='settings'),
    path('tag/<str:tag>/', views.tag_view, name='tagView'),
    path('hot/', views.hot_questions, name='hotQuestions'),
]
