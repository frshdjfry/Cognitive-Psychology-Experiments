# Generated by Django 5.1.2 on 2024-11-06 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0002_remove_participant_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='response_time',
            field=models.DurationField(blank=True, null=True),
        ),
    ]