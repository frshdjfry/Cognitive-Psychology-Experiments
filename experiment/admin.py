from django.contrib import admin

from experiment.models import Participant, Response


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Participant._meta.fields]


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Response._meta.fields]

