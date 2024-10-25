from django.db import models
from apps.lessons.models import Topic
from apps.users.models import User
# Create your models here.
class Vocabulary(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='vocabularies')
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=100)
    pronunciation = models.CharField(max_length=100)
    audio = models.FileField(upload_to='audio/', max_length=100, unique=True)
    example_sentence = models.CharField(max_length=255)
    stage = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.word
class Progression(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progressions')
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='progressions')
    last_reviewed_at = models.DateTimeField(auto_now_add=True)
    review_count = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0)
    next_reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s progression on {self.vocabulary.word}"