from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from habits.models import Habit, Reward
from habits.serializer import HabitsSerializer, RewardSerializer
from habits.services import check_reward_models, check_time_to_complete, check_frequency


class HabitsViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        check_time_to_complete(validated_data)
        check_frequency(validated_data)

        data = check_reward_models(validated_data)
        habit = Habit.objects.create(**data, owner=request.user)

        return Response(HabitsSerializer(habit).data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
