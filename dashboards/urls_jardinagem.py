from django.urls import path
from dashboards.views_jardinagem import dashboard_produtividade_jardinagem
from dashboards.views_adm_jardinagem import dashboard_administrativo_jardinagem


urlpatterns = [
    # rota na raiz do sistema
    path(
        'dashboard-gerencial-jardinagem/<userid>',
        dashboard_produtividade_jardinagem,
        name='dashboard_produtividade_jardinagem'
    ),
    path(
        'dashboard-administrativo-jardinagem/<userid>',
        dashboard_administrativo_jardinagem,
        name='dashboard_administrativo_jardinagem'
    ),
]