from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views.lesson_views import LessonListView,LessonDetailView
from .views.topic_views import TopicDetailView
from .views.vocaulary_views import VocabularyListView, VocabularyNextView, VocabularyCheckView, VocabularyReviewView
from .views.accounts import RegisterAPIView, LoginAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    # path('login/', LoginAPIView.as_view(), name='login'),
    path('api/login_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:lesson_id>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('topics/<int:topic_id>/', TopicDetailView.as_view(), name='topic-detail'),
    path('vocabularies/<int:topic_id>/', VocabularyListView.as_view(), name='vocabulary_list'),
    path('vocabularies/next-two/<int:topic_id>/', VocabularyNextView.as_view(), name='vocabulary_next_two'),
    path('vocabularies/check/', VocabularyCheckView.as_view(), name='vocabulary_check'),
    path('vocabularies/review/<int:topic_id>/', VocabularyReviewView.as_view(), name='vocabulary_review'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)