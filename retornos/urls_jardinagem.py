from django.urls import path
from retornos.views_jardinagem import tempo_desde_ultimo_atendimento_jardinagem

urlpatterns = [
    path('tempo-desde-ultimo-atendimento-jardinagem/<str:userid>',
         tempo_desde_ultimo_atendimento_jardinagem,
         name='tempo_desde_ultimo_atendimento_jardinagem'),
]