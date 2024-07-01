from rest_framework import serializers

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    print("Сериалайзер")
    password = serializers.CharField(max_length=16, write_only=True)
    print("Создалось поле пароля")

    class Meta:
        model = User
        fields = ('id', 'email', 'is_active', 'tg_nickname', 'password')

    def create(self, validated_data):
        print("Вызывается метод криэйт")
        print(validated_data)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        print("Пользователь создан")

        return user
