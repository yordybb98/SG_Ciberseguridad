from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .models import Municipio, Provincia, Categoria, AreaEspecialidad, Conocimiento, Habilidad, Tarea, \
    Herramienta, Genero, CentroTrabajo, RolTrabajo, Especialista
from .forms import UserForm, CategoriaForm, AreaEspecialidadForm, ConocimientoForm, HabilidadForm, \
    TareaForm, HerramientaForm, ProvinciaForm, GeneroForm, CentroTrabajoForm, MunicipioForm, \
    RolTrabajoForm, EspecialistaForm


@never_cache
def autenticar(request):
    if request.method == 'POST':
        usuario: User = authenticate(username=request.POST['usuario'], password=request.POST['contrasena'])
        if usuario:
            login(request, usuario)
            usuario.especialista.online = True
            usuario.especialista.save()
            return redirect('home')
        messages.error(request, 'Usuario y/o Coontraseña incorrectos')
    return redirect('autenticacion')

@never_cache
@login_required
def LogOut(request):
    request.user.especialista.online = False
    request.user.especialista.save()
    logout(request)
    return redirect('autenticacion')

@method_decorator(never_cache, name='dispatch')
class VRegistro(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect('home')
        form = UserCreationForm()
        return render(request, 'Sistema/index.html', {'form': form})

    @staticmethod
    def post(request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = user.username
            user.save()
            login(request, user)
            e = Especialista()
            e.usuario = user
            e.avatar = 'Sistema/DefaultAvatarUser.png'
            e.online = True
            e.save()

            return redirect('home')
        else:
            error = True
            return render(request, 'Sistema/index.html', {'form': form, 'error': error})


@login_required
def home(request):
    return render(request, 'Sistema/home.html')


@login_required
def cambiar_contrasena(request):
    if request.POST:
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Contraseña cambiada satisfactoriamente')
            return redirect('home')
        else:
            messages.warning(request, form.errors)
    form = PasswordChangeForm(user=request.user)
    return render(request, 'Sistema/Act_Perfil/change_password.html', {'form': form})


@login_required
def act_info(request):
    try:
        if request.POST:
            form = UserForm(request.POST, instance=request.user)
            formesp = EspecialistaForm(request.POST, request.FILES, instance=request.user.especialista)
            if form.is_valid() and formesp.is_valid():
                form.save()
                formesp.save()
                messages.success(request, 'Perfil editado satisfactoriamente')
                return redirect('act_info')
            else:
                messages.warning(request, form.errors)
                messages.warning(request, formesp.errors)
        form = UserForm(instance=request.user)
        formesp = EspecialistaForm(instance=request.user.especialista)
        genero = Genero.objects.all()
        provincias = Provincia.objects.all()
        municipios = Municipio.objects.all()
        centros = CentroTrabajo.objects.all()
        lhct = len(centros)
        hoy = timezone.now()
        conocimientos = Conocimiento.objects.all()
        lc = len(conocimientos)
        habilidades = Habilidad.objects.all()
        lh = len(habilidades)
        tareas = Tarea.objects.all()
        lt = len(tareas)
        herramientas = Herramienta.objects.all()
        lht = len(herramientas)
        return render(request, 'Sistema/Act_Perfil/change_personal_info.html', {'form': form,
                                                                                'formEsp': formesp,
                                                                                'generos': genero,
                                                                                'provincias': provincias,
                                                                                'municipios': municipios,
                                                                                'hoy': hoy,
                                                                                'centros': centros,
                                                                                'lhc': lhct,
                                                                                'conocimientos': conocimientos,
                                                                                'lc': lc,
                                                                                'habilidades': habilidades,
                                                                                'lh': lh,
                                                                                'tareas': tareas,
                                                                                'lt': lt,
                                                                                'herramientas': herramientas,
                                                                                'lht': lht,
                                                                                }
                      )
    except Especialista.DoesNotExist:
        e = Especialista()
        e.usuario = request.user
        e.avatar = 'Sistema/DefaultAvatarUser.png'
        e.save()
        return redirect('act_info')


@permission_required('add_categoria')
@login_required
def categoria_add(request):
    form = CategoriaForm(request.POST if request.POST else None)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Categoría añadida Satisfactoriamente')
            return redirect('/ver_categoria')
        else:
            messages.add_message(request, messages.ERROR, 'Ocurrió un Error vuelva a intentarlo')
            return redirect('/añadir_categoria')
    return render(request, 'Sistema/Categorias/categoria-add.html', {'form': form, 'username': request.user})


@login_required
def categoria_list(request):
    categorias = Categoria.objects.all()
    form = CategoriaForm()
    return render(request, 'Sistema/Categorias/categoria-list.html', {'categorias': categorias[::-1], 'form': form,
                                                                      'username': request.user})


@permission_required('delete_categoria')
@login_required
def delete_categoria(request, id):
    c = Categoria.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS, 'Categoría ' + c.nombre.upper() + ' eliminada satisfactoriamente')
    c.delete()
    return redirect('/ver_categoria')


@permission_required('change_categoria')
@login_required
def update_categoria(request, id):
    c = Categoria.objects.get(id=id)
    form = CategoriaForm(request.POST, instance=c)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Categoría ' + c.nombre.upper() + ' editada satisfactoriamente')
        return redirect('/ver_categoria')
    messages.add_message(request, messages.ERROR, 'Ocurrió un error, Intente Nuevamente')
    return redirect('/ver_categoria')


@permission_required('add_areaespecialidad')
@login_required
def area_especialidad_add(request):
    form = AreaEspecialidadForm(request.POST if request.POST else None)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Área de Especialidad añadida Satisfactoriamente')
            return redirect('/ver_area_especialidad')
        else:
            messages.add_message(request, messages.WARNING, 'Rellene los campos obligatorios')
    c = Categoria.objects.all()
    return render(request, 'Sistema/Area_Especialidad/areaespecialidad-add.html', {'form': form, 'categorias': c})


@login_required
def area_especialidad_list(request):
    area_especialidad = AreaEspecialidad.objects.all()
    categorias = Categoria.objects.all()
    form = AreaEspecialidadForm()
    return render(request, 'Sistema/Area_Especialidad/areaespecialidad_list.html', {'categorias': categorias[::-1],
                                                                                    'areas': area_especialidad[::-1],
                                                                                    'form': form,
                                                                                    'username': request.user})


@permission_required('delete_areaespecialidad')
@login_required
def delete_area_especialidad(request, id):
    a = AreaEspecialidad.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS,
                         'Área de Especialidad ' + a.nombre.upper() + ' eliminada satisfactoriamente')
    a.delete()
    return redirect('/ver_area_especialidad')


@permission_required('change_areaespecialidad')
@login_required
def update_area_especialidad(request, id):
    a = AreaEspecialidad.objects.get(id=id)
    form = AreaEspecialidadForm(request.POST, instance=a)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Área de Especialidad ' + a.nombre.upper() + ' editada satisfactoriamente')
        return redirect('/ver_area_especialidad')
    messages.add_message(request, messages.ERROR, 'Ocurrió un error, Intente Nuevamente')
    return redirect('/ver_area_especialidad')


@permission_required('add_roltrabajo')
@login_required
def rol_trabajo_add(request):
    form = RolTrabajoForm(request.POST if request.POST else None)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Rol de Trabajo Añadido Satisfactoriamente')
            return redirect('/ver_rol_trabajo')
        else:
            messages.add_message(request, messages.WARNING, 'Rellene los campos obligatorios')

    ae = AreaEspecialidad.objects.all()
    c = Conocimiento.objects.all()
    h = Habilidad.objects.all()
    t = Tarea.objects.all()
    ht = Herramienta.objects.all()
    lc = len(c)
    lh = len(h)
    lt = len(t)
    lht = len(ht)
    return render(request, 'Sistema/Rol_Trabajo/roltrabajo-add.html', {'form': form, 'areasespecialidades': ae,
                                                                       'conocimientos': c, 'habilidades': h,
                                                                       'tareas': t, 'herramientas': ht,
                                                                       'lc': lc, 'lh': lh, 'lt': lt, 'lht': lht})


@login_required
def rol_trabajo_list(request):
    rt = RolTrabajo.objects.all()
    return render(request, 'Sistema/Rol_Trabajo/roltrabajo-list.html', {'rolestrabajos': rt[::-1]})


@permission_required('delete_roltrabajo')
@login_required
def delete_rol_trabajo(request, id):
    rt = RolTrabajo.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS,
                         'Rol de Trabajo ' + rt.id_personalizado.upper() + ' Eliminado Satisfactoriamente')
    rt.delete()
    return redirect('/ver_rol_trabajo')


@permission_required('change_roltrabajo')
@login_required
def update_rol_trabajo(request, id):
    rt = RolTrabajo.objects.get(id=id)
    if request.POST:
        form = RolTrabajoForm(request.POST, instance=rt)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Rol de Trabajo ' + rt.id_personalizado.upper() + ' editado satisfactoriamente')
            return redirect('rol_trabajo_list')
        else:
            messages.add_message(request, messages.ERROR, 'Ocurrió un error, Intente Nuevamente')
    form = RolTrabajoForm()
    ae = AreaEspecialidad.objects.all()
    c = Conocimiento.objects.all()
    h = Habilidad.objects.all()
    t = Tarea.objects.all()
    ht = Herramienta.objects.all()
    lc = len(c)
    lh = len(h)
    lt = len(t)
    lht = len(ht)
    return render(request, 'Sistema/Rol_Trabajo/roltrabajo-edit.html', {'rt': rt, 'areasespecialidades': ae,
                                                                        'conocimientos': c, 'habilidades': h,
                                                                        'tareas': t, 'herramientas': ht, 'form': form,
                                                                        'lc': lc, 'lh': lh, 'lt': lt, 'lht': lht})


@login_required
def rol_trabajo(request, id):
    rt = RolTrabajo.objects.get(id=id)
    return render(request, 'Sistema/Rol_Trabajo/roltrabajo-view.html', {'rt': rt})

@permission_required('add_conocimiento')
@login_required
def conocimiento_add(request):
    form = ConocimientoForm(request.POST if request.POST else None)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Conocimiento añadido Satisfactoriamente')
            return redirect('/ver_conocimiento')
        else:
            messages.add_message(request, messages.WARNING, 'Rellene los campos obligatorios')
    return render(request, 'Sistema/Conocimiento/conocimiento-add.html', {'form': form})


@login_required
def conocimiento_list(request):
    c = Conocimiento.objects.all()
    form = CategoriaForm()
    return render(request, 'Sistema/Conocimiento/conocimiento-list.html', {'conocimientos': c[::-1], 'form': form})


@permission_required('delete_conocimiento')
@login_required
def delete_conocimiento(request, id):
    c = Conocimiento.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS,
                         'Conocimiento ' + c.id_personalizado.upper() + ' eliminado satisfactoriamente')
    c.delete()
    return redirect('/ver_conocimiento')


@permission_required('change_conocimiento')
@login_required
def update_conocimiento(request, id):
    c = Conocimiento.objects.get(id=id)
    form = ConocimientoForm(request.POST, instance=c)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Conocimiento ' + c.id_personalizado.upper() + ' editado satisfactoriamente')
        return redirect('/ver_conocimiento')
    messages.add_message(request, messages.ERROR, 'Ocurrió un error, Intente Nuevamente')
    return redirect('/ver_conocimiento')


@permission_required('add_habilidad')
@login_required
def habilidad_add(request):
    form = HabilidadForm(request.POST if request.POST else None)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Habilidad Añadida Satisfactoriamente')
            return redirect('/ver_habilidad')
        else:
            messages.add_message(request, messages.WARNING, 'Rellene los campos obligatorios')
    return render(request, 'Sistema/Habilidades/habilidad-add.html', {'form': form})


@login_required
def habilidad_list(request):
    h = Habilidad.objects.all()
    form = HabilidadForm
    return render(request, 'Sistema/Habilidades/habilidad-list.html', {'habilidades': h[::-1], 'form': form})


@permission_required('delete_habilidad')
@login_required
def delete_habilidad(request, id):
    h = Habilidad.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS,
                         'Habilidad ' + h.id_personalizado.upper() + ' eliminada satisfactoriamente')
    h.delete()
    return redirect('/ver_habilidad')


@permission_required('change_habilidad')
@login_required
def update_habilidad(request, id):
    h = Habilidad.objects.get(id=id)
    form = HabilidadForm(request.POST, instance=h)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Habilidad ' + h.id_personalizado.upper() + ' editada satisfactoriamente')
        return redirect('/ver_habilidad')
    messages.add_message(request, messages.ERROR, 'Ocurrió un error, Intente Nuevamente')
    return redirect('/ver_habilidad')


@permission_required('add_tarea')
@login_required
def tarea_add(request):
    form = TareaForm(request.POST if request.POST else None)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Tarea Añadida Satisfactoriamente')
            return redirect('/ver_tarea')
        else:
            messages.add_message(request, messages.WARNING, 'Rellene los campos obligatorios')
    return render(request, 'Sistema/Tareas/tarea-add.html', {'form': form})


@login_required
def tarea_list(request):
    t = Tarea.objects.all()
    form = TareaForm()
    return render(request, 'Sistema/Tareas/tarea-list.html', {'tareas': t[::-1], 'form': form})


@permission_required('delete_tarea')
@login_required
def delete_tarea(request, id):
    t = Tarea.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS,
                         'Tarea ' + t.id_personalizado.upper() + ' eliminada satisfactoriamente')
    t.delete()
    return redirect('/ver_tarea')


@permission_required('change_tarea')
@login_required
def update_tarea(request, id):
    t = Tarea.objects.get(id=id)
    form = TareaForm(request.POST, instance=t)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Tarea ' + t.id_personalizado.upper() + ' editada satisfactoriamente')
        return redirect('/ver_tarea')
    messages.add_message(request, messages.ERROR, 'Ocurrió un error, Intente Nuevamente')
    return redirect('/ver_tarea')


@permission_required('add_herramienta')
@login_required
def herramienta_add(request):
    form = HerramientaForm(request.POST if request.POST else None)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Herramienta añadida satisfactoriamente')
            return redirect('/ver_herramienta')
        else:
            messages.add_message(request, messages.WARNING, 'Rellene los campos obligatorios')
    return render(request, 'Sistema/Herramientas/herramienta-add.html', {'form': form})


@login_required
def herramienta_list(request):
    ht = Herramienta.objects.all()
    form = HerramientaForm()
    return render(request, 'Sistema/Herramientas/herramienta-list.html', {'herramientas': ht[::-1], 'form': form})


@permission_required('delete_herramienta')
@login_required
def delete_herramienta(request, id):
    ht = Herramienta.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS,
                         'Herramienta ' + ht.id_personalizado.upper() + ' eliminada satisfactoriamente')
    ht.delete()
    return redirect('/ver_herramienta')


@permission_required('change_herramienta')
@login_required
def update_herramienta(request, id):
    ht = Herramienta.objects.get(id=id)
    form = HerramientaForm(request.POST, instance=ht)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Herramienta ' + ht.id_personalizado.upper() + ' editada satisfactoriamente')
        return redirect('/ver_herramienta')
    messages.add_message(request, messages.ERROR, 'Ocurrió un error, Intente Nuevamente')
    return redirect('/ver_herramienta')


@permission_required('add_centrotrabajo')
@login_required
def centro_trabajo_add(request):
    form = CentroTrabajoForm(request.POST if request.POST else None)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Centro de Trabajo añadido satisfactoriamente')
            return redirect('/ver_centro_trabajo')
        else:
            messages.add_message(request, messages.WARNING, 'Rellene los campos obligatorios')

    return render(request, 'Sistema/Centros_Trabajos/centrotrabajo-add.html', {'form': form})


@permission_required('view_centrotrabajo')
@login_required
def centro_trabajo_list(request):
    form = CentroTrabajoForm()
    c = CentroTrabajo.objects.all()
    return render(request, 'Sistema/Centros_Trabajos/centrotrabajo-list.html',
                  {'centrostrabajos': c[::-1], 'form': form})


@permission_required('delete_centrotrabajo')
@login_required
def delete_centro_trabajo(request, id):
    ct = CentroTrabajo.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS,
                         'Centro de Trabajo ' + ct.nombre.upper() + ' eliminado satisfactoriamente')
    ct.delete()
    return redirect('/ver_centro_trabajo')


@permission_required('change_centrotrabajo')
@login_required
def update_centro_trabajo(request, id):
    ct = CentroTrabajo.objects.get(id=id)
    form = CentroTrabajoForm(request.POST, instance=ct)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Centro de Trabajo ' + ct.nombre.upper() + ' editado satisfactoriamente')
        return redirect('/ver_centro_trabajo')
    messages.add_message(request, messages.ERROR, 'Ocurrió un error, Intente Nuevamente')
    return redirect('/ver_centro_trabajo')


@permission_required('add_genero')
@login_required
def genero_add(request):
    if request.POST:
        form = GeneroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Género añadido satisfactoriamente')
            return redirect('/ver_genero')
        else:
            messages.add_message(request, messages.WARNING, 'Rellene los campos obligatorios')
    else:
        form = GeneroForm()
    return render(request, 'Sistema/Generos/genero-add.html', {'form': form})


@permission_required('view_genero')
@login_required
def genero_list(request):
    form = GeneroForm()
    g = Genero.objects.all()
    return render(request, 'Sistema/Generos/genero-list.html', {'generos': g[::-1], 'form': form})


@permission_required('delete_genero')
@login_required
def delete_genero(request, id):
    g = Genero.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS,
                         'Género ' + g.nombre.upper() + ' eliminado satisfactoriamente')
    g.delete()
    return redirect('/ver_genero')


@permission_required('change_genero')
@login_required
def update_genero(request, id):
    g = Genero.objects.get(id=id)
    form = GeneroForm(request.POST, request.FILES, instance=g)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Género ' + g.nombre.upper() + ' editado satisfactoriamente')
        return redirect('/ver_genero')
    messages.add_message(request, messages.ERROR, 'Ocurrió un error, Intente Nuevamente')
    return redirect('/ver_genero')


@permission_required('add_municipio')
@login_required
def municipio_add(request):
    form = MunicipioForm(request.POST if request.POST else None)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Municipio añadido satisfactoriamente')
            return redirect('/ver_municipio')
    p = Provincia.objects.all()
    return render(request, 'Sistema/Municipios/municipio-add.html', {'form': form, 'provincias': p[::-1]})


@permission_required('view_municipio')
@login_required
def municipio_list(request):
    m = Municipio.objects.all()
    p = Provincia.objects.all()
    form = MunicipioForm()
    return render(request, 'Sistema/Municipios/municipio-list.html',
                  {'municipios': m[::-1], 'provincias': p, 'form': form})


@permission_required('delete_municipio')
@login_required
def delete_municipio(request, id):
    m = Municipio.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS,
                         'Municipio ' + m.nombre.upper() + ' eliminado satisfactoriamente')
    m.delete()
    return redirect('/ver_municipio')


@permission_required('change_municipio')
@login_required
def update_municipio(request, id):
    m = Municipio.objects.get(id=id)
    form = MunicipioForm(request.POST, instance=m)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Municipio ' + m.nombre.upper() + ' editado satisfactoriamente')
        return redirect('/ver_municipio')
    messages.add_message(request, messages.ERROR, 'Ocurrió un error, Intente Nuevamente')
    return redirect('/ver_municipio')


@permission_required('add_provincia')
@login_required
def provincia_add(request):
    form = ProvinciaForm(request.POST if request.POST else None)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Provincia añadida satisfactoriamente')
            return redirect('/ver_provincia')
        messages.add_message(request, messages.ERROR, 'Ocurrió un error, Intente Nuevamente')

    return render(request, 'Sistema/Provincia/provincia-add.html', {'form': form})


@permission_required('view_provincia')
@login_required
def provincia_list(request):
    p = Provincia.objects.all()
    form = ProvinciaForm
    return render(request, 'Sistema/Provincia/provincia-list.html', {'provincias': p[::-1], 'form': form})


@permission_required('delete_provincia')
@login_required
def delete_provincia(request, id):
    p = Provincia.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS,
                         'Provincia ' + p.nombre.upper() + ' eliminada satisfactoriamente')
    p.delete()
    return redirect('/ver_provincia')


@permission_required('change_provincia')
@login_required
def update_provincia(request, id):
    p = Provincia.objects.get(id=id)
    form = ProvinciaForm(request.POST, instance=p)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Provincia ' + p.nombre.upper() + ' editada satisfactoriamente')
        return redirect('/ver_provincia')
    messages.add_message(request, messages.ERROR, 'Ocurrió un error, Intente Nuevamente')
    return redirect('/ver_provincia')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('is_staff'), name='dispatch')
class AdminAdd(View):

    @staticmethod
    def get(request):
        form = UserCreationForm()
        return render(request, 'Sistema/Administracion_Usuarios/admin-user-add.html', {'form': form})

    @staticmethod
    def post(request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = user.username
            user.is_staff = True
            user.is_superuser = True
            user.save()
            e = Especialista()
            e.usuario = user
            e.avatar = 'Sistema/DefaultAvatarUser.png'
            e.save()
            return redirect('admin_list')
        else:
            messages.warning(request, form.errors)
            return render(request, 'Sistema/Administracion_Usuarios/admin-user-add.html', {'form': form})


@permission_required('is_staff')
@login_required
def admin_list(request):
    admins = User.objects.filter(is_staff=True)
    return render(request, 'Sistema/Administracion_Usuarios/admin-user-list.html', {'administradores': admins, })


@permission_required('is_staff')
@login_required
def delete_admin(request, id):
    a = User.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS,
                         'Administrador(a) ' + a.username.upper() + ' eliminado satisfactoriamente')
    a.delete()
    return redirect('admin_list')


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('is_staff'), name='dispatch')
class EspecialistaAdd(View):

    @staticmethod
    def get(request):
        form = UserCreationForm()
        return render(request, 'Sistema/Administracion_Usuarios/especialista-user-add.html', {'form': form})

    @staticmethod
    def post(request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.first_name = user.username
            user.is_staff = False
            user.save()
            e = Especialista()
            e.usuario = user
            e.avatar = 'Sistema/DefaultAvatarUser.png'
            e.save()
            return redirect('especialista_list')
        else:
            messages.warning(request, form.errors)
            return render(request, 'Sistema/Administracion_Usuarios/especialista-user-add.html', {'form': form})


@permission_required('is_staff')
@login_required
def especialista_list(request):
    especialistas = User.objects.filter(is_staff=False)
    return render(request, 'Sistema/Administracion_Usuarios/especialista-user-list.html',
                  {'especialistas': especialistas})


@permission_required('is_staff')
@login_required
def delete_especialista(request, id):
    e = User.objects.get(id=id)
    messages.add_message(request, messages.SUCCESS,
                         'Especialista ' + e.username.upper() + ' eliminado satisfactoriamente')
    e.delete()
    return redirect('especialista_list')


@login_required
def evaluar_especialista(request, rt_id):
    rt = RolTrabajo.objects.get(id=rt_id)
    usuario = request.user.especialista

    ######################
    ### CONOCIMIENTOS ####
    ######################
    conocimientos_totales = len(rt.conocimientos.all())
    conocimientos_cubiertos = []
    conocimientos_faltantes = []

    for a in rt.conocimientos.all():

        if a in usuario.conocimientos.all():
            conocimientos_cubiertos.append(a)
        else:
            conocimientos_faltantes.append(a)

    promedio_cubierto = porciento(conocimientos_cubiertos, rt.conocimientos.all())
    promedio_faltante = round(100-promedio_cubierto, 2)
    calificacion = calificar(promedio_cubierto)

    estadisticas = {
        'conocimientos':{
            'total': len(rt.conocimientos.all()),
            'total_cubierto': len(conocimientos_cubiertos),
            'promedio_cubierto': promedio_cubierto,
            'total_faltante': len(conocimientos_faltantes),
            'promedio_faltante': promedio_faltante,
            'calificacion': calificacion,
            'faltantes': conocimientos_faltantes
        }
    }

    ######################
    #### HABILIDADES #####
    ######################

    habilidades_cubiertos = []
    habilidades_faltantes = []

    for a in rt.habilidades.all():

        if a in usuario.habilidades.all():
            habilidades_cubiertos.append(a)
        else:
            habilidades_faltantes.append(a)

    promedio_cubierto = porciento(habilidades_cubiertos, rt.habilidades.all())
    promedio_faltante = round(100 - promedio_cubierto, 2)
    calificacion = calificar(promedio_cubierto)

    estadisticas['habilidades'] = {
            'total': len(rt.habilidades.all()),
            'total_cubierto': len(habilidades_cubiertos),
            'promedio_cubierto': promedio_cubierto,
            'total_faltante': len(habilidades_faltantes),
            'promedio_faltante': promedio_faltante,
            'calificacion': calificacion,
            'faltantes': habilidades_faltantes
        }

    ######################
    ###### TAREAS ########
    ######################

    tareas_cubiertos = []
    tareas_faltantes = []

    for a in rt.tareas.all():

        if a in usuario.tareas.all():
            tareas_cubiertos.append(a)
        else:
            tareas_faltantes.append(a)

        promedio_cubierto = porciento(tareas_cubiertos, rt.tareas.all())
        promedio_faltante = round(100 - promedio_cubierto, 2)
        calificacion = calificar(promedio_cubierto)

        estadisticas['tareas'] = {
                'total': len(rt.tareas.all()),
                'total_cubierto': len(tareas_cubiertos),
                'promedio_cubierto': promedio_cubierto,
                'total_faltante': len(tareas_faltantes),
                'promedio_faltante': promedio_faltante,
                'calificacion': calificacion,
                'faltantes': tareas_faltantes
            }

    ######################
    #### HERRAMIENTAS ####
    ######################

    herramientas_cubiertos = []
    herramientas_faltantes = []

    for a in rt.herramientas.all():

        if a in usuario.herramientas.all():
            herramientas_cubiertos.append(a)
        else:
            herramientas_faltantes.append(a)

        promedio_cubierto = porciento(herramientas_cubiertos, rt.herramientas.all())
        promedio_faltante = round(100 - promedio_cubierto, 2)
        calificacion = calificar(promedio_cubierto)

        estadisticas['herramientas'] = {
                'total': len(rt.herramientas.all()),
                'total_cubierto': len(herramientas_cubiertos),
                'promedio_cubierto': promedio_cubierto,
                'total_faltante': len(herramientas_faltantes),
                'promedio_faltante': promedio_faltante,
                'calificacion': calificacion,
                'faltantes': herramientas_faltantes
            }

    return render(request, 'Sistema/Rol_Trabajo/report.html', {'estadisticas': estadisticas, 'rt': rt})


def porciento(parte, total):
    return round((len(parte) * 100) / len(total), 2)


def calificar(a):
    b = ''
    if a == 100:
        b = 'Perfecta'
    elif a >= 75:
        b = 'Alta'
    elif 50 < a < 75:
        b = 'Media'
    else:
        b = 'Baja'
    return b
