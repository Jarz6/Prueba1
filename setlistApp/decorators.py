from django.shortcuts import redirect
from django.contrib import messages

def rol_requerido(roles_permitidos=[]):
    """
    Decorador que restringe el acceso a vistas según los grupos del usuario.
    Si es superusuario o pertenece a alguno de los roles permitidos, ingresa.
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            grupos_usuario = request.user.groups.values_list('name', flat=True)
            if any(rol in grupos_usuario for rol in roles_permitidos):
                return view_func(request, *args, **kwargs)

            messages.error(request, "No tienes permisos suficientes para acceder a este módulo.")
            return redirect('dashboard')
        return wrapper
    return decorator