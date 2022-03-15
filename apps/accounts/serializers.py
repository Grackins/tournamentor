from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import serializers


User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        })
        return data


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
        )

    def validate_password(self, value):
        try:
            validate_password(value)
        except CoreValidationError as e:
            raise ValidationError(e.messages)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(
            username=validated_data.get('email'),
            **validated_data,
        )
        user.set_password(password)
        user.save()

        profile = Profile(user=user)
        profile.save()

        return user
