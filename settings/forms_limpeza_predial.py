from django import forms
from settings.models import SettingServicosGerenteLimpezaPredial
from empresasecundario.utils import define_empresas

class SettingServicosGerenteLimpezaPredialForms(forms.ModelForm):
    def __init__(self, *args, request, userid=str, type='creat/edit', **kwargs):
        super(SettingServicosGerenteLimpezaPredialForms, self).__init__(*args, **kwargs)
        empresas = define_empresas(request=request, userid=userid)
        empresas_primarias_ids = empresas['empresas_primarias_ids']
        empresas_secundarias_ids = empresas['empresas_secundarias_ids']

        self.fields['Gerente'].queryset = self.fields['Gerente'].queryset.filter(
            id_random=userid
        )

    class Meta:
        model = SettingServicosGerenteLimpezaPredial
        fields = [
            'Gerente',
            'NotificationsServicosAtrasados', 'NotificationsServicosProximos', 'NotificationsServicosEmAndamento',
            'NotificationsServicosCancelados', 'NotificationsServicosAgendados', 'NotificationReportProductivity',
            'NotificationReportServicosAtrasados', 'NotificationReportServicosProximos',
            'NotificationReportServicosEmAndamento','NotificationReportServicosCancelados'
        ]

        labels = {
            'NotificationsServicosAtrasados': 'Receber notificação de serviços atrasados?',
            'NotificationsServicosProximos': 'Receber notificação de serviços próximos?',
            'NotificationsServicosEmAndamento': 'Receber notificação de serviços em andamento?',
            'NotificationsServicosCancelados': 'Receber notificação de serviços cancelados?',
            'NotificationsServicosAgendados': 'Receber notificação de serviços agendados?',
            'NotificationReportProductivity': 'Receber relatórios de produtividade? (por e-mail)',
            'NotificationReportServicosAtrasados': 'Receber relatórios de serviços atrasados? (por e-mail)',
            'NotificationReportServicosProximos': 'Receber relatórios de serviços próximos? (por e-mail)',
            'NotificationReportServicosEmAndamento': 'Receber relatórios de serviços em andamento? (por e-mail)',
            'NotificationReportServicosCancelados': 'Receber relatórios de serviços cancelados? (por e-mail)',
        }

        widgets = {
            'Gerente': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationsServicosAtrasados': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationsServicosProximos': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationsServicosEmAndamento': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationsServicosCancelados': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationsServicosAgendados': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationReportProductivity': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationReportServicosAtrasados': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationReportServicosProximos': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationReportServicosEmAndamento': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
            'NotificationReportServicosCancelados': forms.NullBooleanSelect(
                attrs={
                    'class': 'form-control'
                }
            ),
        }