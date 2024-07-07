from django.utils import timezone
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from habits.models import Habit, Reward
from habits.paginatirs import HabitPaginator, RewardPaginator
from habits.serializer import HabitsSerializer, RewardSerializer
from habits.services import check_reward_models, check_time_to_complete, check_frequency
from users.permissions import IsOwner


class HabitsViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    pagination_class = HabitPaginator

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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_public=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ["retrieve", "update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    pagination_class = RewardPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ["retrieve", "update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
