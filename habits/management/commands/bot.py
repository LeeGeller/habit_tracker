from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        from habits.telegram import bot
        bot()
