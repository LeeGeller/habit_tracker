import logging
from datetime import datetime, timedelta

import pytz
from celery import shared_task

from habits.services import create_message_to_user
from habits.telegram import send_message
from users.models import User


@shared_task
def remainder_habit():
    logger = logging.getLogger(__name__)

    tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(tz)

    habit_time = now + timedelta(minutes=30)

    users_with_active_habits = User.objects.filter(habits__time_for_habit__range=(now, habit_time)).distinct()

    try:
        for user in users_with_active_habits:
            habits = user.habits.filter(time_for_habit__range=(now, habit_time))
            if habits.exists():
                identif_id, message = create_message_to_user(user.tg_id, habits)
                logger.info(f"Task created/updated for user {user.tg_id} and habit {habits}")
                try:
                    send_message(identif_id, message)
                    logger.info(f"Sent message: {message} to user {user.tg_id}")
                except Exception as e:
                    logger.error(f"Error sending message to user {user.tg_id}: {e}")
            else:
                continue
    except Exception as e:
        logger.error(f"Error processing habits for user {users_with_active_habits}: {e}")
