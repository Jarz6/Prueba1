from django.db import models

class Estilo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Estilo")

    class Meta:
        verbose_name = "Estilo"
        verbose_name_plural = "Estilos"

    def __str__(self):
        return self.nombre


class Banda(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre de la Banda")
    album = models.CharField(max_length=150, verbose_name="Álbum Destacado")
    imagen = models.CharField(max_length=100, help_text="Ej: foo.jpg, tool.jpg", verbose_name="Nombre de archivo de imagen")
    estilo = models.ForeignKey(Estilo, on_delete=models.CASCADE, related_name="bandas", verbose_name="Estilo Musical")

    class Meta:
        verbose_name = "Banda"
        verbose_name_plural = "Bandas"

    def __str__(self):
        return f"{self.nombre} ({self.album})"


class Cancion(models.Model):
    titulo = models.CharField(max_length=150, verbose_name="Título de la Canción")
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE, related_name="repertorio", verbose_name="Banda")

    class Meta:
        verbose_name = "Canción"
        verbose_name_plural = "Canciones"

    def __str__(self):
        return self.titulo