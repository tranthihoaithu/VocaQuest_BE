from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Lesson
from ..serializers.lesson_serializers import LessonSerializer

class LessonListView(ListAPIView):
    queryset = Lesson.objects.all()  # Lấy tất cả bài học
    serializer_class = LessonSerializer

class LessonDetailView(APIView):
    def get(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({'detail': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonSerializer(lesson)
        return Response(serializer.data, status=status.HTTP_200_OK)