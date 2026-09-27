from django.urls import path
from settings.views_limpeza_predial import configurar_notificacoes_limpeza_predial


urlpatterns = [
    path('Configurar-notificacoes-limpeza-predial/<str:userid>/', configurar_notificacoes_limpeza_predial,
         name='configurar_notificacoes_limpeza_predial'),
]