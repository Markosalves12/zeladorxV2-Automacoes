from django.urls import path
from checklists.views_jardinagem import (checklists_jardinagem, editar_checklist_jardinagem,
                                         view_detailing_checklists_jardinagem, IfDeleteCheckListJardins,
                                         DeleteCheckListJardins)


urlpatterns = [
    path('checklists-jardinagem/<str:userid>/<str:id_random>/', checklists_jardinagem, name='checklists_jardinagem'),
    path(
        'detalhamento-checklists-servico-jardinagem/<str:userid>/<str:id_random>/',
        view_detailing_checklists_jardinagem,
        name='view_detailing_checklists_jardinagem'
    ),
    path(
        'editar-checklist-jardinagem/<str:userid>/<str:id_random>',
        editar_checklist_jardinagem,
        name='editar_checklist_jardinagem'
    ),
    path('delete-checklist-jardinagem/<str:userid>/<str:id_random>/', IfDeleteCheckListJardins,
         name='IfDeleteCheckListJardins'),
    path('DeleteCheckListJardins/<str:id_random>/', DeleteCheckListJardins,
         name="DeleteCheckListJardins")
]