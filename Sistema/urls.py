from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.VRegistro.as_view(), name="autenticacion"),
    path('autenticar/', views.autenticar, name="autenticar"),
    path('logout/', views.LogOut, name="LogOut"),

    path('perfil/', views.act_info, name="act_info"),
    path('cambiar_contraseña/', views.cambiar_contrasena, name="cambiar_contraseña"),

    path('añadir_categoria/', views.categoria_add, name="categoria_add"),
    path('ver_categoria/', views.categoria_list, name="categoria_list"),
    path('delete_categoria/<id>', views.delete_categoria, name='categoria_delete'),
    path('update_categoria/<id>', views.update_categoria, name='categoria_update'),

    path('añadir_area_especialidad/', views.area_especialidad_add, name="area_especialidad_add"),
    path('ver_area_especialidad/', views.area_especialidad_list, name="area_especialidad_list"),
    path('delete_area_especialidad/<id>', views.delete_area_especialidad, name='area_especialidad_delete'),
    path('update_area_especialidad/<id>', views.update_area_especialidad, name='area_especialidad_update'),

    path('añadir_rol_trabajo/', views.rol_trabajo_add, name="rol_trabajo_add"),
    path('ver_rol_trabajo/', views.rol_trabajo_list, name="rol_trabajo_list"),
    path('ver_rol_trabajo/edit_rol_trabajo/<id>', views.update_rol_trabajo, name='rol_trabajo_edit'),
    path('ver_rol_trabajo/rol_trabajo/<id>', views.rol_trabajo, name='rol_trabajo_ver'),
    path('delete_rol_trabajo/<id>', views.delete_rol_trabajo, name='rol_trabajo_delete'),

    path('añadir_conocimiento/', views.conocimiento_add, name="conocimiento_add"),
    path('ver_conocimiento/', views.conocimiento_list, name="conocimiento_list"),
    path('delete_conocimiento/<id>', views.delete_conocimiento, name='conocimiento_delete'),
    path('update_conocimiento/<id>', views.update_conocimiento, name='conocimiento_update'),

    path('añadir_habilidad/', views.habilidad_add, name="habilidad_add"),
    path('ver_habilidad/', views.habilidad_list, name="habilidad_list"),
    path('delete_habilidad/<id>', views.delete_habilidad, name='habilidad_delete'),
    path('update_habilidad/<id>', views.update_habilidad, name='habilidad_update'),

    path('añadir_tarea/', views.tarea_add, name="tarea_add"),
    path('ver_tarea/', views.tarea_list, name="tarea_list"),
    path('delete_tarea/<id>', views.delete_tarea, name='tarea_delete'),
    path('update_tarea/<id>', views.update_tarea, name='tarea_update'),

    path('añadir_herramienta/', views.herramienta_add, name="herramienta_add"),
    path('ver_herramienta/', views.herramienta_list, name="herramienta_list"),
    path('delete_herramienta/<id>', views.delete_herramienta, name='herramienta_delete'),
    path('update_herramienta/<id>', views.update_herramienta, name='herramienta_update'),

    path('añadir_centro_trabajo/', views.centro_trabajo_add, name="centro_trabajo_add"),
    path('ver_centro_trabajo/', views.centro_trabajo_list, name="centro_trabajo_list"),
    path('delete_centro_trabajo/<id>', views.delete_centro_trabajo, name='centro_trabajo_delete'),
    path('update_centro_trabajo/<id>', views.update_centro_trabajo, name='centro_trabajo_update'),

    path('añadir_genero/', views.genero_add, name="genero_add"),
    path('ver_genero/', views.genero_list, name="genero_list"),
    path('delete_genero/<id>', views.delete_genero, name='genero_delete'),
    path('update_genero/<id>', views.update_genero, name='genero_update'),

    path('añadir_municipio/', views.municipio_add, name="municipio_add"),
    path('ver_municipio/', views.municipio_list, name="municipio_list"),
    path('delete_municipio/<id>', views.delete_municipio, name='municipio_delete'),
    path('update_municipio/<id>', views.update_municipio, name='municipio_update'),

    path('añadir_provincia/', views.provincia_add, name="provincia_add"),
    path('ver_provincia/', views.provincia_list, name="provincia_list"),
    path('delete_provincia/<id>', views.delete_provincia, name='provincia_delete'),
    path('update_provincia/<id>', views.update_provincia, name='provincia_update'),

    path('añadir_admin/', views.AdminAdd.as_view(), name="admin_add"),
    path('ver_admin/', views.admin_list, name="admin_list"),
    path('delete_admin/<id>', views.delete_admin, name='admin_delete'),

    path('añadir_especialista/', views.EspecialistaAdd.as_view(), name="especialista_add"),
    path('ver_especialista/', views.especialista_list, name="especialista_list"),
    path('delete_especialista/<id>', views.delete_especialista, name='especialista_delete'),

    path('evaluar_especialista/<rt_id>', views.evaluar_especialista, name='especialista_evaluar'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
