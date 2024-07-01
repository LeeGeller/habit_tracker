from rest_framework import viewsets
from rest_framework.response import Response

from habits.models import Habit
from habits.serializer import HabitsSerializer, RewardSerializer
from users.permissions import IsAutehenticated


class HabitsViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = [IsAutehenticated]

    def list(self, *args, **kwargs):
        public_habits = Habit.objects.filter(is_public=True)
        serializer = HabitsSerializer(public_habits, many=True)
        return Response(serializer.data)
