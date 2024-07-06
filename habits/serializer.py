from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from habits.models import Habit, Reward
from habits.services import check_reward_models


class HabitsSerializer(serializers.ModelSerializer):
    reward_content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(), required=False
    )
    reward_object_id = serializers.IntegerField(required=False)

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["owner"]


class RewardSerializer(serializers.ModelSerializer):
    reward_content_type = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(), required=False
    )
    reward_object_id = serializers.IntegerField(required=False)

    class Meta:
        model = Reward
        fields = "__all__"
        read_only_fields = ["owner"]
