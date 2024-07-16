from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from habits.models import Habit, Reward
from habits.paginatirs import HabitPaginator, RewardPaginator
from habits.serializer import HabitsSerializer, RewardSerializer, HabitsUsersListSerializer
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
        serializer.save(**data, owner=request.user)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        habits = self.queryset.filter(is_public=True)
        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        habit = self.get_object()
        serializer = self.get_serializer(habit)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ["retrieve", "update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class HabitsUsersList(ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitsUsersListSerializer
    pagination_class = HabitPaginator

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


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
