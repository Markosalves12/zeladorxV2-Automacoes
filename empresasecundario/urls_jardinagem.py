from django.urls import path
from empresasecundario.views_jardinagem import (empresas_jardinagem, editar_empresa_jardinagem,
                                                alterar_status_empresa_jardinagem,
                                                IfDeleteEmpresaSecundariaJardinagem,
                                                DeleteEmpresaSecundariaJardinagem)

urlpatterns = [
    path('empresas-jardinagem/<str:userid>', empresas_jardinagem, name='empresas_jardinagem'),
    path(
        'editar-empresa-jardinagem/<str:userid>/<str:id_random>/',
        editar_empresa_jardinagem,
        name='editar_empresa_jardinagem'
    ),
    path('alterar-status-empresa-jardinagem/<str:userid>/<str:id_random>/<str:new_status>',
         alterar_status_empresa_jardinagem,
         name='alterar_status_empresa_jardinagem'
    ),
    path('delete-empresa-jardinagem/<str:userid>/<str:id_random>/', IfDeleteEmpresaSecundariaJardinagem,
         name='IfDeleteEmpresaSecundariaJardinagem'),
    path('DeleteEmpresaSecundariaJardinagem/<str:id_random>/', DeleteEmpresaSecundariaJardinagem,
         name="DeleteEmpresaSecundariaJardinagem")
]