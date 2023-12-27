from django import forms
from django.contrib.auth.forms import UserCreationForm,  UserChangeForm
from django.contrib.auth.models import User
from .models import Profile, Question, Answer, Tag

"""
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        # Проверка минимальной длины имени пользователя
        if len(username) < 6:
            raise forms.ValidationError('Имя пользователя должно быть не менее 6 символов.')
        # Проверка уникальности имени пользователя
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        # Проверка минимальной длины адреса электронной почты
        if len(email) < 8:
            raise forms.ValidationError('Адрес электронной почты должен быть не менее 8 символов.')
        # Проверка, что адрес электронной почты содержит символ "@"
        if '@' not in email:
            raise forms.ValidationError('Адрес электронной почты должен содержать символ "@".')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        # Проверка минимальной длины пароля
        if len(password1) < 9:
            raise forms.ValidationError('Пароль должен быть не менее 9 символов.')
        # Проверка, что пароль содержит хотя бы одну цифру
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError('Пароль должен содержать хотя бы одну цифру.')
        return password1

    def clean(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()
        # Проверка совпадения паролей
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        return cleaned_data

"""

class ProfileRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        #user.email = self.cleaned_data['email']

        if commit:
            user.save()

        profile = Profile.objects.create(user=user, avatar=self.cleaned_data['avatar'])

        return user
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']


class TagInput(forms.TextInput):
    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        return value.strip()

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(widget=TagInput, required=False)

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        raw_tags = self.cleaned_data.get('tags', '')
        tag_names = [tag.strip() for tag in raw_tags.split(',') if tag.strip()]

        # Create new tags individually if they don't exist
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)

        return tags

    def save(self, commit=True):
        instance = super(QuestionForm, self).save(commit=False)
        instance.save()

        # Set the tags for the question
        instance.tags.clear()
        for tag in self.cleaned_data['tags']:
            instance.tags.add(tag)

        if commit:
            instance.save()

        return instance
class AnswerForm(forms.ModelForm):
    tags = forms.CharField(widget=TagInput, required=False)

    class Meta:
        model = Answer
        fields = ['title', 'text', 'tags']

    def __init__(self, question=None, *args, **kwargs):
        # Pass the question instance to the form
        self.question = question
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        raw_tags = self.cleaned_data.get('tags', '')
        tag_names = [tag.strip() for tag in raw_tags.split(',') if tag.strip()]

        # Create new tags individually if they don't exist
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)

        return tags

    def save(self, commit=True):
        instance = super(AnswerForm, self).save(commit=False)

        # Set the question for the answer
        instance.question = self.question

        instance.save()

        # Set the tags for the answer
        instance.tags.clear()
        for tag in self.cleaned_data['tags']:
            instance.tags.add(tag)

        if commit:
            instance.save()

        return instance