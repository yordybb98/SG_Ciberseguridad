from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User
from django.core.validators import MinLengthValidator, validate_integer
from django.db import models
from datetime import date

# Create your models here.
from django.utils import timezone


class Genero(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    nombre = models.CharField(max_length=255)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Categoría', blank=False, null=False)
    abreviatura = models.CharField(max_length=2)
    descripcion = models.CharField(max_length=350)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nombre


class AreaEspecialidad(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Área de Especialidad')
    abreviatura = models.CharField(max_length=3)
    descripcion = models.CharField(max_length=350)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Area de Especialidad'
        verbose_name_plural = 'Areas de Especialidades'

    def __str__(self):
        return self.nombre


class Conocimiento(models.Model):
    descripcion = models.CharField(max_length=350)

    class Meta:
        verbose_name = 'Conocimiento'
        verbose_name_plural = 'Conocimientos'

    @property
    def id_personalizado(self):
        return 'C' + "{:04}".format(self.id)

    def __str__(self):
        return str(self.id_personalizado)


class Habilidad(models.Model):
    descripcion = models.CharField(max_length=350)

    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'

    @property
    def id_personalizado(self):
        return 'H' + "{:04}".format(self.id)

    def __str__(self):
        return str(self.id_personalizado)


class Tarea(models.Model):
    descripcion = models.CharField(max_length=350)

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'

    @property
    def id_personalizado(self):
        return 'T' + "{:04}".format(self.id)

    def __str__(self):
        return str(self.id_personalizado)


class Herramienta(models.Model):
    descripcion = models.CharField(max_length=350)

    class Meta:
        verbose_name = 'Herramienta'
        verbose_name_plural = 'Herramientas'

    @property
    def id_personalizado(self):
        return 'HT' + "{:04}".format(self.id)

    def __str__(self):
        return str(self.id_personalizado)


class RolTrabajo(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='nombre')
    descripcion = models.CharField(max_length=350)
    area_especialidad = models.ForeignKey(AreaEspecialidad, on_delete=models.CASCADE)
    conocimientos = models.ManyToManyField(Conocimiento, verbose_name='Lista de Conocimientos')
    habilidades = models.ManyToManyField(Habilidad, verbose_name='Lista de Habilidades')
    tareas = models.ManyToManyField(Tarea, verbose_name='Lista de Tareas')
    herramientas = models.ManyToManyField(Herramienta, verbose_name='Lista de Herramientas')

    class Meta:
        verbose_name = 'Rol de Trabajo'
        verbose_name_plural = 'Roles de Trabajo'

    @property
    def id_personalizado(self):
        return str(self.area_especialidad.categoria.abreviatura) + '-' \
               + self.area_especialidad.abreviatura + '-' + "{:03}".format(self.id)

    def __str__(self):
        return self.nombre


class CentroTrabajo(models.Model):
    nombre = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Centro de Trabajo'
        verbose_name_plural = 'Centros de Trabajos'

    def __str__(self):
        return self.nombre


class Especialista(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    online = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='Sistema/UsersAvatars', null=True, blank=True)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento', null=True, blank=True )
    ci = models.CharField(max_length=11, null=True, blank=True, validators=[MinLengthValidator(11), validate_integer], verbose_name='Carnet de Identidad')
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)  # Basado en la  UIT-T E.164
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
    trabajo_antiguos = models.ManyToManyField(CentroTrabajo, verbose_name='Centros de Trabajo Previos', blank=True)
    conocimientos = models.ManyToManyField(Conocimiento, blank=True)
    habilidades = models.ManyToManyField(Habilidad, blank=True)
    tareas = models.ManyToManyField(Tarea, blank=True)
    herramientas = models.ManyToManyField(Herramienta, blank=True)

    class Meta:
        verbose_name = 'Especialista'
        verbose_name_plural = 'Especialistas'

    def __str__(self):
        return self.usuario.first_name + ' ' + self.usuario.last_name

    @property
    def is_online(self):
        return self.online

    @property
    def edad(self):
        try:
            return timezone.now().year - self.fecha_nacimiento.year
        except AttributeError:
            return 'Aun sin Definir'

    @property
    def nacimiento(self):
        try:
            month = "{:02}".format(self.fecha_nacimiento.month)
            day = "{:02}".format(self.fecha_nacimiento.day)
            return str(self.fecha_nacimiento.year) + '-' + str(month) + '-' + str(day)
        except AttributeError:
            return 'Aun sin Definir'


    @property
    def has_avatar(self):
        return True if self.avatar is not None else False


    @property
    def has_municipio(self):
        return True if self.municipio is not None else False


    @property
    def has_direccion(self):
        return True if self.direccion is not None else False


    @property
    def has_telefono(self):
        return True if self.telefono is not None else False


    @property
    def has_ci(self):
        return True if self.ci is not None else False
