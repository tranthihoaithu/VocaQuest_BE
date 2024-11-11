from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from ..serializers.vocabulary_serializers import VocabulariesSerializer

class VocabularyApp:
    def __init__(self):
        self.current_index = 0  # Đánh dấu chỉ mục từ vựng hiện tại

    def get_next_vocabulary(self, vocabularies):
        """
        Lấy từ vựng tiếp theo dựa trên chỉ mục hiện tại.
        """
        if self.current_index < len(vocabularies):
            vocabulary = vocabularies[self.current_index]
            self.current_index += 1  # Tăng chỉ mục để lấy từ vựng tiếp theo
            return vocabulary
        return None  # Nếu không còn từ vựng nào, trả về None

class VocabularyListView(APIView):
    def get(self, request, topic_id):
        """
        Lấy tất cả từ vựng chưa học (stage < 6) trong topic với topic_id và trả về từ vựng đầu tiên.
        """
        vocabularies = Vocabulary.objects.filter(topic_id=topic_id, stage__lt=6)

        if vocabularies.exists():
            # Serialize dữ liệu từ vựng
            serializer = VocabulariesSerializer(vocabularies, many=True)

            # Lấy từ vựng đầu tiên trong danh sách
            first_vocabulary = serializer.data[0] if len(serializer.data) > 0 else None

            return Response({
                "topic_id": topic_id,
                "first_vocabulary_to_learn": first_vocabulary
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "No vocabularies left to learn in this topic."
            }, status=status.HTTP_200_OK)


class VocabularyNextView(APIView):
    """
    API để lấy 2 từ vựng tiếp theo cần học trong topic với topic_id.
    """
    def get(self, request, topic_id):
        # Lọc các từ vựng của topic cụ thể và stage < 3
        vocabularies = Vocabulary.objects.filter(topic_id=topic_id, stage__lt=3)

        # Nếu có đủ 2 từ vựng để hiển thị
        if vocabularies.count() >= 2:
            vocab_list = vocabularies[:2]  # Lấy 2 từ vựng đầu tiên
            serializer = VocabulariesSerializer(vocab_list, many=True)
            return Response({
                "vocabularies": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "No more vocabularies to display or not enough vocabularies left."
            }, status=status.HTTP_400_BAD_REQUEST)

class VocabularyCheckView(APIView):
    """
    API để kiểm tra hai từ vựng đã học, cập nhật stage nếu trả lời đúng.
    """
    def post(self, request):
        """
        Kiểm tra hai từ vựng và cập nhật stage nếu đúng.
        """
        vocab_data = request.data.get('vocabularies', [])
        if len(vocab_data) != 2:
            return Response({"message": "You must provide exactly two vocabularies."}, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra và cập nhật giai đoạn cho từng từ vựng
        for vocab in vocab_data:
            word_id = vocab.get('id')
            answer = vocab.get('answer')  # Đáp án của người dùng (ví dụ: nghĩa của từ)

            try:
                vocabulary = Vocabulary.objects.get(id=word_id)

                # Kiểm tra đáp án (Giả sử bạn kiểm tra nghĩa từ)
                if answer.lower() == vocabulary.meaning.lower():
                    # Nếu đáp án đúng, tăng stage lên
                    vocabulary.stage += 1
                    vocabulary.save()
                else:
                    # Nếu sai, trả về từ vựng và đáp án đúng
                    return Response({
                        "vocabulary": VocabulariesSerializer(vocabulary).data,
                        "correct_answer": vocabulary.meaning
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Vocabulary.DoesNotExist:
                return Response({"message": "Vocabulary not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Both words checked successfully."}, status=status.HTTP_200_OK)

class VocabularyReviewView(APIView):
    """
    API để kiểm tra 5 từ vựng đầu tiên và kết thúc khi đạt stage = 3.
    """
    def get(self, request, topic_id):
        vocabularies = Vocabulary.objects.filter(topic_id=topic_id, stage=3)

        # Kiểm tra nếu tất cả các từ vựng đã đạt stage = 3
        if vocabularies.count() == 5:
            return Response({
                "message": "You have completed the lesson!"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "You still have words to learn."
            }, status=status.HTTP_400_BAD_REQUEST)
