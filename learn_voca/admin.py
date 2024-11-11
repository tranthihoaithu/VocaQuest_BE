from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Lesson)
admin.site.register(Topic)
admin.site.register(Vocabulary)
admin.site.register(Question)