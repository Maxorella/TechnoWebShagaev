from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question, Answer, Tag, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def paginate(objects_list, request, per_page=3, adjacent_pages=2):  # TODO как вернуть текущий номер страницы
    # TODO paginator.num_pages - возвращает сколько ВСЕГО страниц
    paginator = Paginator(objects_list, per_page)

    page_num = int(request.GET.get('p', 1))

    try:
        page_items = paginator.page(page_num)
    except PageNotAnInteger:
        page_items = paginator.page(1)
        page_num = 1
    except EmptyPage:
        page_items = paginator.page(paginator.num_pages)
        page_num = paginator.num_pages
    total_pages = paginator.num_pages
    start_page = max(page_num - adjacent_pages, 1)
    end_page = min(page_num + adjacent_pages, total_pages)
    rang = range(start_page, end_page + 1)
    return (page_items, page_num, total_pages, rang)


# def hotquestion(request, question_id): # конкр вопрос
#    item = QUESTIONS[question_id]
#    return render(request, 'question.html', {'questions': item})


def mainpage(request):  # новые вопросы на mainpage
    q = Question.objects.NewQuestions()
    popt = Tag.objects.Popular()[0:5]
    popprof = Profile.objects.Popular()[0:5]
    page_items, pagenum, total_pages, pag_range = paginate(q, request)
    return render(request, 'mainpage.html',
                  {'poptags': popt, 'popprof': popprof, 'questions': page_items.object_list,
                   'page_items': page_items, 'current_page': pagenum, 'total_pages': total_pages, 'page_range': pag_range})
    # TODO передавать номер страницы


def tagpage(request, tag_name):  # hotlist
    q = Question.objects.filter(tags__name=tag_name).order_by('-creation_date')
    popt = Tag.objects.Popular()[0:5]
    popprof = Profile.objects.Popular()[0:5]
    page_items, pagenum, total_pages, pag_range = paginate(q, request)
    return render(request, 'tag.html', {'poptags': popt, 'popprof': popprof, 'tag': tag_name,
                                                 'questions': page_items.object_list, 'page_items': page_items,
                                                 'current_page': pagenum, 'total_pages': total_pages,
                                                 'page_range': pag_range})

    # TODO передавать номер страницы


def onequest(request, question_id):  # конкр вопрос
    que = Question.objects.filter(id=question_id)
    ans = Answer.objects.filter(question_id=question_id).order_by('-creation_date')
    answ_items, pagenum = paginate(ans, request)
    popt = Tag.objects.Popular()[0:5]
    popprof = Profile.objects.Popular()[0:5]
    return render(request, 'question.html', {'poptags': popt, 'popprof': popprof,
                                             'question': que.first(), 'answers': answ_items})
    # TODO передавать номер страницы


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'register.html')


def hotquestions(request):
    q = Question.objects.HotQuestions()
    popt = Tag.objects.Popular()[0:5]
    popprof = Profile.objects.Popular()[0:5]
    page_items, pagenum, total_pages, pag_range = paginate(q, request)
    return render(request, 'hotquestions.html', {'poptags': popt, 'popprof': popprof,
                                                 'questions': page_items.object_list, 'page_items': page_items, 'current_page': pagenum, 'total_pages': total_pages, 'page_range': pag_range})


def askquestion(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
