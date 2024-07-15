from django.test import TestCase

from habits.models import Reward, Habit
from users.models import User


class HabitTestCase(TestCase):
    id = 1
    email = 'test_test_u@gmail.ru'
    is_active = True
    tg_id = 1142947908
    password_1 = '1234'
    password_2 = '1234'

    def setUp(self):
        user = User.objects.create(
            email=self.email, is_active=self.is_active, tg_id=self.tg_id
        )
        user.set_password(self.password_1)
        user.save()

        response = self.client.post("/users/token/", {"email": self.email, "password": self.password_1}
                                    )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        reward = Reward.objects.create(
            reward="test_reward",
            owner=user.id
        )
        habit_pleasent = Habit.objects.create(
            name="test_habit 1",
            description="test_description 1",
            time_for_habit=1,
            is_pleasent=True,
            owner=user.id,
        )
        habit_not_plesant = Habit.objects.create(
            name="test_habit 2",
            description="test_description 2",
            time_for_habit=1,
            is_pleasent=False,
            owner=user.id, )
