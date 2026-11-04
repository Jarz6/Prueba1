from django import forms
from .models import Banda, Cancion
from cobrosApp.models import TarifaRocola, TicketReproduccion

class BandaForm(forms.ModelForm):
    class Meta:
        model = Banda
        fields = ['nombre', 'album', 'estilo', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'album': forms.TextInput(attrs={'class': 'form-control'}),
            'estilo': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: foo.jpg'}),
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
        fields = ['cancion', 'tarifa']
        widgets = {
            'cancion': forms.Select(attrs={'class': 'form-select'}),
            'tarifa': forms.Select(attrs={'class': 'form-select'}),
        }