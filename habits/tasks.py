from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.telegram import remind_about_habit
from users.models import User


@shared_task
def remainder_habit():
    now_time = timezone.now()
    habit_time = now_time + timedelta(minutes=30)

    users_with_active_habits = User.objects.filter(habits__time_for_habit=habit_time)

    habits = dict()

    for user in users_with_active_habits:
        habits['user.id'] = user

    remind_about_habit.delay(habits)
