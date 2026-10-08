from django.shortcuts import render
from django.db.models import Avg, Count
from .models import TarifaRocola

def planes_servicios(request):
    # Consulta mediante Django ORM
    tarifas = TarifaRocola.objects.all()
    contexto = {
        'tarifas': tarifas
    }
    return render(request, 'cobrosApp/servicios.html', contexto)

def resumen_cobros(request):
    # Agregaciones estadísticas del lado del servidor con ORM
    metricas = TarifaRocola.objects.aggregate(
        total=Count('id'),
        promedio=Avg('duracion_minutos')
    )
    contexto = {
        'total_modos': metricas['total'] or 0,
        'promedio_duracion': metricas['promedio'] or 0,
    }
    return render(request, 'cobrosApp/calcular.html', contexto)