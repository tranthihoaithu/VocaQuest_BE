from django.contrib import admin
from .models import Lesson,Topic,Test,Question

# Register your models here.
admin.site.register(Lesson)
admin.site.register(Topic)
admin.site.register(Test)
admin.site.register(Question)