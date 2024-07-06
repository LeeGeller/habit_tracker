from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.telegram import remind_about_habit


@shared_task
def remainder_habit(user_id):
    now_time = timezone.now()
    print(now_time)
    time_to_remind = now_time + timedelta(minutes=30)
    print(time_to_remind)

    habit_queryset = Habit.objects.filter(owner=user_id, time_to_complete__lte=time_to_remind)

    habits_list = list(habit_queryset)
    remind_about_habit(habits_list)
