from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.telegram import remind_about_habit


@shared_task
def remainder_habit(user_id):
    now_time = timezone.now()
    habit_time = now_time + timedelta(minutes=30)

    habit_identification = Habit.objects.filter(
        owner=user_id, time_for_habit__lte=habit_time
    ).values_list('id', flat=True)

    habits_list = list(habit_identification)
    remind_about_habit.delay(habits_list)
