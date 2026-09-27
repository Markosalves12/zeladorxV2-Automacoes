from django.urls import path
from medidor.views import medidor_upload
from medidor.utils import processar_poligonos

urlpatterns = [
    path('Dimensionador/<str:userid>/', medidor_upload, name='medidor_upload'),
    path('processar_poligonos/<str:id_random>/', processar_poligonos, name='processar_poligonos'),
]