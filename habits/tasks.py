from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from habits.services import create_message_to_user
from users.models import User

import logging

logger = logging.getLogger(__name__)


@shared_task
def remainder_habit():
    now_time = timezone.now()
    habit_time = now_time + timedelta(hours=3, minutes=30)

    users_with_active_habits = User.objects.filter(habits__time_for_habit__range=(now_time, habit_time))

    for user in users_with_active_habits:
        try:
            habits = user.habits.filter(time_for_habit__range=(now_time, habit_time))

            for habit in habits:
                name = f'reminder_habit_{user.id}_{habit.id}_{now_time}'

                schedule, created = CrontabSchedule.objects.get_or_create(
                    minute=habit.time_for_habit.minute,
                    hour=habit.time_for_habit.hour,
                    day_of_week='*',
                    day_of_month='*',
                    month_of_year='*',
                )

                PeriodicTask.objects.update_or_create(
                    crontab=schedule,
                    name=name,
                    defaults={
                        'task': 'habits.tasks.remainder_habit',
                        'args': f'[{user.id}, {habit.id}]',
                    }
                )

            user_habits = user.habits.all()

            create_message_to_user(user.id, user_habits)

            logger.info(f"Task created/updated for user {user.id} and habits {[habit.id for habit in habits]}")

        except Exception as e:
            logger.error(f"Error creating task for user {user.id}: {e}")
