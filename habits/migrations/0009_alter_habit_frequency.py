# Generated by Django 4.2.2 on 2024-07-11 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0008_alter_habit_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="frequency",
            field=models.PositiveIntegerField(
                default=1, max_length=7, verbose_name="Количество повторений"
            ),
        ),
    ]
