from django.urls import path
from servicos.views_limpeza_predial import (agendar_servico_limpeza_predial, servicos_agendados_limpeza_predial,
                                            editar_servico_limpeza_predial_agendado,
                                            realizar_servico_limpeza_predial_agendado,
                                            cancelar_servico_limpeza_predial, concluir_servico_limpeza_predial,
                                            view_detailing_limpeza_predial,
                                            IfDeleteServicoAgendadoLimpezaPredial,
                                            DeleteServicoAgendadoLimpezaPredial)

urlpatterns = [
    path(
        'agendar-servico-limpeza-predial/<str:type>/<str:userid>',
        agendar_servico_limpeza_predial,
        name='agendar_servico_limpeza_predial'
    ),
    path(
        'servicos-agendados-limpeza-predial/<str:userid>',
        servicos_agendados_limpeza_predial,
        name='servicos_agendados_limpeza_predial'
    ),
    path(
        'editar-servico-limpeza-predial-agendado/<str:userid>/<str:id_random>',
        editar_servico_limpeza_predial_agendado,
        name='editar_servico_limpeza_predial_agendado'
    ),
    path(
        'realizar-servico-limpeza-predial-agendado/<str:type>/<str:userid>/<str:id_random>',
        realizar_servico_limpeza_predial_agendado,
        name='realizar_servico_limpeza_predial_agendado'
    ),
    path(
        'cancelar-servico-limpeza-predial/<str:userid>/<str:id_random>/<str:type>',
        cancelar_servico_limpeza_predial,
         name='cancelar_servico_limpeza_predial'),
    path(
        'concluir-servico-limpeza-predial/<str:userid>/<str:id_random>/<str:type>',
        concluir_servico_limpeza_predial,
         name='concluir_servico_limpeza_predial'
    ),

    path(
        'detalhamento-servico-limpeza-predial/<str:userid>/<str:id_random>',
        view_detailing_limpeza_predial,
        name='view_detailing_limpeza_predial'
    ),

    path(
        'delete-servico-limpeza-predial-agendado/<str:userid>/<str:id_random>/',
        IfDeleteServicoAgendadoLimpezaPredial,
        name='IfDeleteServicoAgendadoLimpezaPredial'
    ),
    path(
        'DeleteServicoAgendadoLimpezaPredial/<str:id_random>/',
        DeleteServicoAgendadoLimpezaPredial,
        name="DeleteServicoAgendadoLimpezaPredial"
    )
]