from datetime import timedelta, datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from users.models import User


class Habit(models.Model):
    """
    frequency:
    7 - one time in week,
    6 - two times in week,
    5 - three time in week,
    4 - four times in week,
    3 - five times in week,
    2 - six times in week,
    1 - seven times in week
    """
    action = models.CharField(max_length=255, verbose_name="Действие")
    place = models.CharField(max_length=255, verbose_name="Место")
    is_public = models.BooleanField(default=False, verbose_name="Публичная")
    is_pleasent = models.BooleanField(default=False, verbose_name="Полезная")
    frequency = models.PositiveIntegerField(
        default=1, verbose_name="Количество повторений"
    )
    time_to_complete = models.DurationField(verbose_name="Время на выполнение")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", related_name='habits')
    reward_content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True
    )
    reward_object_id = models.PositiveIntegerField(null=True, blank=True)
    reward = GenericForeignKey("reward_content_type", "reward_object_id")
    time_for_habit = models.DateTimeField(default=timezone.now, verbose_name="Время выполнения привычки")
    last_remember = models.DateTimeField(null=True, blank=True, verbose_name="Последнее воспоминание")

    def set_time_to_complete(self, time):
        self.time_to_complete = timedelta(seconds=time)

    def set_time_for_habit(self, time):
        self.time_for_habit = datetime.strptime(time, '%Y-%m-%dT%H:%M')

    def __str__(self):
        return f"{self.action}, {self.time_to_complete}, {self.place} ,{self.owner}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"


class Reward(models.Model):
    reward = models.CharField(max_length=255, verbose_name="Награда")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return self.reward

    class Meta:
        verbose_name = "Награда"
        verbose_name_plural = "Награды"
