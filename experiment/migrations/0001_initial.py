# Generated by Django 5.1.2 on 2024-11-04 23:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('group', models.CharField(choices=[('A', 'Group A'), ('B', 'Group B')], max_length=1)),
                ('session_id', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('question_id', models.CharField(max_length=50)),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiment.participant')),
            ],
        ),
    ]
