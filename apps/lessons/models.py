from django.db import models
from django.template.defaultfilters import title
from apps.users.models import User

# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Topic(models.Model):
    name = models.CharField(max_length=100)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

class Question(models.Model):
    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = 'MC', 'Multiple Choice'
        FILL_IN_THE_BLANK = 'F', 'Fill In The Blank'
        LISTEN_AND_WRITE = 'L', 'Listen And Write'

    tests = models.ManyToManyField(Test, related_name='questions')
    question_type = models.CharField( max_length=2,
        choices=QuestionType.choices,
        default=QuestionType.MULTIPLE_CHOICE,)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text


