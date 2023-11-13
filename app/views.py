from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
import random

# Create your views here.
QUESTIONS = [
    {
        'id': i,
        'title': f'Question{i}',
        'content': f'Lorem ispum {i}'
    } for i in range(20)
]

ANSWERS = [
    {
        'id': i,
        'title': f'Answer{i}',
        'content': f'Lorem ispum {i}'
    } for i in range(20)
]
def paginate(objects, page, per_page=15):

    if (page is None):
        page=1

    try:
        page = int(page)
    except ValueError:
        page = 1
    except NameError:
        page = 1
    if (page<1):
        page=1

    if ((page*per_page-per_page) > len(QUESTIONS)):
        page=1 #TODO: что делать если за пределами списка вопросов?


    paginator = Paginator(objects, per_page)
    return paginator.page(page)


#def hotquestion(request, question_id): # конкр вопрос
#    item = QUESTIONS[question_id]
#    return render(request, 'question.html', {'questions': item})


def mainpage(request):# новые вопросы на mainpage
    pagenum = request.GET.get('pagenum')
    per_page = 3
    page_items = paginate(QUESTIONS,pagenum,per_page).object_list

    return render(request, 'mainpage.html', {'questions': page_items, 'p1':pagenum})


def tagpage(request, tag_name):  # hotlist
    pagenum = request.GET.get('pagenum')
    per_page=3
    page_items = paginate(QUESTIONS, pagenum, per_page).object_list
    return render(request, 'tag.html', {'tag': tag_name, 'questions': page_items})


def onequest(request,  question_id): # конкр вопрос
    item = QUESTIONS[question_id]
    answer_n = random.randint(0,len(ANSWERS))
    answ_items = ANSWERS[answer_n:answer_n+2] #TODO сделать выборку с базы
    return render(request, 'question.html', {'question': item, 'answers': answ_items})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'register.html')

def hotquestions(request):
    pagenum = int(request.GET.get('pagenum'))
    per_page = 3
    if ((pagenum * per_page - per_page) > len(QUESTIONS)):
        pagenum = 1  # TODO: что делать если за пределами списка вопросов?
    page_items = paginate(QUESTIONS, pagenum, per_page).object_list
    return render(request, 'hotquestions.html',{'questions': page_items})

def askquestion(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
