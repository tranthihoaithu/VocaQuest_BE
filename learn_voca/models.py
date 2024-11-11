from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    user = models.ManyToManyField(User,related_name='lessons')
    def __str__(self):
        return self.title

class Topic(models.Model):
    name = models.CharField(max_length=100)
    lessons = models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='topics',default=1)
    def __str__(self):
        return self.name

class Vocabulary(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='vocabularies')
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=100)
    audio = models.FileField(upload_to='audio/', max_length=100, unique=True)
    example_sentence = models.CharField(max_length=255)
    stage = models.IntegerField() #giai doan hoc tu vung
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.word

class UserProgress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='progress')
    vocabulary = models.ForeignKey(Vocabulary,on_delete=models.CASCADE,related_name='progress')
    stage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(6)])
    last_reviewed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.vocabulary.word} (Stage: {self.stage})"



class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


class Question(models.Model):
    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = 'MC', 'Multiple Choice'
        FILL_IN_THE_BLANK = 'F', 'Fill In The Blank'
        LISTEN_AND_CHOICE = 'L', 'Listen And Choice'

    tests = models.ManyToManyField(Test, related_name='questions')
    question_type = models.CharField( max_length=2,
        choices=QuestionType.choices,
        default=QuestionType.MULTIPLE_CHOICE,)
    question_text = models.CharField(max_length=200)
    voca = models.ManyToManyField(Vocabulary,related_name='questions')
    correct_answer = models.CharField(max_length=200, null=True, blank=True)

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=200, null=True, blank=True)
    is_correct = models.BooleanField(default=False)