
from django.core.management import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
import random
from app.models import Profile, Question, Answer,  Tag, LikeQuestion, LikeAnswer
fake = Faker()#.name()

class Command(BaseCommand):
    #  def __init__(self, ratio):
    #     self.ratio = ratio #кол-во заполнений
    help = "Fills database with fake data" # информация о команде


    def add_arguments(self, parser): # добавляет переменную ratio
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **kwargs): # сама обработка команды
        num = kwargs['ratio'] #взять количество данных

        users =[
            User.objects.create_user(
                username=fake.unique.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password=fake.password(),  # Замените 'your_password_here' на желаемый пароль
                date_joined=fake.date_between(start_date='-10y', end_date='-1d')
            ) for i in range(num)
        ]

       # user_l = User.objects.bulk_create(users)




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
                text =  fake.sentence(nb_words=20),
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
                questions[i].tags.add(tagtoad)



        likes_quest=[]
        count=0
        for prof in profiles:
            checker = list()
            for i in range(0,100,1):
                ques_n=random.choice(questions)
                if  not (ques_n in checker):
                    likes_quest.append(LikeQuestion(profile=prof, question=ques_n, like=fake.pybool()))
                    checker.append(ques_n)


        likes_question_l = LikeQuestion.objects.bulk_create(likes_quest)

        answers = [
            Answer(
                author = random.choice(profiles), question = random.choice(questions),
                title = fake.paragraph(nb_sentences=2), text =  fake.sentence(nb_words=20),
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
                answers[i].tags.add(tagtoad)




        likes_answ = []
        count = 0
        for prof in profiles:
            checker = list()
            for i in range(0, 100, 1):
                answ_n = random.choice(answers)
                if not (answ_n in checker):
                    likes_answ.append(LikeAnswer(profile=prof, answer=answ_n, like=fake.pybool()))
                    checker.append(answ_n)







        likes_answer_l = LikeAnswer.objects.bulk_create(likes_answ)


