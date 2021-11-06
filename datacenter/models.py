from django import utils
from django.db import models


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def get_duration(self):
        if self.leaved_at:
            return self.leaved_at - self.entered_at
        else:
            return utils.timezone.localtime() - self.entered_at

    def is_long(self, minutes):
        duration = self.get_duration()
        duration_minutes = int(duration.total_seconds() // 60)
        if duration_minutes > minutes: return True
        return False

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved='leaved at ' + str(self.leaved_at) if self.leaved_at else 'not leaved'
        )


def format_duration(duration):
    duration_minutes = int(duration.total_seconds() % 3600 // 60)
    duration_hours = int(duration.total_seconds() // 3600)
    if duration_hours:
        formated_duration = f'{duration_hours}ч {duration_minutes}мин'
    else:
        formated_duration = f'{duration_minutes}мин'
    return formated_duration
