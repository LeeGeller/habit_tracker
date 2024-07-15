import logging
from datetime import timedelta, datetime

import pytz
from rest_framework.exceptions import ValidationError

from config.settings import TIME_ZONE
from habits.models import Habit, Reward

logger = logging.getLogger(__name__)


def check_reward_models(validated_data):
    reward_content_type = validated_data.get("reward_content_type")
    reward_object_id = validated_data.get("reward_object_id")
    model_class = reward_content_type.model_class()

    if reward_object_id:
        if issubclass(model_class, Habit) and validated_data.get("is_pleasent"):
            habit_model = Habit.objects.get(pk=reward_object_id, is_pleasent=True)
            validated_data["reward"] = habit_model
    elif issubclass(model_class, Reward) and not validated_data.get("is_pleasent"):
        reward_model = Reward.objects.get(pk=reward_content_type)
        validated_data["reward"] = reward_model
    return validated_data


def check_time_to_complete(validated_data):
    time = validated_data.get("time_to_complete")
    if time and (timedelta(seconds=0) < time < timedelta(seconds=121)):
        return validated_data
    else:
        raise ValidationError("Time must be more than 0 and less than 120 seconds")


def check_frequency(validated_data):
    frequency = validated_data.get("frequency")
    if frequency and frequency > 0:
        return validated_data
    else:
        raise ValidationError("Frequency must be more than 0")


def create_message_to_user(user_id, habits):
    message = ""

    try:
        message += f"I will do {habits.action} at {habits.time_for_habit.strftime('%X')} in {habits.place}\n"
        logger.info(f"Created message: {message} for user {user_id}")
    except Exception as e:
        logger.error(f"Error creating message for user {user_id}: {e}")
    return user_id, message


def create_habit_time():
    tz = pytz.timezone(TIME_ZONE)
    now = datetime.now(tz)
    now, habit_time = now + timedelta(minutes=30), now + timedelta(minutes=31)

    return now, habit_time
