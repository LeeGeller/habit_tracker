from datetime import timedelta

from django.db import models

from users.models import User


class Habit(models.Model):
    action = models.CharField(max_length=255, verbose_name='Действие')
    place = models.CharField(max_length=255, verbose_name='Место')
    is_public = models.BooleanField(default=False, verbose_name='Публичная')
    is_pleasent = models.BooleanField(default=False, verbose_name='Полезная')
    frequency = models.PositiveIntegerField(default=1, verbose_name='Количество повторений')
    time_to_complete = models.DurationField(verbose_name='Время на выполнение')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    reward = models.ForeignKey('Reward', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Награда')

    def set_time_to_complete(self, time):
        self.time_to_complete = timedelta(seconds=time)

    def __str__(self):
        return f"{self.action}, {self.time_to_complete}, {self.place} ,{self.owner}"

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'


class Reward(models.Model):
    reward = models.CharField(max_length=255, verbose_name='Награда')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return self.reward

    class Meta:
        verbose_name = 'Награда'
        verbose_name_plural = 'Награды'
