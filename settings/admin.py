from django.contrib import admin
from settings.models import  SettingServicosGerenteLimpezaPredial, SettingServicosGerenteJardinagem


# Register your models here.
class SettingServicosGerenteLimpezaPredialAdmin(admin.ModelAdmin):
    list_display = ('id', 'Gerente','NotificationsServicosAtrasados', 'NotificationsServicosProximos',
                    'NotificationsServicosEmAndamento','NotificationsServicosCancelados',
                    'NotificationsServicosAgendados', 'NotificationReportProductivity',
                    'NotificationReportServicosAtrasados', 'NotificationReportServicosProximos',
                    'NotificationReportServicosEmAndamento','NotificationReportServicosCancelados')

    list_display_links = ('id', 'Gerente','NotificationsServicosAtrasados', 'NotificationsServicosProximos',
                    'NotificationsServicosEmAndamento','NotificationsServicosCancelados',
                    'NotificationsServicosAgendados', 'NotificationReportProductivity',
                    'NotificationReportServicosAtrasados', 'NotificationReportServicosProximos',
                    'NotificationReportServicosEmAndamento','NotificationReportServicosCancelados')

    search_fields = ('id', 'Gerente','NotificationsServicosAtrasados', 'NotificationsServicosProximos',
                    'NotificationsServicosEmAndamento','NotificationsServicosCancelados',
                    'NotificationsServicosAgendados', 'NotificationReportProductivity',
                    'NotificationReportServicosAtrasados', 'NotificationReportServicosProximos',
                    'NotificationReportServicosEmAndamento','NotificationReportServicosCancelados')

    list_filter = ('id', 'Gerente','NotificationsServicosAtrasados', 'NotificationsServicosProximos',
                    'NotificationsServicosEmAndamento','NotificationsServicosCancelados',
                    'NotificationsServicosAgendados', 'NotificationReportProductivity',
                    'NotificationReportServicosAtrasados', 'NotificationReportServicosProximos',
                    'NotificationReportServicosEmAndamento','NotificationReportServicosCancelados')

    list_per_page = 20


class SettingServicosGerenteJardinagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'Gerente', 'NotificationsServicosAtrasados', 'NotificationsServicosProximos',
                    'NotificationsServicosEmAndamento', 'NotificationsServicosCancelados',
                    'NotificationsServicosAgendados', 'NotificationReportProductivity',
                    'NotificationReportServicosAtrasados', 'NotificationReportServicosProximos',
                    'NotificationReportServicosEmAndamento', 'NotificationReportServicosCancelados')

    list_display_links = ('id', 'Gerente', 'NotificationsServicosAtrasados', 'NotificationsServicosProximos',
                          'NotificationsServicosEmAndamento', 'NotificationsServicosCancelados',
                          'NotificationsServicosAgendados', 'NotificationReportProductivity',
                          'NotificationReportServicosAtrasados', 'NotificationReportServicosProximos',
                          'NotificationReportServicosEmAndamento', 'NotificationReportServicosCancelados')

    search_fields = ('id', 'Gerente', 'NotificationsServicosAtrasados', 'NotificationsServicosProximos',
                     'NotificationsServicosEmAndamento', 'NotificationsServicosCancelados',
                     'NotificationsServicosAgendados', 'NotificationReportProductivity',
                     'NotificationReportServicosAtrasados', 'NotificationReportServicosProximos',
                     'NotificationReportServicosEmAndamento', 'NotificationReportServicosCancelados')

    list_filter = ('id', 'Gerente', 'NotificationsServicosAtrasados', 'NotificationsServicosProximos',
                   'NotificationsServicosEmAndamento', 'NotificationsServicosCancelados',
                   'NotificationsServicosAgendados', 'NotificationReportProductivity',
                   'NotificationReportServicosAtrasados', 'NotificationReportServicosProximos',
                   'NotificationReportServicosEmAndamento', 'NotificationReportServicosCancelados')

    list_per_page = 20


admin.site.register(SettingServicosGerenteLimpezaPredial, SettingServicosGerenteLimpezaPredialAdmin)
admin.site.register(SettingServicosGerenteJardinagem, SettingServicosGerenteJardinagemAdmin)