from django.urls import path
from areas.views_areas_jardinagem import (areas_jardins, editar_area_jardins, areas_associadas_localidades_jardinagem,
                                          alterar_status_areas_jardinagem, IfDeleteAreasJardinagem, DeleteAreasJardinagem)

urlpatterns = [
    path('areas-jardins/<str:userid>', areas_jardins, name='areas_jardins'),
    path('editar-area-jardins/<str:userid>/<str:id_random>', editar_area_jardins, name='editar_area_jardins'),
    path('areas-associadas-localidades-jardinagem/<str:userid>/<str:id_random>', areas_associadas_localidades_jardinagem,
         name='areas_associadas_localidades_jardinagem'),
    path('alterar-status-areas-jardinagem/<str:userid>/<str:id_random>/<str:new_status>',
         alterar_status_areas_jardinagem,
         name='alterar_status_areas_jardinagem'
    ),
    path('delete-areas-jardinagem/<str:userid>/<str:id_random>/', IfDeleteAreasJardinagem, name='IfDeleteAreasJardinagem'),
    path('DeleteAreasJardinagem/<str:id_random>/', DeleteAreasJardinagem, name="DeleteAreasJardinagem"),
]