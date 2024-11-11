from django.contrib import admin
from .models import *

# Register your models here.


admin.register(Profile)
admin.register(Tag)
admin.register(Question)
admin.register(Answer)
admin.register(QuestionLike)
admin.register(AnswerLike)