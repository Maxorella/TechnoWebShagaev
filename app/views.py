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
    q = Question.objects.new_questions()
    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    page_items, pagenum, total_pages, pag_range = paginate(q, request)
    return render(request, 'mainpage.html',
                  {'poptags': popt, 'popprof': popprof, 'questions': page_items.object_list,
                   'page_items': page_items, 'current_page': pagenum, 'total_pages': total_pages, 'page_range': pag_range})
    # TODO передавать номер страницы


def tagpage(request, tag_name):  # hotlist
    q = Question.objects.by_tag(tag_name)
    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    page_items, pagenum, total_pages, pag_range = paginate(q, request)
    return render(request, 'tag.html', {'poptags': popt, 'popprof': popprof, 'tag': tag_name,
                                                 'questions': page_items.object_list, 'page_items': page_items,
                                                 'current_page': pagenum, 'total_pages': total_pages,
                                                 'page_range': pag_range})

    # TODO передавать номер страницы


def onequest(request, question_id):  # конкр вопрос
    que = Question.objects.question_rating(question_id=question_id)
    ans = Answer.objects.answer_rating(question_id=question_id).order_by('-creation_date')
    answ_items, pagenum, total_pages, pag_range  = paginate(ans, request, 2000)
    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    #answ_items, pagenum, total_pages, pag_range = paginate(ans, request)
    return render(request, 'question.html', {'poptags': popt, 'popprof': popprof,
                                             'question': que.first(), 'answers': answ_items})
    # TODO передавать номер страницы


def login(request):
    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    return render(request, 'login.html', {'poptags': popt, 'popprof': popprof})


def signup(request):
    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    return render(request, 'register.html', {'poptags': popt, 'popprof': popprof})


def hotquestions(request):
    q = Question.objects.hot_questions()
    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    page_items, pagenum, total_pages, pag_range = paginate(q, request)
    return render(request, 'hotquestions.html', {'poptags': popt, 'popprof': popprof,
                                                 'questions': page_items.object_list, 'page_items': page_items, 'current_page': pagenum, 'total_pages': total_pages, 'page_range': pag_range})


def askquestion(request):
    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    return render(request, 'ask.html', {'poptags': popt, 'popprof': popprof})


def settings(request):
    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    return render(request, 'settings.html',{'poptags': popt, 'popprof': popprof})
