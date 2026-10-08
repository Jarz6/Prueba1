from django.contrib import admin
from .models import TarifaRocola

@admin.register(TarifaRocola)
class TarifaRocolaAdmin(admin.ModelAdmin):
    list_display = ('id', 'modo_reproduccion', 'duracion_minutos', 'precio_base')
    search_fields = ('modo_reproduccion',)
    list_filter = ('duracion_minutos',)