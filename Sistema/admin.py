from django.contrib import admin
from .models import Especialista, Conocimiento, Habilidad, Tarea, Herramienta, CentroTrabajo, RolTrabajo,\
                    AreaEspecialidad, Categoria,  Genero,  Provincia,  Municipio


class RolTrabajoAdmin(admin.ModelAdmin):
    list_display = ('id_personalizado', 'nombre')


admin.site.register(Especialista)
admin.site.register(Categoria)
admin.site.register(AreaEspecialidad)
admin.site.register(RolTrabajo, RolTrabajoAdmin)
admin.site.register(Conocimiento)
admin.site.register(Habilidad)
admin.site.register(Tarea)
admin.site.register(Herramienta)
admin.site.register(CentroTrabajo)
admin.site.register(Genero)
admin.site.register(Municipio)
admin.site.register(Provincia)