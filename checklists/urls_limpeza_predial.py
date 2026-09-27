from django.urls import path
from checklists.views_limpeza_predial import (checklists_limpeza_predial, editar_checklist_limpeza_predial,
                                              view_detailing_checklists_limpeza_predial,
                                              IfDeleteCheckListLimpezaPredial, DeleteCheckLimpezaPredial)


urlpatterns = [
    path(
        'checklists-limpeza-predial/<str:userid>/<str:id_random>/',
        checklists_limpeza_predial,
        name='checklists_limpeza_predial'
    ),
    path(
        'detalhamento-checklists-servico-limpeza-predial/<str:userid>/<str:id_random>/',
        view_detailing_checklists_limpeza_predial,
        name='view_detailing_checklists_limpeza_predial'
    ),
    path(
        'editar-checklist-limpeza-predial/<str:userid>/<str:id_random>',
        editar_checklist_limpeza_predial,
        name='editar_checklist_limpeza_predial'
    ),
    path('delete-checklist-limpeza-predial/<str:userid>/<str:id_random>/', IfDeleteCheckListLimpezaPredial,
         name='IfDeleteCheckListLimpezaPredial'),
    path('DeleteCheckLimpezaPredial/<str:id_random>/', DeleteCheckLimpezaPredial,
         name="DeleteCheckLimpezaPredial")
]