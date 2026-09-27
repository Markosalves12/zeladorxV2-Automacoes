from django.urls import path
from gerente.views_limpeza_predial import (gerentes_limpeza_predial, editar_gerente_limpeza_predial,
                                           alterar_status_gerente_limpeza_predial,
                                           historico_de_servicos_gerente_limpeza_predial,
                                           IfDeleteGerenteLimpezaPredial, DeleteGerenteLimpezaPredial)


urlpatterns = [
    # rota na raiz do sistema
    path('gerentes-limpeza-predial/<str:userid>', gerentes_limpeza_predial, name='gerentes_limpeza_predial'),
    path(
        'editar-gerente-limpeza-predial/<str:userid>/<str:id_random>',
        editar_gerente_limpeza_predial,
        name='editar_gerente_limpeza_predial'
    ),
    path(
        'alterar-status-gerente-limpeza-predial/<str:userid>/<str:id_random>/<str:new_status>',
        alterar_status_gerente_limpeza_predial,
        name='alterar_status_gerente_limpeza_predial'
    ),
    path(
        'historico-de-servicos-gerente-limpeza-predial/<str:userid>/<str:id_random>',
        historico_de_servicos_gerente_limpeza_predial,
        name='historico_de_servicos_gerente_limpeza_predial'
    ),
    path('delete-gerente-limpeza-predial/<str:userid>/<str:id_random>/', IfDeleteGerenteLimpezaPredial,
         name='IfDeleteGerenteLimpezaPredial'),
    path('DeleteGerenteLimpezaPredial/<str:id_random>/', DeleteGerenteLimpezaPredial,
         name="DeleteGerenteLimpezaPredial")
]