from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from habits.telegram import bot
from users.models import User


@shared_task
def remainder_habit():
    now_time = timezone.now()
    habit_time = now_time + timedelta(hours=3, minutes=30)

    users_with_active_habits = User.objects.filter(habits__time_for_habit__gt=habit_time)

    for user in users_with_active_habits:
        name = f'reminder_habit_{user.id}_{user.habits.id}'

        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=user.time_for_habit.minute,
            hour=user.time_for_habit.hour,
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )

        PeriodicTask.objects.update_or_create(
            crontab=schedule,
            name=name,
            defaults={
                'task': 'habits.tasks.remainder_habit',
                'args': f'[{user.id}, {user.habits.id}]',
            }
        )
        bot.send_message(user.tg_id, f"I will {user.habits.action} at {user.time_for_habit} in {user.habits.place}")
