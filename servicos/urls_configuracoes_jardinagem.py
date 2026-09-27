from django.urls import path
from servicos.views_configuracoes_jardinagem import (configurar_servico_jardinagem,
                                                     servicos_configurados_jardinagem,
                                                     editar_servico_jardinagem_configurado,
                                                     alterar_status_servico_jardinagem_configurado,
                                                     historico_de_servicos_configurados_jardinagem,
                                                     IfDeleteServicoJardinagemConfigurado,
                                                     DeleteServicoJardinagemConfigurado)

urlpatterns = [
    path(
        'configurar-servico-jardinagem/<str:userid>',
         configurar_servico_jardinagem,
         name='configurar_servico_jardinagem'
    ),
    path(
        'editar-servico-jardinagem-configurado/<str:userid>/<str:id_random>',
         editar_servico_jardinagem_configurado,
         name='editar_servico_jardinagem_configurado'
    ),
    path(
        'servicos-configurados-jardinagem/<str:userid>',
         servicos_configurados_jardinagem,
         name='servicos_configurados_jardinagem'
    ),
    path('alterar-status-servico-jardinagem-configurado/<str:userid>/<str:id_random>/<str:new_status>',
         alterar_status_servico_jardinagem_configurado,
         name='alterar_status_servico_jardinagem_configurado'
    ),
    path(
        'historico-de-servicos-configurados-jardinagem/<str:userid>/<str:id_random>',
        historico_de_servicos_configurados_jardinagem,
        name='historico_de_servicos_configurados_jardinagem'
    ),
    path(
        'delete-servico-jardinagem-configurado/<str:userid>/<str:id_random>/',
        IfDeleteServicoJardinagemConfigurado,
        name='IfDeleteServicoJardinagemConfigurado'
    ),
    path(
        'DeleteServicoJardinagemConfigurado/<str:id_random>/',
        DeleteServicoJardinagemConfigurado,
        name="DeleteServicoJardinagemConfigurado"
    )
]