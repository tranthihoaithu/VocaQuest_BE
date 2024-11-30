from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate
from learn_voca.models import User
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        # Kiểm tra xem người dùng có tồn tại không
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Unable to log in with provided credentials.")

        if not user.is_active:
            raise serializers.ValidationError("User  account is disabled.")

        # Trả về thông tin người dùng
        return {
            'username': user.username,
            'email': user.email,
            # Có thể thêm các trường khác nếu cần
        }

