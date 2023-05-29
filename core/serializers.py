from typing import Any, Type

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True
    )
    password_repeat = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs) -> Any:
        if attrs.get('password') != attrs.pop('password_repeat'):
            raise serializers.ValidationError('Password mismatch')
        validate_password(attrs.get('password'))
        return attrs

    def create(self, validated_data) -> Any:
        user = super().create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    class Meta:
        model: Type[User] = User
        fields: tuple = ('username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model: Type[User] = User
        fields: tuple = ('id', 'username', 'first_name', 'last_name', 'email')


class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        required=True
    )
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )

    def validate(self, attrs):
        user = self.context.get('request').user
        old_password, new_password = attrs.get('old_password'), attrs.get('new_password')
        if not user.check_password(old_password):
            raise serializers.ValidationError('Wrong password')

        if new_password is not None and old_password == new_password:
            raise serializers.ValidationError('Similar password')
        return attrs

    def update(self, instance: User, validated_data) -> Any:
        instance.set_password(validated_data.get('new_password'))
        return super().update(instance, validated_data)

    class Meta:
        model: Type[User] = User
        fields: tuple = ('old_password', 'new_password')

