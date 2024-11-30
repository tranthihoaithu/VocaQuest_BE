from rest_framework.serializers import ModelSerializer
from learn_voca.models import Topic

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'lessons']
