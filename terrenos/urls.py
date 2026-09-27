from django.urls import path
from terrenos.views import (terrenos, editar_terreno, alterar_status_terreno, areas_associadas_terrenos,
                            IfDeleteTerreno, DeleteTerreno)

urlpatterns = [
    path('terrenos/<str:userid>', terrenos, name='terrenos'),
    path('editar-terreno/<str:userid>/<str:id_random>', editar_terreno, name='editar_terreno'),
    path(
        'alterar-status-terreno/<str:userid>/<str:id_random>/<str:new_status>',
        alterar_status_terreno,
        name='alterar_status_terreno'
    ),
    path(
        'areas-associadas-terrenos/<str:userid>/<str:id_random>',
        areas_associadas_terrenos,
        name='areas_associadas_terrenos'
    ),

    path(
        'delete-terreno/<str:userid>/<str:id_random>/',
        IfDeleteTerreno,
        name='IfDeleteTerreno'
    ),
    path(
        'DeleteTerreno/<str:id_random>/',
        DeleteTerreno,
        name="DeleteTerreno"
    )
]