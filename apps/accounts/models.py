from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
    )
    steam_id = models.CharField(
        max_length=32,
        null=False,
        blank=True,
    )


class Team(models.Model):
    name = models.CharField(
        max_length=32,
    )
    captain = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=False,
        related_name='own_teams'
    )
    players = models.ManyToManyField(
        Profile,
        related_name='teams',
    )


class Invitation(models.Model):
    class Status(models.TextChoices):
        WAITING = 'Waiting', _('Waiting')
        DECLINED = 'Declined', _('Declined')
        ACCEPTED = 'Accepted', _('Accepted')
        EXPIRED = 'Expired', _('Expired')

    to = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=False,
    )
    from_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        null=False,
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.WAITING,
    )

