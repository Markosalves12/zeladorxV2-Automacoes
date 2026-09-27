from django.shortcuts import render, redirect
from gerente.models import Gerente
from settings.models import SettingServicosGerenteJardinagem, SettingServicosGerenteLimpezaPredial
from permissionscontrol.utils import verify_login

def force_configuracoes(request, userid):
    block = verify_login(request=request, userid=userid)

    if block == True:
        return redirect('logout')

    objects = Gerente.objects.all()

    for gerente in objects:
        # Configuração para Jardinagem
        configurate_jardinagem, created = SettingServicosGerenteJardinagem.objects.get_or_create(
            Gerente=gerente,
            defaults={
                'NotificationsServicosAtrasados': False,
                'NotificationsServicosProximos': False,
                'NotificationsServicosEmAndamento': False,
                'NotificationsServicosCancelados': False,
                'NotificationsServicosAgendados': False,
                'NotificationReportProductivity': False,
                'NotificationReportServicosAtrasados': False,
                'NotificationReportServicosProximos': False,
                'NotificationReportServicosEmAndamento': False,
                'NotificationReportServicosCancelados': False,
            }
        )
        if not created:  # Se já existia, sobrescrevemos com os valores padrão
            configurate_jardinagem.NotificationsServicosAtrasados = False
            configurate_jardinagem.NotificationsServicosProximos = False
            configurate_jardinagem.NotificationsServicosEmAndamento = False
            configurate_jardinagem.NotificationsServicosCancelados = False
            configurate_jardinagem.NotificationsServicosAgendados = False
            configurate_jardinagem.NotificationReportProductivity = False
            configurate_jardinagem.NotificationReportServicosAtrasados = False
            configurate_jardinagem.NotificationReportServicosProximos = False
            configurate_jardinagem.NotificationReportServicosEmAndamento = False
            configurate_jardinagem.NotificationReportServicosCancelados = False
            configurate_jardinagem.save()

        # Configuração para Limpeza Predial
        configurate_limpeza_predial, created = SettingServicosGerenteLimpezaPredial.objects.get_or_create(
            Gerente=gerente,
            defaults={
                'NotificationsServicosAtrasados': False,
                'NotificationsServicosProximos': False,
                'NotificationsServicosEmAndamento': False,
                'NotificationsServicosCancelados': False,
                'NotificationsServicosAgendados': False,
                'NotificationReportProductivity': False,
                'NotificationReportServicosAtrasados': False,
                'NotificationReportServicosProximos': False,
                'NotificationReportServicosEmAndamento': False,
                'NotificationReportServicosCancelados': False,
            }
        )
        if not created:  # Se já existia, sobrescrevemos com os valores padrão
            configurate_limpeza_predial.NotificationsServicosAtrasados = False
            configurate_limpeza_predial.NotificationsServicosProximos = False
            configurate_limpeza_predial.NotificationsServicosEmAndamento = False
            configurate_limpeza_predial.NotificationsServicosCancelados = False
            configurate_limpeza_predial.NotificationsServicosAgendados = False
            configurate_limpeza_predial.NotificationReportProductivity = False
            configurate_limpeza_predial.NotificationReportServicosAtrasados = False
            configurate_limpeza_predial.NotificationReportServicosProximos = False
            configurate_limpeza_predial.NotificationReportServicosEmAndamento = False
            configurate_limpeza_predial.NotificationReportServicosCancelados = False
            configurate_limpeza_predial.save()

    return render(
        request,
        'DataTableAndForms/DataTableAndForms.html'
    )