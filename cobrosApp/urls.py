from django.urls import path
from . import views

urlpatterns = [
    path('', views.planes_servicios, name='planes_cobros'),
    path('resumen/', views.resumen_cobros, name='resumen_cobros'),
]