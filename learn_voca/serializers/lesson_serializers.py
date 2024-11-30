from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from learn_voca.models import Lesson, UserProgress, Vocabulary
from learn_voca.serializers.topic_serilizer import TopicSerializer


class LessonSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)  # Liên kết với TopicSerializer
    progress = serializers.SerializerMethodField()  # Trường tiến độ
    total_vocab = serializers.SerializerMethodField()  # Trường tổng số từ vựng

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'created_date', 'updated_date', 'active', 'topics', 'image', 'progress', 'total_vocab']

    def get_progress(self, obj):
        # Lấy đối tượng user từ request context
        user = self.context.get('request', None)

        if user and user.user.is_authenticated:  # Kiểm tra nếu user không phải None và đã đăng nhập
            return obj.get_progress_and_total(user.user)['progress']
        else:
            return 0  # Trả về 0 nếu người dùng chưa đăng nhập hoặc không hợp lệ

    def get_total_vocab(self, obj):
        # Tính tổng số từ vựng trong bài học này thông qua Topic
        total_vocab = 0
        for topic in obj.topics.all():  # Duyệt qua tất cả các Topic liên kết với bài học này
            total_vocab += topic.vocabularies.count()  # Tính số lượng từ vựng trong từng Topic
        return total_vocab  # Trả về tổng số từ vựng trong tất cả các Topic của bài học
