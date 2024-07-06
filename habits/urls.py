from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitsViewSet, RewardViewSet

appname = HabitsConfig.name

router = DefaultRouter()
router.register(r"habits", HabitsViewSet, basename="habits")
router.register(r"rewards", RewardViewSet, basename="rewards")

urlpatterns = [] + router.urls
