from rest_framework.test import APITestCase

from habits.models import Reward, Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.email = 'test_test_u@gmail.com'
        self.is_active = True
        self.tg_id = 1142947908
        self.password = '1234'

        self.user = User.objects.create(
            email=self.email, is_active=self.is_active, tg_id=self.tg_id
        )
        self.user.set_password(self.password)
        self.user.save()

        response = self.client.post("token/refresh/", {"email": self.email, "password": self.password})
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.reward = Reward.objects.create(
            reward="test_reward",
            owner=self.user
        )
        self.habit_pleasent = Habit.objects.create(
            action="test_habit 1",
            place="test_place 1",
            frequency=1,
            time_to_complete="00:30:00",
            is_pleasent=True,
            owner=self.user,
            time_for_habit="2024-07-16T12:00",
            last_remember="2024-07-16T12:00"
        )
        self.habit_not_plesant = Habit.objects.create(
            action="test_habit 2",
            place="test_place 2",
            frequency=1,
            time_to_complete="00:30:00",
            is_pleasent=False,
            owner=self.user,
            time_for_habit="2024-07-16T12:00",
            last_remember="2024-07-16T12:00"
        )

    def test_habit_list(self):
        response = self.client.get("/habits/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_create_habit(self):
        data = {
            "action": "test_habit 3",
            "place": "test_place 3",
            "frequency": 1,
            "time_to_complete": "00:30:00",
            "is_pleasent": False,
            "time_for_habit": "2024-07-16T12:00",
            "last_remember": "2024-07-16T12:00"
        }
        response = self.client.post("/habits/", data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['action'], "test_habit 3")
