from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitsViewSet

appname = HabitsConfig.name

router = DefaultRouter()
router.register(r'habits', HabitsViewSet, basename="habits")
urlpatterns = [
              ] + router.urls
