from rest_framework import serializers

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=16, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'is_active', 'tg_nickname', 'password')

    def create(self, validated_data):

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
