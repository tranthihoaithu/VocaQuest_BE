
from rest_framework.serializers import ModelSerializer

from learn_voca.models import Lesson
from learn_voca.serializers.topic_serilizer import TopicSerializer


class LessonSerializer(ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    class Meta:
        model = Lesson
        fields = ['id','title', 'created_date','updated_date','active', 'user', 'topics']