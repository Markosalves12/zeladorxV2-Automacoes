from django.urls import path
from notifications.views_limpeza_predial import (send_notification_servicos_atrasados_limpeza_predial, send_notification_servicos_proximos_limpeza_predial,
                                            send_notification_servicos_em_andamento_limpeza_predial)


urlpatterns = [
    path(
        'send_notification_servicos_atrasados_limpeza_predial/',
        send_notification_servicos_atrasados_limpeza_predial,
        name='send_notification_servicos_atrasados_limpeza_predial'
    ),
    path(
        'send_notification_servicos_proximos_limpeza_predial/',
        send_notification_servicos_proximos_limpeza_predial,
        name='send_notification_servicos_proximos_limpeza_predial'
    ),
    path(
        'send_notification_servicos_em_andamento_limpeza_predial/',
        send_notification_servicos_em_andamento_limpeza_predial,
        name='send_notification_servicos_em_andamento_limpeza_predial'
    ),
]