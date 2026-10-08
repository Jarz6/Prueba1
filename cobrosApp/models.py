from django.db import models

class TarifaRocola(models.Model):
    modo_reproduccion = models.CharField(
        max_length=150, 
        verbose_name="Modo de Reproducción (ej. Set corto aleatorio, Álbum completo)"
    )
    duracion_minutos = models.PositiveIntegerField(
        verbose_name="Duración estimada (minutos)"
    )
    precio_base = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Tarifa / Costo ($)"
    )

    class Meta:
        verbose_name = "Tarifa de Rocola"
        verbose_name_plural = "Tarifas de Rocola"

    def __str__(self):
        return f"{self.modo_reproduccion} - {self.duracion_minutos} min (${self.precio_base})"