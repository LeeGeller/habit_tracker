from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="Admin@Admin.com",
            tg_id="12345",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password("1234")
        user.save()
