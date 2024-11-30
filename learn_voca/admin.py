from django.contrib import admin
from django.utils.html import mark_safe
from .models import *
# Register your models here.
class LessonAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    search_fields = ["title", "created_date"]
    readonly_fields = ["avatar"]

    def avatar(self, lesson):
        return mark_safe(
            "<img src='/media/{img_url}' width='60' height='60' alt='{alt}' />".format(img_url=lesson.image.name,alt=lesson.title))


class VocabularyAdmin(admin.ModelAdmin):
    list_display = ["id", "topic", "word", "meaning"]

class VocaInlineAdmin(admin.StackedInline):
    model = Vocabulary
    pk_name = 'topic'

class TopicAdmin(admin.ModelAdmin):
    list_display = ["id", "name","lessons"]
    inlines = (VocaInlineAdmin,)

class UserAdmin(admin.ModelAdmin):
    list_display = ["id","full_name", "username", "email", "is_staff", "is_active"]

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    full_name.admin_order_field = 'last_name'  # Sắp xếp theo last_name
    full_name.short_description = 'Full Name'  # Tiêu đề cột trong admin

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Vocabulary, VocabularyAdmin)
admin.site.register(Question)
admin.site.register(User, UserAdmin)








