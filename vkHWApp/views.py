from django.shortcuts import render
from django.contrib import admin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *

popular_tags = Tag.objects.get_ten_popular_tags()

def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    try:
        page_to_return = paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(1)
    return page_to_return


def index(request):
    questions = paginate(Question.objects.get_new_questions(), request.GET.get('page', 1))
    return render(request, "index.html",
                  {'questions': questions, 'popular_tags': popular_tags})


def question(request, question_id):
    try:
        this_question = Question.objects.get_question_by_id(question_id)
    except Question.DoesNotExist as e:
        return handler404(request)
    answers = Answer.objects.get_answers_to_question(question_id)
    return render(request, 'oneQuestionAndAnswers.html', {'question': this_question, 'answers': answers, 'popular_tags': popular_tags})


def new_question(request):
    return render(request, 'newQuestion.html')


def sign_up(request):
    return render(request, 'registration.html')


def login(request):
    return render(request, 'login.html')


def settings(request):
    return render(request, 'settings.html')


def tag_view(request, tag):
    try:
        questions_by_tag = Question.objects.get_questions_by_tag(tag)
    except Question.DoesNotExist as e:
        return handler404(request)
    questions = paginate(questions_by_tag, request.GET.get('page', 1))
    return render(request, 'tagQuestions.html',{'questions': questions, 'tag': tag, 'popular_tags': popular_tags})


def hot_questions(request):
    questions = paginate(Question.objects.get_hot_questions(), request.GET.get('page', 1))
    return render(request, 'hotQuestions.html',
                  {'questions': questions, 'popular_tags': popular_tags})


def handler404(request):
    return render(request, '404.html', {'popular_tags': popular_tags}, status=404)
