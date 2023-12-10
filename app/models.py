from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class MyQuerySet(models.QuerySet):
    def published(self):
        return self.filter(tags_name='Movies') # пример
    pass


class QuestionManager(models.Manager):
    def HotQuestions(self):
        return  self.order_by('-rating') #первыми идут самые популярные
        #self.filter(quest_profiles_liked)
    def NewQuestions(self):
        return  self.order_by('-creation_date')

    def Bytag(self, tag_name):
        return  self.filter(tags__name=tag_name).order_by('rating')

class TagManager(models.Manager):
    def Popular(self):
        return self.annotate(question_count=Count('question'),
                             answer_count=Count('answer')).order_by('-question_count', '-answer_count')

class ProfileManager(models.Manager):
    def Popular(self):
        return self.annotate(question_count=Count('question'),
                             answer_count=Count('answer')).order_by('-question_count', '-answer_count')

class AnswerManager(models.Manager):
    def ByDate(self):
        return self.order_by('-creation_date')

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #email = models.CharField(max_length=40)
    #real_name = models.CharField(max_length=30)
    avatar = models.CharField(max_length=50, null=True, blank=True)  # хранит путь до аватарки
    is_deleted = models.BooleanField(default=False)
    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username}'

class Question(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)  # если удалён то null(а вообще по is_deleted лучше смотреть)
    tags = models.ManyToManyField('Tag')
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=300)
    liked = models.ManyToManyField('Profile', related_name='quest_profiles_liked')
    disliked = models.ManyToManyField('Profile', related_name='quest_profiles_disliked')
    rating = models.IntegerField()
    creation_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    objects = QuestionManager()

    def __str__(self):
        return f'{self.title}'
class Answer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)  #если удалён то null(а вообще по is_deleted лучше смотреть)
    question = models.ForeignKey('Question', null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag')
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=300)
    liked = models.ManyToManyField('Profile', related_name='answ_profiles_liked')
    disliked = models.ManyToManyField('Profile',related_name='answ_profiles_disliked')
    rating = models.IntegerField()
    creation_date = models.DateTimeField()
    correct = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    objects = AnswerManager()

    def __str__(self):
        return f'{self.title}'
class Tag(models.Model):
    name = models.CharField(max_length=30)
    objects = TagManager()

    def __str__(self):
        return f'{self.name}'

