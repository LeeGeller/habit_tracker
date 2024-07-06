from datetime import timedelta

from rest_framework.exceptions import ValidationError

from habits.models import Habit, Reward


def check_reward_models(validated_data):
    reward_content_type = validated_data["reward_content_type"]
    reward_object_id = validated_data["reward_object_id"]
    model_class = reward_content_type.model_class()

    if reward_object_id and reward_content_type:
        if issubclass(model_class, Habit) and validated_data.get("is_pleasent"):
            habit_model = Habit.objects.get(pk=reward_object_id, is_pleasent=True)
            validated_data["reward"] = habit_model
    elif issubclass(model_class, Reward) and not validated_data.get("is_pleasent"):
        reward_model = Reward.objects.get(pk=reward_object_id)
        validated_data["reward"] = reward_model
    return validated_data


def check_time_to_complete(validated_data):
    time = validated_data.get("time_to_complete")
    if time and (0 < time < 121):
        return validated_data
    else:
        raise ValidationError("Time must be more than 0 and less than 120 seconds")


def check_frequency(validated_data):
    frequency = validated_data.get("frequency")
    if frequency and frequency > 8:
        return validated_data
    else:
        raise ValidationError("Frequency must be more than 0")
