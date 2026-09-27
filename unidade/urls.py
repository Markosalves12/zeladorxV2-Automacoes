from django.urls import path
from unidade.views import unidades, editar_unidade, alterar_status_unidade, IfDeleteUnidade, DeleteUnidade
from unidade.maps_jardinagem import visualizar_unidade_jardinagem
from unidade.maps_limpeza_predial import visualizar_unidade_limpeza_predial


urlpatterns = [
    # rota na raiz do sistema
    path('unidades/<str:userid>', unidades, name='unidades'),
    path('editar-unidade/<str:userid>/<str:id_random>', editar_unidade, name='editar_unidade'),
    path('visualizar-unidade-jardinagem/<str:userid>/<str:id_random>',
         visualizar_unidade_jardinagem, name='visualizar_unidade_jardinagem'),
    path('visualizar-unidade-limpeza-predial/<str:userid>/<str:id_random>',
         visualizar_unidade_limpeza_predial, name='visualizar_unidade_limpeza_predial'),
    path(
        'alterar-status-unidade/<str:userid>/<str:id_random>/<str:new_status>',
        alterar_status_unidade,
        name='alterar_status_unidade'
    ),
    path(
        'delete-unidade/<str:userid>/<str:id_random>/',
        IfDeleteUnidade,
        name='IfDeleteUnidade'
    ),
    path(
        'DeleteUnidade/<str:id_random>/',
        DeleteUnidade,
        name="DeleteUnidade"
    )
]