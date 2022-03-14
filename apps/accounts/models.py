from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
    )
    steam_id = models.CharField(
        max_length=32,
    )


class Team(models.Model):
    name = models.CharField(
        max_length=32,
    )
    captain = models.ForeignKey(
        Profile,
    )
    players = models.ManyToManyField(
        Profile,
    )


class Invitation(models.Model):
    class Status(models.TextChoices):
        WAITING = 'Waiting', _('Waiting')
        DECLINED = 'Declined', _('Declined')
        ACCEPTED = 'Accepted', _('Accepted')
        EXPIRED = 'Expride', _('Expired')

    to = models.ForeignKey(
        Profile,
    )
    from_team = models.ForeignKey(
        Team,
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.WAITING,
    )

