from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Lesson, Topic,Vocabulary
from ..serializers.lesson_serializers import TopicSerializer
from ..serializers.vocabulary_serializers import VocabulariesSerializer


class TopicDetailView(APIView):
    def get(self, request, topic_id):
        try:
            topic = Topic.objects.get(pk=topic_id)
        except Lesson.DoesNotExist:
            return Response({'detail': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TopicSerializer(topic)
        # Lấy danh sách các từ vựng trong topic
        vocabularies = Vocabulary.objects.filter(topic=topic)
        vocabulary_serializer = VocabulariesSerializer(vocabularies, many=True)
        return Response({
            'topic': serializer.data,
            'vocabularies': vocabulary_serializer.data
        }, status=status.HTTP_200_OK)