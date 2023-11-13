from django.db import models
from django.contrib.auth.models import User
class MyQuerySet(models.QuerySet):
    def published(self):
        return self.filter(tags_name='Movies') # пример
    pass
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    avatar = models.CharField(max_length=50, null=True, blank=True)  # хранит путь до аватарки
    registration_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.username}'

class Question(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)  # если удалён то null(а вообще по is_deleted лучше смотреть)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=300)
    mark_count = models.IntegerField()  # TODO
    creation_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

class Answer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)  #если удалён то null(а вообще по is_deleted лучше смотреть)
    question = models.OneToOneField('Question', null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=300)
    mark_count = models.IntegerField()  # TODO
    creation_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

class Tag(models.Model):
    name = models.CharField(max_length=30)


class question_mark_relation(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    mark = models.BooleanField(null=True, blank=True) # если null пользователь отменил отметку(остался нейтральным)

class answer_mark_relation(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    mark = models.IntegerField() # если 0 пользователь отменил отметку(остался нейтральным)

class question_tag_relation(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True)
