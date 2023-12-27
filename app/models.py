from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone  # Import timezone module


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.annotate(
            rating=Count('likequestion__like', filter=Q(likequestion__like=True)) -
                   Count('likequestion__like', filter=Q(likequestion__like=False))
        ).order_by('-creation_date')

    def by_tag(self, tag_name):
        return self.filter(tags__name=tag_name).annotate(
            rating=Count('likequestion__like', filter=Q(likequestion__like=True)) -
                   Count('likequestion__like', filter=Q(likequestion__like=False))
        ).order_by('-creation_date')

    def hot_questions(self):
        return self.annotate(
            rating=Count('likequestion__like', filter=Q(likequestion__like=True)) -
                   Count('likequestion__like', filter=Q(likequestion__like=False))
        ).order_by('-rating')
    def question_rating(self, question_id):
        return self.filter(pk=question_id).annotate(
            rating=Count('likequestion__like', filter=Q(likequestion__like=True)) -
                   Count('likequestion__like', filter=Q(likequestion__like=False))
        )


class TagManager(models.Manager):
    def popular(self):
        return self.annotate(question_count=Count('question'),
                             answer_count=Count('answer')).order_by('-question_count', '-answer_count')


class ProfileManager(models.Manager):
    def popular(self):
        return self.annotate(question_count=Count('question'),
                             answer_count=Count('answer')).order_by('-question_count', '-answer_count')




class AnswerManager(models.Manager):
    def by_date(self, question_id):
        return self.filter(question_id).order_by('-creation_date')


    def answer_rating(self, question_id):
        return self.filter(question_id=question_id).annotate(
            rating=Count('likeanswer__like', filter=Q(likeanswer__like=True)) -
                   Count('likeanswer__like', filter=Q(likeanswer__like=False))
        ).order_by('-creation_date')

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, unique=True)
    avatar = models.ImageField(upload_to='static/img/', null=True, blank=True)  # хранит путь до аватарки
    #is_deleted = models.BooleanField(default=False)
    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username}'


class Question(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)  # если удалён то null(по is_deleted лучше смотреть)
    tags = models.ManyToManyField('Tag')
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    creation_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    is_correct = models.BooleanField(default=False)
    objects = QuestionManager()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'
class Answer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)  #если удалён то null(по is_deleted лучше смотреть)
    question = models.ForeignKey('Question', null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag')
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    creation_date = models.DateTimeField()
    correct = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    objects = AnswerManager()
    def __str__(self):
        return f'{self.title}'
    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = timezone.now()
        super().save(*args, **kwargs)

class LikeQuestion(models.Model):
    like = models.BooleanField(null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

class LikeAnswer(models.Model):
    like = models.BooleanField(null=True)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    objects = TagManager()

    def __str__(self):
        return f'{self.name}'

