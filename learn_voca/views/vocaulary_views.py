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

# tạo bai kiem tra
class CreateTestView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        lesson_id = request.data.get('lesson_id')

        lesson = Lesson.objects.get(id=lesson_id)
        test = Test.objects.create(user=user, lesson=lesson)

        # Lấy các từ vựng trong bài học và tạo câu hỏi
        vocabularies = lesson.topics.vocabularies.all()  # Từ vựng liên kết với chủ đề trong bài học
        for vocabulary in vocabularies:
            question = Question.objects.create(question_text=f"What is the meaning of {vocabulary.word}?", question_type='MC')
            question.voca.add(vocabulary)
            test.questions.add(question)

        return Response({'message': 'Test created successfully', 'test_id': test.id})

# nop cau tra loi tinh diem
class SubmitAnswerView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        question_id = request.data.get('question_id')
        selected_answer = request.data.get('selected_answer')

        question = Question.objects.get(id=question_id)
        correct_answer = question.correct_answer
        is_correct = selected_answer == correct_answer

        # Lưu câu trả lời của người dùng
        UserAnswer.objects.create(user=user, question=question, selected_answer=selected_answer, is_correct=is_correct)

        return Response({'message': 'Answer submitted', 'is_correct': is_correct})
# theo doi tien trinh hoc tap
class ProgressView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        progress = UserProgress.objects.filter(user=user).select_related('vocabulary')
        data = [
            {
                'vocabulary': p.vocabulary.word,
                'stage': p.stage,
                'last_reviewed': p.last_reviewed
            } for p in progress
        ]
        return Response(data)

