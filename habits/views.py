from django.shortcuts import render
from rest_framework import viewsets

from habits.models import Habit
from habits.serializer import HabitsSerializer, RewardSerializer
from users.permissions import IsAutehenticated


class HabitsViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = [IsAutehenticated]


class RewardViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [IsAutehenticated]