from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio_setlist'),
    path('bandas/', views.lista_bandas, name='lista_bandas'),
]