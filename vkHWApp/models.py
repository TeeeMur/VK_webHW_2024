from django.db import models
from django.contrib.auth.models import User as AuthUser


class Profile(models.Model):
    name = models.CharField(max_length=25, null=False, blank=False)
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profileImage = models.ImageField(upload_to='profileImgs/', null=True)

    def __str__(self):
        return self.name

class TagManager(models.Manager):
    def get_ten_popular_tags(self):
        return self.order_by('created_at')[:10]

class Tag(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    created_at = models.DateField(auto_now_add=True)

    objects = TagManager()

    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
    def get_new_questions(self):
        return self.order_by('created_at').annotate(rating=models.Count('questionlike'), answers_count=models.Count('answer'))
    
    def get_hot_questions(self):
        return self.annotate(answers_count=models.Count('answer'), rating=models.Count('questionlike')).order_by('-answers_count', '-rating')
    
    def get_questions_by_tag(self, tag):
        return self.filter(tags__name=tag).annotate(rating=models.Count('questionlike'), answers_count=models.Count('answer')).order_by('answers_count')
    
    def get_question_by_id(self, id):
        return self.annotate(rating=models.Count('questionlike')).get(id=id)

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=False)
    text = models.TextField(max_length=900, null=False, blank=False)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

class AnswerManager(models.Manager):
    def get_answers_to_question(self, question_id):
        return self.filter(reference_question__id=question_id).order_by('answerlike').annotate(rating=models.Count('answerlike'))


class Answer(models.Model):
    reference_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=False)
    text = models.TextField(max_length=900, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AnswerManager()

class QuestionLike(models.Model):
    this_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=False)

    class Meta:
        unique_together = ['this_question', 'author']

class AnswerLike(models.Model):
    this_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=False)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=False)

    class Meta:
        unique_together = ['this_answer', 'author']

