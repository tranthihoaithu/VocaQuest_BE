from rest_framework.serializers import ModelSerializer
from learn_voca.models import Topic
from learn_voca.serializers.vocabulary_serializers import VocabulariesSerializer


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'lessons']
