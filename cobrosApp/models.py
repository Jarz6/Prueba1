from django.db import models
from django.contrib.auth.models import User
from setlistApp.models import Banda, Cancion

class TarifaRocola(models.Model):
    modo_reproduccion = models.CharField(max_length=100, verbose_name="Modo de Reproducción")
    duracion_minutos = models.PositiveIntegerField(verbose_name="Duración (minutos)")
    precio_base = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Precio Base ($)")

    def __str__(self):
        return f"{self.modo_reproduccion} - ${self.precio_base}"

class TicketReproduccion(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente en Cola'),
        ('REPRODUCIENDO', 'En Reproducción'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]

    codigo_ticket = models.CharField(max_length=20, unique=True, verbose_name="Código")
    # Ahora permite seleccionar Canción O Banda/Álbum
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE, related_name="tickets", null=True, blank=True)
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE, related_name="tickets", null=True, blank=True, verbose_name="Álbum / Banda")
    tarifa = models.ForeignKey(TarifaRocola, on_delete=models.PROTECT, related_name="tickets")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    monto_cobrado = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    def __str__(self):
        item = self.cancion.titulo if self.cancion else f"Álbum: {self.banda.album}"
        return f"Ticket #{self.codigo_ticket} - {item} ({self.usuario.username})"