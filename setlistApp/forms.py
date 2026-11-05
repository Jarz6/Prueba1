from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Banda, Cancion, Estilo
from cobrosApp.models import TarifaRocola, TicketReproduccion


class EstiloForm(forms.ModelForm):
    class Meta:
        model = Estilo
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Heavy Metal, Indie Rock'}),
        }


class CancionForm(forms.ModelForm):
    class Meta:
        model = Cancion
        fields = ['titulo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la pista'}),
        }


class BandaForm(forms.ModelForm):
    class Meta:
        model = Banda
        fields = ['nombre', 'album', 'estilo', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'album': forms.TextInput(attrs={'class': 'form-control'}),
            'estilo': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: foo.jpg o enlace URL'}),
        }


class TarifaForm(forms.ModelForm):
    class Meta:
        model = TarifaRocola
        fields = ['modo_reproduccion', 'duracion_minutos', 'precio_base']
        widgets = {
            'modo_reproduccion': forms.TextInput(attrs={'class': 'form-control'}),
            'duracion_minutos': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_base': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = TicketReproduccion
        fields = ['tarifa', 'cancion', 'banda']
        widgets = {
            'tarifa': forms.Select(attrs={'class': 'form-select'}),
            'cancion': forms.Select(attrs={'class': 'form-select'}),
            'banda': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        cancion = cleaned_data.get('cancion')
        banda = cleaned_data.get('banda')

        if not cancion and not banda:
            raise forms.ValidationError("Debes seleccionar una Canción O un Álbum para la reproducción.")
        if cancion and banda:
            raise forms.ValidationError("Por favor selecciona solo una opción: o una Canción individual o un Álbum completo.")
        return cleaned_data


class RegistroUsuarioForm(UserCreationForm):
    ROLES_DISPONIBLES = [
        ('Administrador', 'Administrador (Acceso Total)'),
        ('Supervisor', 'Supervisor (Gestión Operacional)'),
        ('Administrativo', 'Administrativo (Consultas y Transacciones)'),
    ]

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.cl'})
    )
    rol = forms.ChoiceField(
        choices=ROLES_DISPONIBLES,
        initial='Administrativo',
        label="Nivel de Cuenta / Rol",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'rol']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya se encuentra registrado.")
        return email