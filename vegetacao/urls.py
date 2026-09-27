from django.urls import path
from vegetacao.views import (vegetacao, editar_vegetacao, alterar_status_vegetacao, areas_associadas_vegetacao,
                             IfDeleteCatalogoVegetacao, DeleteCatalogoVegetacao)

urlpatterns = [
    path('vegetacao/<str:userid>', vegetacao, name='vegetacao'),
    path('editar-vegetacao/<str:userid>/<str:id_random>', editar_vegetacao, name='editar_vegetacao'),
    path(
        'alterar-status-vegetacao/<str:userid>/<str:id_random>/<str:new_status>',
        alterar_status_vegetacao,
        name='alterar_status_vegetacao'
    ),
    path(
        'areas-associadas-vegetacao/<str:userid>/<str:id_random>',
        areas_associadas_vegetacao,
        name='areas_associadas_vegetacao'
    ),
    path(
        'delete-vegetacao/<str:userid>/<str:id_random>/',
        IfDeleteCatalogoVegetacao,
        name='IfDeleteCatalogoVegetacao'
    ),
    path(
        'DeleteUnidade/<str:id_random>/',
        DeleteCatalogoVegetacao,
        name="DeleteCatalogoVegetacao"
    )
]