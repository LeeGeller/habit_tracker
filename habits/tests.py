from rest_framework.test import APITestCase

from habits.models import Reward, Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.email = "test@gmail.com"
        self.is_active = True
        self.tg_id = 1142947908
        self.password = "1234"

        self.user = User.objects.create(
            email=self.email, is_active=self.is_active, tg_id=self.tg_id
        )
        self.user.set_password(self.password)
        self.user.save()
        self.client.login(email="test_test_u@gmail.com", password="1234")

        response = self.client.post(
            "/users/login/", {"email": self.email, "password": self.password}
        )
        self.token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.reward = Reward.objects.create(reward="test_reward", owner=self.user)

        self.habit_pleasent = Habit.objects.create(
            action="test_habit 1",
            place="test_place 1",
            frequency=1,
            time_to_complete="00:00:30",
            is_pleasent=True,
            is_public=True,
            owner=self.user,
            time_for_habit="2024-07-16T12:00",
            last_remember="2024-07-16T12:00",
        )
        self.habit_not_plesant = Habit.objects.create(
            action="test_habit 2",
            place="test_place 2",
            frequency=1,
            time_to_complete="00:00:30",
            is_pleasent=False,
            is_public=False,
            owner=self.user,
            time_for_habit="2024-07-16T12:00",
            last_remember="2024-07-16T12:00",
        )

    def test_habit_list(self):
        response = self.client.get("/habits/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_users_list(self):
        response = self.client.get("/users-list/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_get_one_habit(self):
        response = self.client.get(f"/habits/{self.habit_pleasent.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.habit_pleasent.id)

    def test_update_habit(self):
        response = self.client.get(f"/habits/{self.habit_pleasent.id}/")
        self.assertEqual(response.status_code, 200)

        data = {
            "action": "test_habit changed",
            "place": "test_place changed",
            "frequency": 5,
            "time_to_complete": "00:00:40",
            "is_pleasent": True,
            "is_public": True,
            "owner": self.user,
            "time_for_habit": "2024-07-17T12:00",
            "last_remember": "2024-07-17T12:00",
        }

        data_for_matches = response.data

        self.client.put(f"/habits/{self.habit_pleasent.id}/", data)

        response = self.client.get(f"/habits/{self.habit_pleasent.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, data_for_matches)

    def test_delete_habit(self):
        response = self.client.delete(f"/habits/{self.habit_pleasent.id}/")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"/habits/{self.habit_pleasent.id}/")
        self.assertEqual(response.status_code, 404)
