from django.urls import path
from notifications.views_jardinagem import (send_notification_servicos_atrasados_jardinagem, send_notification_servicos_proximos_jardinagem,
                                            send_notification_servicos_em_andamento_jardinagem, send_notificaton_retorno_proximo,
                                            send_notificaton_retorno_atrasado)


urlpatterns = [
    path(
        'send_notification_servicos_atrasados_jardinagem/',
        send_notification_servicos_atrasados_jardinagem,
        name='send_notification_servicos_atrasados_jardinagem'
    ),
    path(
        'send_notification_servicos_proximos_jardinagem/',
        send_notification_servicos_proximos_jardinagem,
        name='send_notification_servicos_proximos_jardinagem'
    ),
    path(
        'send_notification_servicos_em_andamento_jardinagem/',
        send_notification_servicos_em_andamento_jardinagem,
        name='send_notification_servicos_em_andamento_jardinagem'
    ),
    path(
        'send_notificaton_retorno_proximo/',
        send_notificaton_retorno_proximo,
        name='send_notificaton_retorno_proximo'
    ),
    path(
        'send_notificaton_retorno_atrasado/',
        send_notificaton_retorno_atrasado,
        name='send_notificaton_retorno_atrasado'
    ),
]