from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from requests import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from ..serializers.user_serializers import UserSerializer, LoginSerializer
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from learn_voca.models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def send_verification_email(user):
    token = default_token_generator.make_token(user)
    verification_link = reverse('verify_email', kwargs={'user_id': user.id, 'token': token})
    verification_url = f"{settings.SITE_URL}{verification_link}"

    subject = "Xác thực Email"
    message = f"Nhấn vào link sau để xác thực email của bạn: {verification_url}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            # Tạo payload cho JWT
            user = serializer.instance
            payload = jwt_payload_handler(user)
            # Encode payload để tạo ra JWT
            token = jwt_encode_handler(payload)
            # Trả về thông tin người dùng và JWT token
            send_verification_email(user)
            return Response({
                'user': {
                    'username': user.username,
                    'email': user.email,
                },
                'access_token': token,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def verify_email(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse("Người dùng không tồn tại.")

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Xác thực email thành công! Bạn có thể đăng nhập.")
    else:
        return HttpResponse("Link xác thực không hợp lệ hoặc đã hết hạn.")

class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    'user': {
                        'username': user.username,
                        'email': user.email,
                    },
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)