from django.urls import path
from permissionscontrol.views_especials import permissions_especials, editar_permissoes_especials

urlpatterns = [
    path('permissions-especials/<str:userid>', permissions_especials, name='permissions_especials'),
    path('editar-permissoes-especials/<str:userid>/<str:id_random>', editar_permissoes_especials, name='editar_permissoes_especials'),
]