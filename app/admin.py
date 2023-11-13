import django.contrib.admin
from django.contrib import admin

# Register your models here.
from .models import Profile, Question, Answer,  Tag, question_mark_relation, answer_mark_relation, question_tag_relation

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(question_mark_relation)
admin.site.register(answer_mark_relation)
admin.site.register(question_tag_relation)