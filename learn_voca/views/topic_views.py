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
            # Lấy topic theo id
            topic = Topic.objects.get(pk=topic_id)
        except Topic.DoesNotExist:
            return Response({'detail': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)

        # Lấy dữ liệu về topic
        serializer = TopicSerializer(topic)

        # Lấy danh sách từ vựng trong topic
        vocabularies = Vocabulary.objects.filter(topic=topic)

        # Sử dụng serializer để chuyển đổi danh sách từ vựng thành JSON
        vocabulary_serializer = VocabulariesSerializer(vocabularies, many=True)

        # Trả về thông tin topic và từ vựng
        return Response({
            'topic': serializer.data,
            'vocabularies': vocabulary_serializer.data
        }, status=status.HTTP_200_OK)