from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import UserProgress, Vocabulary

class UpdateProgressView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        vocabulary_id = request.data.get('vocabulary_id')
        stage = request.data.get('stage')

        vocabulary = Vocabulary.objects.get(id=vocabulary_id)
        progress, created = UserProgress.objects.get_or_create(user=user, vocabulary=vocabulary)
        progress.stage = stage
        progress.save()

        return Response({'message': 'Progress updated successfully', 'stage': progress.stage})
