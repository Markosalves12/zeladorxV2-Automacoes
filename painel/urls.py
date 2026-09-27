from django.urls import path

from painel import views

app_name = 'painel'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('entrar/', views.Login.as_view(), name='login'),
    path('sair/', views.sair, name='sair'),
    path('rotinas/', views.rotinas, name='rotinas'),
    path('rotinas/<int:pk>/alternar/', views.alternar_rotina, name='alternar_rotina'),
    path('rotinas/<int:pk>/horario/', views.horario_rotina, name='horario_rotina'),
    path('rotinas/<int:pk>/executar/', views.executar_rotina, name='executar_rotina'),
    path('execucoes/', views.execucoes, name='execucoes'),
    path('execucoes/<int:pk>/', views.execucao_detalhe, name='execucao_detalhe'),
    path('notificacoes/', views.notificacoes, name='notificacoes'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]
