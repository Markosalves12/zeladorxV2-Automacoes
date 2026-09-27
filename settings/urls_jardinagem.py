from django.urls import path
from settings.views_jardinagem import configurar_notificacoes_jardinagem
from settings.views_gerals import force_configuracoes


urlpatterns = [
    path('force_configuracoes/<str:userid>/', force_configuracoes, name='force_configuracoes'),
    path('Configurar-notificacoes-jardinagem/<str:userid>/', configurar_notificacoes_jardinagem,
         name='configurar_notificacoes_jardinagem'),
]