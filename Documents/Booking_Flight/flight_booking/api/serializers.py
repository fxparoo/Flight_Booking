from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
import api.models as am
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_registration.api.serializers import DefaultRegisterUserSerializer


class RegisterUserSerializer(DefaultRegisterUserSerializer):
    class Meta:
        model = am.AppUser
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data, *args):
        data = validated_data.copy()
        if data.get("is_admin"):
            user = am.AppUser.objects.create_user(**data)
            user.role = 'admin'
        else:
            user = am.AppUser.objects.create_user(**data)
            user.role = 'user'
        user.save()
        return user


class LoginTokenSerializer(TokenObtainPairSerializer):
    """Custom Serializer for jwt access and refresh token"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['role'] = user.role

        return token


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    old_password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = am.AppUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"message": "Password fields don't match"})
        return attrs

    def validate_old_password(self, value):
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError({"message": "incorrect old password"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            "message": "password updated successfully"
        }
