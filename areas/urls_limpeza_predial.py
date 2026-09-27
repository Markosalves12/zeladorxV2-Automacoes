from django.urls import path
from areas.views_limpeza_predial import (areas_limpeza_predial, editar_area_limpeza_predial,
                                         areas_associadas_localidades_limpeza_predial,
                                         alterar_status_areas_limpeza_predial, IfDeleteAreasLimpezaPredial,
                                         DeleteAreasLimpezaPredial)

urlpatterns = [
    path('areas-limpeza-predial/<str:userid>', areas_limpeza_predial, name='areas_limpeza_predial'),
    path('editar-area-limpeza_predial/<str:userid>/<str:id_random>', editar_area_limpeza_predial, name='editar_area_limpeza_predial'),
    path('areas-associadas-localidades-limpeza_predial/<str:userid>/<str:id_random>', areas_associadas_localidades_limpeza_predial,
         name='areas_associadas_localidades_limpeza_predial'),
    path('alterar-status-areas-limpeza-predial/<str:userid>/<str:id_random>/<str:new_status>',
         alterar_status_areas_limpeza_predial,
         name='alterar_status_areas_limpeza_predial'
    ),
    path('delete-areas-limpeza-predial/<str:userid>/<str:id_random>/', IfDeleteAreasLimpezaPredial,
         name='IfDeleteAreasLimpezaPredial'),
    path('DeleteAreasLimpezaPredial/<str:id_random>/', DeleteAreasLimpezaPredial, name="DeleteAreasLimpezaPredial")
]