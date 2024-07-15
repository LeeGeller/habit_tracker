import logging
from datetime import timedelta, datetime

from celery import shared_task

from habits.models import Habit
from habits.services import create_message_to_user, create_habit_time
from habits.telegram import send_message


@shared_task
def remainder_habit():
    logger = logging.getLogger(__name__)

    now, habit_time = create_habit_time()

    habits_with_users = Habit.objects.filter(
        time_for_habit__range=(now, habit_time)).select_related('owner')
    logger.info(f"Found {habits_with_users} habits with users")

    try:
        for habit in habits_with_users:
            identif_id, message = create_message_to_user(habit.owner.tg_id, habit)
            logger.info(f"Task created/updated for user {habit.owner.tg_id} and habit {habit}")

            try:
                send_message(identif_id, message)
                habit.last_remember += timedelta(days=habit.frequency)
                habit.save()
                logger.info(f"Sent message: {message} to user {habit.owner.tg_id}")
            except Exception as e:
                logger.error(f"Error sending message to user {habit.owner.tg_id}: {e}")
    except Exception as e:
        logger.error(f"Error processing habits for user {habits_with_users}: {e}")
