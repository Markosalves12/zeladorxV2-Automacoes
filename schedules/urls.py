from django.urls import path
from schedules.views import force_updates

urlpatterns = [
    path('force_updates/', force_updates, name='force_updates'),
]