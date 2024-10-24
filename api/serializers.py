from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match")
        return data
    
    def validate_email(self, data):
        if CustomUser.objects.filter(email=data).exists():
            raise serializers.ValidationError("Email already exists")
        return data
    
    def create(self, validated_data):

        validated_data.pop('password2')

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError('User does not exist')
            
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User is not active')
            else:
                raise serializers.ValidationError("Incorrect Password")
        else:
            raise serializers.ValidationError('Invalid credentials')
        
        data['user'] = user
        return data
    
class LogoutSerilizer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

    def validate(self, data):
        refresh_token = data.get('refresh')

        if not refresh_token:
            raise serializers.ValidationError('Refresh Token is required')
        return data


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'image', 'slug')



