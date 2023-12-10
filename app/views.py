from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
import random
from .models import Question, Answer, Tag, Profile
# Create your views here.

def paginate(objects_list,request, per_page=3): #TODO как вернуть текущий номер страницы
    #TODO paginator.num_pages - возвращает сколько ВСЕГО страниц
    try:
        pagenum = request.GET.get('p')
    except:
        pagenum=1
    if (pagenum is None):
        pagenum=1
    try:
        pagenum = int(pagenum)
    except ValueError:
        pagenum = 1
    except NameError:
        pagenum = 1
    if (pagenum<1):
        pagenum=1
    paginator = Paginator(objects_list, per_page)

    return (paginator.page(pagenum),pagenum)


#def hotquestion(request, question_id): # конкр вопрос
#    item = QUESTIONS[question_id]
#    return render(request, 'question.html', {'questions': item})


def mainpage(request):# новые вопросы на mainpage
    q = Question.objects.NewQuestions()
    popt = Tag.objects.Popular()[0:5]
    popprof= Profile.objects.Popular()[0:5]
    print(popprof)
    page_items, pagenum = paginate(q,request)
    page_items = page_items.object_list
    return render(request, 'mainpage.html', {'poptags':popt,'popprof': popprof, 'questions': page_items})
    #TODO передавать номер страницы


def tagpage(request, tag_name):  # hotlist
    q = Question.objects.filter(tags__name=tag_name).order_by('-creation_date')
    popt = Tag.objects.Popular()[0:5]
    popprof = Profile.objects.Popular()[0:5]
    page_items, pagenum = paginate(q,request)
    page_items = page_items.object_list
    return render(request, 'tag.html', {'poptags':popt,'popprof': popprof,'tag': tag_name, 'questions': page_items})
    #TODO передавать номер страницы


def onequest(request,  question_id): # конкр вопрос
    que=Question.objects.filter(id=question_id)
    ans=Answer.objects.filter(question_id=question_id).order_by('-creation_date')
    answ_items, pagenum=paginate(ans, request)
    popt = Tag.objects.Popular()[0:5]
    popprof = Profile.objects.Popular()[0:5]
    return render(request, 'question.html', {'poptags':popt,'popprof': popprof,
                                             'question': que.first(), 'answers': answ_items})
    #TODO передавать номер страницы


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'register.html')

def hotquestions(request):
    # TODO: что делать если за пределами списка вопросов?
    q = Question.objects.HotQuestions()
    popt = Tag.objects.Popular()[0:5]
    popprof = Profile.objects.Popular()[0:5]
    page_items, pagenum = paginate(q, request)
    page_items = page_items.object_list

    return render(request, 'hotquestions.html',{'poptags':popt,'popprof': popprof,
                                             'questions': page_items})

def askquestion(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
