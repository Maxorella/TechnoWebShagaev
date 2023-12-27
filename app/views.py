from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Question, Answer, Tag, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ProfileRegistrationForm, UpdateProfileForm, UpdateUserForm, QuestionForm, AnswerForm
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

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


@login_required
def onequest(request, question_id):  # конкр вопрос
    que = Question.objects.question_rating(question_id=question_id)
    ans = Answer.objects.answer_rating(question_id=question_id).order_by('-creation_date')
    answ_items, pagenum, total_pages, pag_range  = paginate(ans, request, 2000)
    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]

    if request.method == 'POST':
        form = AnswerForm(que.first(),request.POST)
        if form.is_valid():
            # Save the question to the database
            answer = form.save(commit=False)
            # Set the author to the currently logged-in user
            answer.author = request.user.profile  # Assuming user has a profile linked
            answer.save()
            # Redirect to the question detail page or any other desired page
            return redirect('onequestion', question_id=question_id)
    else:
        form = AnswerForm(que)

    return render(request, 'question.html', {'poptags': popt, 'popprof': popprof,
                                             'question': que.first(), 'answers': answ_items, 'form': form})

def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Get the referring URL from the session
                next_url = request.session.get('continue', None)
                # Clear the referring URL from the session
                request.session.pop('continue', None)
                # Redirect to the referring URL or a default page
                return redirect(next_url) if next_url else redirect(reverse('mainpage'))

    else:
        form = AuthenticationForm()
        request.session['continue'] = request.GET.get('continue')
    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    return render(request, 'login.html', {'poptags': popt, 'popprof': popprof, 'form': form})
    # TODO continue param

def signup(request):
    if request.method == 'POST':
        form = ProfileRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a profile for the user
            #Profile.objects.create(user=user)
            return redirect(reverse('log_in'))  # Change 'home' to the actual URL name for your home page
    else:
        form = ProfileRegistrationForm()

    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    return render(request, 'register.html', {'poptags': popt, 'popprof': popprof, 'form': form})


def hotquestions(request):
    q = Question.objects.hot_questions()
    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    page_items, pagenum, total_pages, pag_range = paginate(q, request)
    return render(request, 'hotquestions.html', {'poptags': popt, 'popprof': popprof,
                                                 'questions': page_items.object_list, 'page_items': page_items, 'current_page': pagenum, 'total_pages': total_pages, 'page_range': pag_range})

def log_out(request):
    logout(request)
    return redirect(reverse('mainpage'))  # Замените 'home' на URL вашей домашней страницы

@login_required
def askquestion(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Save the question to the database
            question = form.save(commit=False)
            # Set the author to the currently logged-in user
            question.author = request.user.profile  # Assuming user has a profile linked
            question.save()
            # Redirect to the question detail page or any other desired page
            return redirect('onequestion', question_id=question.id)
    else:
        form = QuestionForm()



    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    return render(request, 'ask.html', {'poptags': popt, 'popprof': popprof, 'form': form})


@login_required
def settings(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('settings')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    popt = Tag.objects.popular()[0:5]
    popprof = Profile.objects.popular()[0:5]
    return render(request, 'settings.html',{'poptags': popt, 'popprof': popprof, 'user_form': user_form, 'profile_form': profile_form})
