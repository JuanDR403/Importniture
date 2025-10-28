from django.db import models


class Usuario(models.Model):
    idusuarios = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, null=True, blank=True)
    apellido = models.CharField(max_length=45, null=True, blank=True)
    correo = models.EmailField(max_length=45, null=True, blank=True)
    telefono = models.CharField(max_length=45, null=True, blank=True)
    idrol = models.IntegerField(db_column='idrol', default=1)

    class Meta:
        db_table = 'usuarios'
        managed = False
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.correo})"
