from django.contrib import admin
from .models import Estilo, Banda, Cancion

class CancionInline(admin.TabularInline):
    model = Cancion
    extra = 1

@admin.register(Estilo)
class EstiloAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Banda)
class BandaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'album', 'estilo', 'imagen')
    list_filter = ('estilo',)
    search_fields = ('nombre', 'album')
    inlines = [CancionInline]

@admin.register(Cancion)
class CancionAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'banda')
    list_filter = ('banda',)
    search_fields = ('titulo', 'banda__nombre')