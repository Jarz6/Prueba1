from django.urls import path
from django.contrib.auth import views as auth_views
from setlistApp import views

urlpatterns = [
    # Inicio y Redirección
    path('', views.dashboard_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Autenticación Propia
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Recuperación de Contraseña mediante Correo
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),

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