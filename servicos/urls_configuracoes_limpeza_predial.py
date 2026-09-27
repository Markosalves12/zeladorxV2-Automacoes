from django.urls import path
from servicos.views_configuracoes_limpeza_predial import (configurar_servico_limpeza_predial,
                                                          servicos_configurados_limpeza_predial,
                                                          editar_servico_limpezapredial_configurado,
                                                          alterar_status_servico_limpezapredial_configurado,
                                                          historico_de_servicos_configurados_limpeza_predial,
                                                          IfDeleteServicoLimpezaPredialConfigurado,
                                                          DeleteServicoLimpezaPredialConfigurado)

urlpatterns = [
    path(
        'configurar-servico-limpeza-predial/<str:userid>',
         configurar_servico_limpeza_predial,
         name='configurar_servico_limpeza_predial'
    ),
    path(
        'editar-servico-limpezapredial-configurado/<str:userid>/<str:id_random>',
         editar_servico_limpezapredial_configurado,
         name='editar_servico_limpezapredial_configurado'
    ),
    path(
        'servicos-configurados-limpeza-predial/<str:userid>',
         servicos_configurados_limpeza_predial,
         name='servicos_configurados_limpeza_predial'
    ),
    path('alterar-status-servico-limpezapredial-configurado/<str:userid>/<str:id_random>/<str:new_status>',
         alterar_status_servico_limpezapredial_configurado,
         name='alterar_status_servico_limpezapredial_configurado'
    ),
    path(
        'historico-de-servicos-configurados-limpeza-predial/<str:userid>/<str:id_random>',
        historico_de_servicos_configurados_limpeza_predial,
        name='historico_de_servicos_configurados_limpeza_predial'
    ),
    path(
        'delete-servico-limpeza-predial-configurado/<str:userid>/<str:id_random>/',
        IfDeleteServicoLimpezaPredialConfigurado,
        name='IfDeleteServicoLimpezaPredialConfigurado'
    ),
    path(
        'DeleteServicoLimpezaPredialConfigurado/<str:id_random>/',
        DeleteServicoLimpezaPredialConfigurado,
        name="DeleteServicoLimpezaPredialConfigurado"
    )
]