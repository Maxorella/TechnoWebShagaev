from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    avatar = models.CharField(max_length=50, null=True, blank=True)  # хранит путь до аватарки
    is_deleted = models.BooleanField(default=False)

class Message(models.Model):
    author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)#если удалён то null(а вообще по is_deleted лучше смотреть)
    answer_id = models.IntegerField(null=True, blank=True)#если NULL - то это вопрос, если есть id - то ответ
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=300)
    mark_count = models.IntegerField()  # TODO
    is_deleted = models.BooleanField(default=False)

class Tag(models.Model):
    name = models.CharField(max_length=30)


class message_mark_relation(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    mark = models.BooleanField(null=True, blank=True) # если null пользователь отменил отметку(остался нейтральным)

class question_tag_relation(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.SET_NULL, null=True)
