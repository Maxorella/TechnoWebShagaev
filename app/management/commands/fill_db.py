
from django.core.management import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
import random
from app.models import Profile, Question, Answer,  Tag
fake = Faker()#.name()

class Command(BaseCommand):
    #  def __init__(self, ratio):
    #     self.ratio = ratio #кол-во заполнений
    help = "Fills database with fake data" # информация о команде


    def add_arguments(self, parser): # добавляет переменную ratio
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **kwargs): # сама обработка команды
        num = kwargs['ratio'] #взять количество данных
        print()
        #num = 10
        #$for i in range(num):

        #  for _ in range(5):
        ###TODO пароль не заполняется?
        users = [
            User(
                username=fake.unique.user_name(), first_name=fake.first_name(),
                last_name=fake.last_name(), email=fake.email(), password=fake.password(),
                date_joined =fake.date_between(start_date='-10y',end_date='-1d')
            ) for i in range(num)
        ]

        user_l = User.objects.bulk_create(users)

        profiles = [
            Profile(
                user = users[i], avatar = f'/static/img/{users[i].username}',
                is_deleted=False
            ) for i in range(num)
        ]

        profiles_l = Profile.objects.bulk_create(profiles)


        tagss = [
            Tag(
                name = fake.word()
            ) for i in range(num)
        ]
        tags_l = Tag.objects.bulk_create(tagss)


        # variable_nb_sentences to False сделает чётко 2 предложения
        questions = [
            Question(
                author=random.choice(profiles), title = fake.paragraph(nb_sentences=2),
                text =  fake.sentence(nb_words=20), rating=0,
                creation_date = fake.date_between(start_date='-10y',end_date='-1d'),
                is_deleted = False
            )for i in range(10*num)
        ]

        questions_l = Question.objects.bulk_create(questions)


        for i in range(10*num): # добавление тэгов к вопросу
            profl=[]
            tagl=[]
            for j in range(4):
                tagtoad=random.choice(tagss)
                if tagtoad in tagl:
                    continue
                tagl.append(tagtoad)
                questions_l[i].tags.add(tagtoad)

            #лайки к вопросу
            rating=0
            for j in range(random.randint(3,10)): #лайки
                toad=random.choice(profiles)
                if toad in profl:
                    continue
                if random.randint(0,1):
                    questions_l[i].liked.add(toad)
                    rating+=1
                else:
                    questions_l[i].disliked.add(toad)
                    rating-=1
                profl.append(toad)
            questions_l[i].rating = rating

        for q in questions_l:
            q.save()

        answers = [
            Answer(
                author = random.choice(profiles), question = random.choice(questions),
                title = fake.paragraph(nb_sentences=2), text =  fake.sentence(nb_words=20), rating=0,
                creation_date = fake.date_between(start_date='-10y', end_date='-1d'),
                correct = fake.pybool(), is_deleted=False
            ) for i in range(100*num)
        ]

        answers_l = Answer.objects.bulk_create(answers)

        for i in range(100*num): # добавление тэгов к ответу
            profl=[]
            tagl=[]
            for j in range(4):
                tagtoad=random.choice(tagss)
                if tagtoad in tagl:
                    continue
                tagl.append(tagtoad)
                answers_l[i].tags.add(tagtoad)
            rating=0
            #лайки к вопросу
            for j in range(random.randint(3,10)): #лайки
                toad=random.choice(profiles)
                if toad in profl:
                    continue
                if random.randint(0,1):
                    answers_l[i].liked.add(toad)
                    rating+=1
                else:
                    answers_l[i].disliked.add(toad)
                    rating-=1
                profl.append(toad)
            answers_l[i].rating = rating

        for a in answers_l:
            a.save()


