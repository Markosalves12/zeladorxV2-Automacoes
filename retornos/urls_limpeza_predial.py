from django.urls import path
from retornos.views_limpeza_predial import tempo_desde_ultimo_atendimento_limpeza_predial

urlpatterns = [
    path('tempo-desde-ultimo-atendimento-limpeza-predial/<str:userid>',
         tempo_desde_ultimo_atendimento_limpeza_predial,
         name='tempo_desde_ultimo_atendimento_limpeza_predial'),
]