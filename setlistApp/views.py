import uuid
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.db.models import Count
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.conf import settings

from .forms import BandaForm, TarifaForm, TicketForm, CancionForm, EstiloForm, RegistroUsuarioForm, SolicitarCodigoForm, VerificarCodigoYCambiarClaveForm
from .models import Banda, Cancion, Estilo
from .forms import BandaForm, TarifaForm, TicketForm
from .decorators import rol_requerido
from cobrosApp.models import TarifaRocola, TicketReproduccion
from .forms import BandaForm, TarifaForm, TicketForm, CancionForm, EstiloForm

# --- AUTENTICACIÓN PROPIA ---
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# --- DASHBOARD DIFERENCIADO POR PERFIL ---
@login_required
def dashboard_view(request):
    usuario = request.user
    es_admin = usuario.is_superuser or usuario.groups.filter(name='Administrador').exists()
    es_supervisor = usuario.groups.filter(name='Supervisor').exists()
    es_administrativo = usuario.groups.filter(name='Administrativo').exists()

    metricas = {
        'total_bandas': Banda.objects.count(),
        'total_tarifas': TarifaRocola.objects.count(),
        'total_tickets': TicketReproduccion.objects.count(),
        'promedio_tarifa': TarifaRocola.objects.aggregate(Avg('precio_base'))['precio_base__avg'] or 0,
    }

    context = {
        'es_admin': es_admin,
        'es_supervisor': es_supervisor,
        'es_administrativo': es_administrativo,
        'metricas': metricas,
        'tickets_recientes': TicketReproduccion.objects.select_related('cancion', 'tarifa', 'usuario').order_by('-fecha_solicitud')[:5],
    }
    return render(request, 'dashboard/dashboard.html', context)

# --- MANTENEDOR 1: BANDAS (CRUD) ---
@login_required
@rol_requerido(['Administrador', 'Supervisor'])
def lista_bandas(request):
    query = request.GET.get('q', '')
    if query:
        bandas = Banda.objects.filter(
            Q(nombre__icontains=query) | Q(album__icontains=query)
        ).select_related('estilo').annotate(num_canciones=Count('repertorio'))
    else:
        bandas = Banda.objects.all().select_related('estilo').annotate(num_canciones=Count('repertorio'))
    return render(request, 'mantenedores/bandas_lista.html', {'bandas': bandas, 'query': query})



@login_required
@rol_requerido(['Administrador', 'Supervisor'])
def crear_banda(request):
    if request.method == 'POST':
        form = BandaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banda creada correctamente.')
            return redirect('bandas_lista')
    else:
        form = BandaForm()
    return render(request, 'mantenedores/banda_form.html', {'form': form, 'titulo': 'Nueva Banda'})

@login_required
@rol_requerido(['Administrador', 'Supervisor'])
def editar_banda(request, pk):
    banda = get_object_or_404(Banda, pk=pk)
    if request.method == 'POST':
        form = BandaForm(request.POST, instance=banda)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banda actualizada con éxito.')
            return redirect('bandas_lista')
    else:
        form = BandaForm(instance=banda)
    return render(request, 'mantenedores/banda_form.html', {'form': form, 'titulo': 'Modificar Banda'})

@login_required
@rol_requerido(['Administrador'])
def eliminar_banda(request, pk):
    banda = get_object_or_404(Banda, pk=pk)
    if request.method == 'POST':
        banda.delete()
        messages.success(request, 'Banda eliminada correctamente.')
        return redirect('bandas_lista')
    return render(request, 'mantenedores/confirmar_eliminar.html', {'objeto': banda.nombre, 'volver': 'bandas_lista'})

# --- MANTENEDOR 2: TARIFAS (CRUD) ---
@login_required
@rol_requerido(['Administrador', 'Supervisor', 'Administrativo'])
def lista_tarifas(request):
    tarifas = TarifaRocola.objects.all()
    return render(request, 'mantenedores/tarifas_lista.html', {'tarifas': tarifas})

@login_required
@rol_requerido(['Administrador'])
def crear_tarifa(request):
    if request.method == 'POST':
        form = TarifaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarifa registrada con éxito.')
            return redirect('tarifas_lista')
    else:
        form = TarifaForm()
    return render(request, 'mantenedores/tarifa_form.html', {'form': form, 'titulo': 'Nueva Tarifa'})

@login_required
@rol_requerido(['Administrador'])
def editar_tarifa(request, pk):
    tarifa = get_object_or_404(TarifaRocola, pk=pk)
    if request.method == 'POST':
        form = TarifaForm(request.POST, instance=tarifa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarifa actualizada correctamente.')
            return redirect('tarifas_lista')
    else:
        form = TarifaForm(instance=tarifa)
    return render(request, 'mantenedores/tarifa_form.html', {'form': form, 'titulo': 'Modificar Tarifa'})

@login_required
@rol_requerido(['Administrador'])
def eliminar_tarifa(request, pk):
    tarifa = get_object_or_404(TarifaRocola, pk=pk)
    if request.method == 'POST':
        tarifa.delete()
        messages.success(request, 'Tarifa eliminada con éxito.')
        return redirect('tarifas_lista')
    return render(request, 'mantenedores/confirmar_eliminar.html', {'objeto': tarifa.modo_reproduccion, 'volver': 'tarifas_lista'})

# --- TRANSACCIÓN OPERACIONAL ---
@login_required
def transaccion_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.usuario = request.user
            ticket.codigo_ticket = f"ROC-{uuid.uuid4().hex[:6].upper()}"
            ticket.monto_cobrado = ticket.tarifa.precio_base
            ticket.save()
            messages.success(request, f'Transacción exitosa: Ticket #{ticket.codigo_ticket} emitido.')
            return redirect('dashboard')
    else:
        form = TicketForm()
    return render(request, 'transacciones/nuevo_ticket.html', {'form': form})

# --- GESTIÓN DE CANCIONES DENTRO DE UNA BANDA ---
@login_required
@rol_requerido(['Administrador', 'Supervisor'])
def detalle_canciones_banda(request, pk):
    """Permite ver el setlist y agregar canciones a una banda específica."""
    banda = get_object_or_404(Banda, pk=pk)
    
    # Usar la relación directa 'repertorio'
    canciones = banda.repertorio.all()

    if request.method == 'POST':
        form = CancionForm(request.POST)
        if form.is_valid():
            nueva_cancion = form.save(commit=False)
            nueva_cancion.banda = banda
            nueva_cancion.save()
            messages.success(request, f'Pista "{nueva_cancion.titulo}" agregada con éxito al álbum {banda.album}.')
            return redirect('detalle_canciones_banda', pk=banda.id)
    else:
        form = CancionForm()

    return render(request, 'mantenedores/banda_canciones.html', {
        'banda': banda,
        'canciones': canciones,
        'form': form,
    })


@login_required
@rol_requerido(['Administrador', 'Supervisor'])
def eliminar_cancion(request, pk):
    """Permite quitar una canción de una banda."""
    cancion = get_object_or_404(Cancion, pk=pk)
    banda_id = cancion.banda.id
    if request.method == 'POST':
        cancion.delete()
        messages.success(request, 'Canción eliminada del repertorio.')
        return redirect('detalle_canciones_banda', pk=banda_id)
    return render(request, 'mantenedores/confirmar_eliminar.html', {
        'objeto': f'Canción: {cancion.titulo}',
        'volver': 'bandas_lista',
    })

# --- CREACIÓN RÁPIDA DE GÉNERO / ESTILO ---
@login_required
@rol_requerido(['Administrador', 'Supervisor'])
def crear_estilo(request):
    """Permite registrar un nuevo género/estilo musical y volver a la creación de banda."""
    next_url = request.GET.get('next', 'crear_banda')
    if request.method == 'POST':
        form = EstiloForm(request.POST)
        if form.is_valid():
            estilo = form.save()
            messages.success(request, f'Género "{estilo.nombre}" creado exitosamente.')
            return redirect(next_url)
    else:
        form = EstiloForm()
    return render(request, 'mantenedores/estilo_form.html', {'form': form, 'next_url': next_url})


# --- REGISTRO DE USUARIOS ---
def registro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save()
            
            rol_seleccionado = form.cleaned_data.get('rol')
            grupo_rol, _ = Group.objects.get_or_create(name=rol_seleccionado)
            nuevo_usuario.groups.add(grupo_rol)

            if rol_seleccionado == 'Administrador':
                nuevo_usuario.is_staff = True
                nuevo_usuario.save()

            login(request, nuevo_usuario)
            messages.success(request, f'¡Cuenta creada como {rol_seleccionado}! Bienvenido {nuevo_usuario.username}.')
            return redirect('dashboard')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'auth/registro.html', {'form': form})


# --- RECUPERACIÓN POR CÓDIGO DE SEGURIDAD (OTP) ---
def recuperar_solicitar_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SolicitarCodigoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # Generar código aleatorio de 6 dígitos
            codigo = str(random.randint(100000, 999999))
            
            # Guardar en sesión de Django
            request.session['reset_codigo'] = codigo
            request.session['reset_user_id'] = user.id

            asunto = "Código de recuperación - Rocola Virtual"
            mensaje = f"""Hola {user.username},

Tu código de verificación para restablecer tu contraseña es:

{codigo} 

Ingresa este código de 6 dígitos en la aplicación para definir tu nueva contraseña.
"""
            try:
                send_mail(
                    asunto,
                    mensaje,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.info(request, f'Hemos enviado un código de 6 dígitos a {email}.')
                return redirect('recuperar_verificar')
            except Exception as e:
                # Si SMTP falla, dejamos el código en la consola del servidor por respaldo
                print(f"\n[BACKUP EN TERMINAL] Código de recuperación generado: {codigo} para {user.username}\n")
                messages.error(request, f'Error al conectar con el servidor de correo: {e}')
    else:
        form = SolicitarCodigoForm()

    return render(request, 'auth/password_reset.html', {'form': form})

def recuperar_verificar_view(request):
    codigo_sesion = request.session.get('reset_codigo')
    user_id_sesion = request.session.get('reset_user_id')

    # Si no ha pedido código antes, devolver al inicio de la solicitud
    if not codigo_sesion or not user_id_sesion:
        messages.warning(request, 'Primero solicita tu código de verificación.')
        return redirect('password_reset')

    if request.method == 'POST':
        form = VerificarCodigoYCambiarClaveForm(request.POST)
        if form.is_valid():
            codigo_ingresado = form.cleaned_data['codigo']
            nueva_clave = form.cleaned_data['nueva_clave']

            if codigo_ingresado == codigo_sesion:
                user = get_object_or_404(User, id=user_id_sesion)
                user.set_password(nueva_clave)
                user.save()

                # Limpiar datos de la sesión
                del request.session['reset_codigo']
                del request.session['reset_user_id']

                messages.success(request, '¡Contraseña actualizada exitosamente! Ya puedes iniciar sesión.')
                return redirect('login')
            else:
                messages.error(request, 'El código ingresado es incorrecto.')
    else:
        form = VerificarCodigoYCambiarClaveForm()

    return render(request, 'auth/password_reset_confirm.html', {'form': form})