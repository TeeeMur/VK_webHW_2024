import random
import string
from django.core.management.base import BaseCommand, CommandParser
from vkHWApp.models import *
import time

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if kwargs['fill_count']:
            profiles_count = kwargs['fill_count'][0]
            questions_count = profiles_count * 10
            answers_count = profiles_count * 100
            tags_count = profiles_count
            likes_count = profiles_count * 200

            start_time = time.time()

            profiles_list = [Profile(name=f'profile_{i + 1}') for i in range(profiles_count)]
            Profile.objects.bulk_create(profiles_list)

            print('profiles added')

            tags_list = [Tag(name=f"tag {i + 1}") for i in range(tags_count)]
            Tag.objects.bulk_create(tags_list)

            print('tags added')

            max_profile_id = Profile.objects.count()
            
            questions_list = [Question(name=f'Question_{i + 1}', 
                                       author = Profile.objects.get(pk=random.randint(1, max_profile_id)), 
                                       text=f'text {i}' * (i % 30 + 1)) for i in range(questions_count)]
            Question.objects.bulk_create(questions_list)

            print('questions added')

            tags_objects = list(Tag.objects.all())

            for each_question in list(Question.objects.all()):
                tags = random.sample(tags_objects, random.randint(1, 3))
                for each_tag in tags:
                    each_question.tags.add(each_tag)

            question_objects = list(Question.objects.all())

            answers_list = [Answer(
                reference_question=random.choice(question_objects),
                author=Profile.objects.get(pk=random.randint(1, max_profile_id)),
                text=f'answer {i}' * (i % 25 + 1)) for i in range(answers_count)]

            Answer.objects.bulk_create(answers_list)

            print('answers added')

            answers_like_list = []
            questions_like_list = []

            questions_required_count = int(likes_count * 0.09)

            for each_profile in list(Profile.objects.all()):
                for each_question in list(Question.objects.all()):
                    questions_like_list.append(QuestionLike(author=each_profile, this_question=each_question))
                if len(questions_like_list) >= int(questions_required_count):
                    break

            print('questions likes created')

            for each_profile in list(Profile.objects.all()):
                for each_answer in list(Answer.objects.all()):
                    answers_like_list.append(AnswerLike(author=each_profile, this_answer=each_answer))
                if len(answers_like_list) + len(questions_like_list) >= likes_count:
                    break
            
            print('answers likes created')

            AnswerLike.objects.bulk_create(answers_like_list)
            print('answers likes added')

            QuestionLike.objects.bulk_create(questions_like_list)
            print('questions likes added')
            creation_time = time.time() - start_time
            print(f'time of creation: {creation_time}')

            
    
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'fill_count',
            nargs=1,
            type=int
        )
        return super().add_arguments(parser)
        