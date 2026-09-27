from django.urls import path
from empresasecundario.views_limpeza_predial import (empresas_limpeza_predial, editar_empresa_limpeza_predial,
                                                     alterar_status_empresa_limpeza_predial,
                                                     IfDeleteEmpresaSecundariaLimpezaPredial,
                                                     DeleteEmpresaSecundariaLimpezaPredial)

urlpatterns = [
    path('empresas-limpeza-predial/<str:userid>', empresas_limpeza_predial, name='empresas_limpeza_predial'),
    path(
        'editar-empresa-limpeza-predial/<str:userid>/<str:id_random>/',
        editar_empresa_limpeza_predial,
        name='editar_empresa_limpeza_predial'
    ),
    path('alterar-status-empresa-limpeza-predial/<str:userid>/<str:id_random>/<str:new_status>',
         alterar_status_empresa_limpeza_predial,
         name='alterar_status_empresa_limpeza_predial'
         ),
    path('delete-empresa-limpeza-predial/<str:userid>/<str:id_random>/', IfDeleteEmpresaSecundariaLimpezaPredial,
         name='IfDeleteEmpresaSecundariaLimpezaPredial'),
    path('DeleteEmpresaSecundariaLimpezaPredial/<str:id_random>/', DeleteEmpresaSecundariaLimpezaPredial,
         name="DeleteEmpresaSecundariaLimpezaPredial")
]