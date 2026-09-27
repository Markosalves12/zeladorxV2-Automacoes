from django.db import models
from utils.utils import generate_id_random
from gerente.models import Gerente


class SettingServicosGerenteJardinagem(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Gerente = models.ForeignKey(
        to=Gerente,
        null=False,
        blank=False,
        related_name='RGerenteSettingServicosJardinagemGerente',
        on_delete=models.CASCADE,
    )

    NotificationsServicosAtrasados = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationsServicosProximos = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationsServicosEmAndamento = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationsServicosCancelados = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationsServicosAgendados = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationReportProductivity = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationReportServicosAtrasados = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationReportServicosProximos = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationReportServicosEmAndamento = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationReportServicosCancelados = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )


class SettingServicosGerenteLimpezaPredial(models.Model):
    id_random = models.CharField(
        unique=True,
        default=generate_id_random,
        max_length=20
    )

    Gerente = models.ForeignKey(
        to=Gerente,
        null=False,
        blank=False,
        related_name='RGerenteSettingServicosLimpezaPredialGerente',
        on_delete=models.CASCADE,
    )

    NotificationsServicosAtrasados = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationsServicosProximos = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationsServicosEmAndamento = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationsServicosCancelados = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationsServicosAgendados = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationReportProductivity = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationReportServicosAtrasados = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationReportServicosProximos = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationReportServicosEmAndamento = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    NotificationReportServicosCancelados = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )