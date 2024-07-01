from rest_framework import serializers

from habits.models import Habit, Reward
from users.models import User


class HabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = "__all__"
