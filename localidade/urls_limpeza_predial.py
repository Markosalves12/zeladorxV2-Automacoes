from django.urls import path
from localidade.views_limpeza_predial import (localidades_limpeza_predial, editar_localidade_limpeza_predial,
                                              alterar_status_localidade_limpeza_predial,
                                              mapa_localidades_limpeza_predial, IfDeleteLocalidadeLimpezaPredial,
                                              DeleteLocalidadeLimpezaPredial)


urlpatterns = [
    path('localidades-limpeza-predial/<str:userid>', localidades_limpeza_predial, name='localidades_limpeza_predial'),
    path(
        'editar-localidade-limpeza-predial/<str:userid>/<str:id_random>',
        editar_localidade_limpeza_predial,
        name='editar_localidade_limpeza_predial'
    ),
    path(
        'alterar-status-localidade-limpeza-predial/<str:userid>/<str:id_random>/<str:new_status>',
        alterar_status_localidade_limpeza_predial,
        name='alterar_status_localidade_limpeza_predial'
    ),
    path('mapa-localidades-limpeza-predial/<str:userid>', mapa_localidades_limpeza_predial, name='mapa_localidades_limpeza_predial'),
    path('delete-localidade-limpeza-predial/<str:userid>/<str:id_random>/', IfDeleteLocalidadeLimpezaPredial,
         name='IfDeleteLocalidadeLimpezaPredial'),
    path('DeleteLocalidadeLimpezaPredial/<str:id_random>/', DeleteLocalidadeLimpezaPredial,
         name="DeleteLocalidadeLimpezaPredial")
]