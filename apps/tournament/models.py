from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Team


class Game(models.Model):
    tournament = models.ForeignKey(
        'Tournament',
        on_delete=models.CASCADE,
        null=False,
    )
    server_ip = models.GenericIPAddressField()
    server_port = models.IntegerField()
    result = models.CharField(
        max_length=10,
    )
    left_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        related_name='games_as_left_team',
    )
    right_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        related_name='games_as_right_team',
    )
    start_date = models.DateTimeField()


class Tournament(models.Model):
    class Mode(models.TextChoices):
        SINGLE_ELIM = 'SingleElim', _('Single-elimination')

    mode = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=Mode.choices,
    )
    target_size = models.IntegerField(
        choices=(
            (2, '2'),
            (4, '4'),
            (8, '8'),
            (16, '16'),
        ),
    )
    start_date = models.DateTimeField()
    participants = models.ManyToManyField(
        Team,
        through='Participation',
    )

    def shuffle_participants(self):
        participations = Participation.objects.filter(tournament=self).all()
        random.shuffle(participations)
        for i, participant in enumerate(participations):
            participant.order = i
            participant.save()

    def can_join(self):
        return self.participants.count < self.target_size


class Participation(models.Model):
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        null=False,
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        null=False,
    )
    order = models.IntegerField()
