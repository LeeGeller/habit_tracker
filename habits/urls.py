from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitsViewSet, RewardViewSet, HabitsUsersList

appname = HabitsConfig.name

router = DefaultRouter()
router.register(r"habits", HabitsViewSet, basename="habits")
router.register(r"rewards", RewardViewSet, basename="rewards")

urlpatterns = [
    path("users-list/", HabitsUsersList.as_view(), name="users-habits"),
] + router.urls
