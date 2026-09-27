from django.urls import path
from localidade.views_jardinagem import (localidades_jardinagem, editar_localidade_jardinagem,
                                         alterar_status_localidade_jardinagem, mapa_localidades_jardinagem,
                                         IfDeleteLocalidadeJardinagem, DeleteLocalidadeJardinagem)


urlpatterns = [
    path('localidades-jardinagem/<str:userid>', localidades_jardinagem, name='localidades_jardinagem'),
    path(
        'editar-localidade-jardinagem/<str:userid>/<str:id_random>',
        editar_localidade_jardinagem,
        name='editar_localidade_jardinagem'
    ),
    path(
        'alterar-status-localidade-jardinagem/<str:userid>/<str:id_random>/<str:new_status>',
        alterar_status_localidade_jardinagem,
        name='alterar_status_localidade_jardinagem'
    ),
    path('mapa-localidades-jardinagem/<str:userid>', mapa_localidades_jardinagem, name='mapa_localidades_jardinagem'),
    path('delete-localidade-jardinagem/<str:userid>/<str:id_random>/', IfDeleteLocalidadeJardinagem,
         name='IfDeleteLocalidadeJardinagem'),
    path('IfDeleteLocalidadeJardinagem/<str:id_random>/', DeleteLocalidadeJardinagem,
         name="DeleteLocalidadeJardinagem")
]