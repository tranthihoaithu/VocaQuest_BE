from rest_framework.serializers import ModelSerializer
from learn_voca.models import *

class VocabulariesSerializer(ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = '__all__'

# Serializer cho UserProgress
class UserProgressSerializer(ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ['id', 'user', 'vocabulary', 'last_reviewed']

class QuestionSerializer(ModelSerializer):
    voca = VocabulariesSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_type', 'question_text', 'voca','satge', 'choices', 'audio_url']

    def get_choices(self, obj):
        # Lấy tất cả các lựa chọn cho câu hỏi trắc nghiệm
        choices = []
        if obj.question_type == 'MC':
            # Lấy danh sách các lựa chọn trắc nghiệm (giả sử có một bảng chứa các lựa chọn)
            for vocabulary in obj.voca.all():
                choices.append(vocabulary.meaning)
        return choices

    def get_audio_url(self, obj):
        # Nếu câu hỏi là loại "Listen and Choice", trả về audio_url
        if obj.question_type == 'L':
            # Giả sử URL âm thanh được lưu trong Vocabulary hoặc cấu hình khác
            return f"http://example.com/audio/{obj.voca.first().word}.mp3"
        return None