from django.shortcuts import render
from .models import Banda

def inicio(request):
    return render(request, 'setlistApp/inicio.html')

def lista_bandas(request):
    bandas = Banda.objects.select_related('estilo').prefetch_related('repertorio').all()
    contexto = {
        'bandas': bandas
    }
    return render(request, 'setlistApp/bandas.html', contexto)