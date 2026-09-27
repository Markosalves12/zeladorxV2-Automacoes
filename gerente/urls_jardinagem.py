from django.urls import path
from gerente.views_jardinagem import (gerentes_jardinagem, editar_gerente_jardinagem,
                                      alterar_status_gerente_jardinagem,
                                      historico_de_servicos_gerente_jardinagem, IfDeleteGerenteJardinagem, DeleteGerenteJardinagem)


urlpatterns = [
    # rota na raiz do sistema
    path('gerentes-jardinagem/<str:userid>', gerentes_jardinagem, name='gerentes_jardinagem'),
    path(
        'editar-gerente-jardinagem/<str:userid>/<str:id_random>',
        editar_gerente_jardinagem,
        name='editar_gerente_jardinagem'
    ),
    path(
        'alterar-status-gerente-jardinagem/<str:userid>/<str:id_random>/<str:new_status>',
         alterar_status_gerente_jardinagem,
         name='alterar_status_gerente_jardinagem'
    ),
    path(
        'historico-de-servicos-gerente-jardinagem/<str:userid>/<str:id_random>',
        historico_de_servicos_gerente_jardinagem,
        name='historico_de_servicos_gerente_jardinagem'
    ),
    path('delete-gerente-jardinagem/<str:userid>/<str:id_random>/', IfDeleteGerenteJardinagem,
         name='IfDeleteGerenteJardinagem'),
    path('DeleteGerenteJardinagem/<str:id_random>/', DeleteGerenteJardinagem,
         name="DeleteGerenteJardinagem")
]