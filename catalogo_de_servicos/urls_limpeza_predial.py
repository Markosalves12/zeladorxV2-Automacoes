from django.urls import path
from catalogo_de_servicos.views_limpeza_predial import (catalogo_de_servicos_limpeza_predial,
                                                        editar_catalogo_de_servicos_limpeza_predial,
                                                        alterar_status_catalogo_de_servicos_limpeza_predial,
                                                        IfDeleteServicoCatalogoLimpezaPredial,
                                                        DeleteServicoCatalogoLimpezaPredial)

urlpatterns = [
    path(
        'catalogo-de-servicos-limpeza-predial/<str:userid>',
        catalogo_de_servicos_limpeza_predial,
        name='catalogo_de_servicos_limpeza_predial'
    ),
    path(
        'editar-catalogo-de-servicos-limpeza-predial/<str:userid>/<str:id_random>',
        editar_catalogo_de_servicos_limpeza_predial,
        name='editar_catalogo_de_servicos_limpeza_predial'
    ),
    path('alterar-status-catalogo-de-servicos-limpeza-predial/<str:userid>/<str:id_random>/<str:new_status>',
         alterar_status_catalogo_de_servicos_limpeza_predial,
         name='alterar_status_catalogo_de_servicos_limpeza_predial'
    ),
    path('delete-catalogo-de-servicos-limpeza-predial/<str:userid>/<str:id_random>/', IfDeleteServicoCatalogoLimpezaPredial,
         name='IfDeleteServicoCatalogoLimpezaPredial'),
    path('DeleteServicoCatalogoLimpezaPredial/<str:id_random>/', DeleteServicoCatalogoLimpezaPredial,
         name="DeleteServicoCatalogoLimpezaPredial")
]
