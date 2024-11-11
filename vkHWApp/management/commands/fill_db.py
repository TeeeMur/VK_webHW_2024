import random
import string
from django.core.management.base import BaseCommand, CommandParser
from vkHWApp.models import *

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if kwargs['fill_count']:
            profiles_count = kwargs['fill_count'][0]
            questions_count = profiles_count * 10
            answers_count = profiles_count * 100
            tags_count = profiles_count
            likes_count = profiles_count * 200
            profiles_list = [Profile(name=f'profile_{i + 1}') for i in range(profiles_count)]
            Profile.objects.bulk_create(profiles_list)
            tags_list = [Tag(name=f"tag {i + 1}") for i in range(tags_count)]
            Tag.objects.bulk_create(tags_list)
            questions_list = [Question(name=f'Question_{i + 1}', 
                                       author = random.choice(Profile.objects.all()), 
                                       text=''.join(random.choices(string.ascii_letters,
                                        k=random.randint(0, 400)))) for i in range(questions_count)]
            Question.objects.bulk_create(questions_list)
            tags_objects = list(Tag.objects.all())
            for each_question in Question.objects.all():
                tags = random.sample(tags_objects, random.randint(1, 3))
                for each_tag in tags:
                    each_question.tags.add(each_tag)
            answers_list = [Answer(
                reference_question=random.choice(Question.objects.all()),
                author=random.choice(Profile.objects.all()),
                text=''.join(random.choices(string.ascii_letters,
                                        k=random.randint(0, 100)))
            ) for i in range(answers_count)]
            Answer.objects.bulk_create(answers_list)
            answers_like_pairs = [[each_profile, list()] for each_profile in Profile.objects.all()]
            questions_like_pairs = [[each_profile, list()] for each_profile in Profile.objects.all()]
            answers = list(Answer.objects.all())
            questions = list(Question.objects.all())
            for each_pair in range(len(answers_like_pairs)):
                this_answers = random.sample(answers, random.randint(1, len(answers)//4))
                answers_like_pairs[each_pair][1].extend(this_answers)
                this_questions = random.sample(questions, random.randint(1, len(questions)//4))
                questions_like_pairs[each_pair][1].extend(this_questions)
            answers_like_list = []
            questions_like_list = []
            for each_pair in answers_like_pairs:
                for each_answer in each_pair[1]:
                    answers_like_list.append(AnswerLike(author=each_pair[0], this_answer=each_answer))
            for each_pair in questions_like_pairs:
                for each_answer in each_pair[1]:
                    questions_like_list.append(QuestionLike(author=each_pair[0], this_question=each_answer))
            AnswerLike.objects.bulk_create(answers_like_list)
            QuestionLike.objects.bulk_create(questions_like_list)
    
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'fill_count',
            nargs=1,
            type=int
        )
        return super().add_arguments(parser)
        