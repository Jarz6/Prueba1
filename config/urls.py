from django.urls import path
from setlistApp import views

urlpatterns = [
    # Inicio y Redirección
    path('', views.dashboard_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Autenticación y Registro
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),

    # Recuperación de Contraseña mediante Código de Seguridad (OTP)
    path('recuperar/', views.recuperar_solicitar_view, name='password_reset'),
    path('recuperar/verificar/', views.recuperar_verificar_view, name='recuperar_verificar'),

    # Mantenedor 1: Bandas
    path('bandas/', views.lista_bandas, name='bandas_lista'),
    path('bandas/crear/', views.crear_banda, name='crear_banda'),
    path('bandas/editar/<int:pk>/', views.editar_banda, name='editar_banda'),
    path('bandas/eliminar/<int:pk>/', views.eliminar_banda, name='eliminar_banda'),

    # Mantenedor 2: Tarifas
    path('tarifas/', views.lista_tarifas, name='tarifas_lista'),
    path('tarifas/crear/', views.crear_tarifa, name='crear_tarifa'),
    path('tarifas/editar/<int:pk>/', views.editar_tarifa, name='editar_tarifa'),
    path('tarifas/eliminar/<int:pk>/', views.eliminar_tarifa, name='eliminar_tarifa'),

    # Transacción Operacional
    path('transacciones/ticket/', views.transaccion_ticket, name='transaccion_ticket'),

    # Canciones asociadas a una Banda
    path('bandas/<int:pk>/canciones/', views.detalle_canciones_banda, name='detalle_canciones_banda'),
    path('canciones/eliminar/<int:pk>/', views.eliminar_cancion, name='eliminar_cancion'),

    # Crear Género / Estilo
    path('estilos/crear/', views.crear_estilo, name='crear_estilo'),
]