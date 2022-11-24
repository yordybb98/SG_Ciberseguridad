window.addEventListener('DOMContentLoaded', event => {

    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
         if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
             document.body.classList.toggle('sb-sidenav-toggled');
         }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

function search_function(elemento){
    let input, query, container, options, a, txtvalue, cont=0, result;
    input = $('#search_' + elemento)[0];
    query = input.value.toLowerCase();
    container = document.getElementById(elemento);
    result = container.getElementsByTagName('p');
    options = container.getElementsByClassName('form-check');
    for (let i = 0; i < options.length; i++) {
        a = options[i].getElementsByTagName('label')[0];
        txtvalue = a.innerText;
        if(txtvalue.toLowerCase().indexOf(query) > -1){
            options[i].style.display = '';
        }else{
            options[i].style.display = 'none';
            cont++;
        }
    }
    if(options.length === cont){
       result[0].innerText = 'No se encontraron resultados asociados a su búsqueda';
    }else{
        result[0].innerText = '';
    }
}

function swap(time){
    $('.form-content').animate({
        height: "toggle",
        opacity: "toggle"
    },time);
}

function eliminar(e,plural){
    let id = e[0].firstElementChild.id;
    e.remove();
    $('#'+id)[0].checked = false;
    competenciasempty(plural)
}

function manejocompetencias(singular,plural){

    competenciasempty(plural)

    e = $('#lista'+plural.toLocaleLowerCase()+ ' > div')

    for (let i = 0; i < e.length ; i++) {
        let con = $('#'+singular.toLowerCase()+i)
        id = con[0].firstElementChild.value
        con[0].firstElementChild.id = singular+'Check'+id
        con.on('click', function (e){
            eliminar(con, plural)
        })
    }

    $('#Aceptar'+plural).on('click', function (e){
        e.preventDefault();

        divs = $('#' + plural.toLowerCase() + ' > div');
        divs_checked = [];
        for (let i=0; i < divs.length; i++){
            if(divs[i].firstElementChild.checked){
                divs_checked.push(divs[i]);
            }
        }

        let lista = $('#lista' + plural.toLowerCase())[0];
        lista.classList.remove('text-dark-green')
        lista.innerHTML = '';
        for (let i = 0; i < divs_checked.length; i++) {
            var original = divs_checked[i];
            var clone = original.cloneNode(true);
            clone.id = singular.toLowerCase() + i;
            lista.appendChild(clone);

            let c = $('#' + singular.toLowerCase() + i)

            c.on('click', function (e){
                eliminar(c, plural)
            });
        }
    });
}

function competenciasempty(plural){
    let lista = $('#lista' + plural.toLowerCase())[0];
    if(lista){
        if (lista.childElementCount === 0 ){
            lista.innerHTML = 'Añada ' + plural + ' a su Perfil'
            lista.classList.add('text-dark-green')
        }
    }
}

$(document).ready(function(){


    //Manejo de Conocimientos del Especialista
    manejocompetencias('Conocimiento', 'Conocimientos')
    manejocompetencias('Habilidad', 'Habilidades')
    manejocompetencias('Tarea', 'Tareas')
    manejocompetencias('Herramienta', 'Herramientas')

    //Hora en el Sistema
    showTime()
    function showTime(){
        myDate = new Date();
        hours = myDate.getHours();
        minutes = myDate.getMinutes();
        if (hours < 10) hours = ('0' + hours);
        if (minutes < 10) minutes = ('0' + minutes);
        $("#HoraActual").text(myDate.toLocaleDateString() + ' ' +hours+ ":" +minutes);
        setInterval(showTime, 60000);
    }


    //Popover
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })

    //Tooltip
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })


    //SWAP REG-AUT
    $('.button').click(function(){
        swap(700);
    });


    //Validacion de los forms
    (function () {
        let forms = document.querySelectorAll('.needs-validation')

      Array.prototype.slice.call(forms)
        .forEach(function (form) {
          form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
              event.preventDefault()
              event.stopPropagation()
            }

            form.classList.add('was-validated')
          }, false)
        })
    })()

    //Ver_Pasword (Register)
    $("#see").on('click', function (){
        let pasw = $("#UserPass");
        var rep_pasw = $("#RepUserPass");
        if($("#see")[0].checked){
            pasw.attr('type', 'text');
            rep_pasw.attr('type', 'text');
        }
        else{
            pasw.attr('type', 'password');
            rep_pasw.attr('type', 'password');
        }
    })

    //Cambiar Provincia (Chequear si hay que dejarlo)
    $("optgroup > .option").on('click', function (e){
        element_selected = e.target;
        municipio = element_selected.value;

        provincia = element_selected.classList[1];

        element_provincia = $("#Provincia")[0];
        element_provincia.innerText  = provincia;

        })

    //Agregrar '-' al ingresar numero telefonico
    $("#Telefono").on('keyup', function (e){
        input = $("#Telefono")[0]
        size = input.textLength
        text = $("#Telefono")[0].value
        if(size == '4'){
            if(text.substr(text.length - 1, text.length ) != '-'){
                $("#Telefono")[0].value = text.substr(0, text.length - 1 ) + '-' + text.substr(text.length - 1, text.length )
            }
            else
                $("#Telefono")[0].value = text.substr(0, text.length - 1 )

        }else if(size == '7'){
            if(text.substr(text.length - 1, text.length ) != '-'){
                $("#Telefono")[0].value = text.substr(0, text.length - 1 ) + '-' + text.substr(text.length - 1, text.length )
            }
            else
                $("#Telefono")[0].value = text.substr(0, text.length - 1 )

        }

    })


    //Alert de salir
    $('#exit').on('click', function(e){
		e.preventDefault();
        Swal.fire({
          title: '¿Quiere cerrar sesión?',
          text: "Saldrá del Sistema",
          icon: 'warning',
          showCancelButton: true,
          cancelButtonColor: '#3085d6',
          confirmButtonColor: '#d33',
          confirmButtonText: 'Si, Salir',
          cancelButtonText: 'Cancelar'
        }).then((result) => {
          if (result.isConfirmed){
              window.location.href="/logout";
          }
        })
	});

    //Actualizar imagenes de avatar antes de enviar al backend
    const seleccionArchivos = $('#Avatar')[0],
        imagenPrevisualizacion = $('#img_avatar');


    if(seleccionArchivos){
        seleccionArchivos.addEventListener("change", () => {
            const archivos = seleccionArchivos.files;
            imagenPrevisualizacion.removeClass("hide");
            // Ahora tomamos el primer archivo, el cual vamos a previsualizar
            const primerArchivo = archivos[0];
            // Lo convertimos a un objeto de tipo objectURL
            const objectURL = URL.createObjectURL(primerArchivo);
            // Y a la fuente de la imagen le ponemos el objectURL
            imagenPrevisualizacion[0].src = objectURL;
        });
    }


    //
    $('#change_avatar').on('click', function (e){
        seleccionArchivos.click()
    })
});

function confirmar(id, path, element){
	Swal.fire({
          title: '¿Borrar ' + element + '?',
          text: "Esta acción no se podrá deshacer",
          icon: 'warning',
          showCancelButton: true,
          cancelButtonColor: '#3085d6',
          confirmButtonColor: '#d33',
          confirmButtonText: 'Si, Borrar'
        }).then((result) => {
          if (result.isConfirmed){
              window.location.href='/'+path+id;
          }
        })
    return false
}

    $("#allknowledge").on('click', function (e){

        if ( $("#allknowledge")[0].checked) {
            for(let i = 1; i <= $("[validate_conocimiento='True']").length; i++ ){
                document.getElementById('ConocimientoCheck'+i).checked =true;
            }
        }
        else{
            for(let i = 1; i <= $("[validate_conocimiento='True']").length; i++ ){
                document.getElementById('ConocimientoCheck'+i).checked =false;
            }
        }
    })

    $("#allskills").on('click', function (e){

        if ( $("#allskills")[0].checked) {
            for(let i = 1; i <= $("[validate_habilidad='True']").length; i++ ){
                document.getElementById('HabilidadCheck'+i).checked =true;
            }
        }
        else{
            for(let i = 1; i <= $("[validate_habilidad='True']").length; i++ ){
                document.getElementById('HabilidadCheck'+i).checked =false;
            }
        }
    })

    $("#alltasks").on('click', function (e){

        if ( $("#alltasks")[0].checked) {
            for(let i = 1; i <= $("[validate_tarea='True']").length; i++ ){
                document.getElementById('TareaCheck'+i).checked =true;
            }
        }
        else{
            for(let i = 1; i <= $("[validate_tarea='True']").length; i++ ){
                document.getElementById('TareaCheck'+i).checked =false;
            }
        }
    })

    $("#alltools").on('click', function (e){

        if ( $("#alltools")[0].checked) {
            for(let i = 1; i <= $("[validate_herramienta='True']").length; i++ ){
                document.getElementById('HerramientaCheck'+i).checked =true;
            }
        }
        else{
            for(let i = 1; i <= $("[validate_herramienta='True']").length; i++ ){
                document.getElementById('HerramientaCheck'+i).checked =false;
            }
        }
    })

    $("#allJobs").on('click', function (e){

        if ( $("#allJobs")[0].checked) {
            for(let i = 1; i <= $("[validate_centro='True']").length; i++ ){
                document.getElementById('CentroCheck'+i).checked =true;
            }
        }
        else{
            for(let i = 1; i <= $("[validate_centro='True']").length; i++ ){
                document.getElementById('CentroCheck'+i).checked =false;
            }
        }
    })

    $("[validate_conocimiento='True']").on('click', function (e){
        validate_conocimiento();
    })

    $("[validate_habilidad='True']").on('click', function (e){
        validate_habilidad();
    })

    $("[validate_tarea='True']").on('click', function (e){
        validate_tarea();
    })

    $("[validate_herramienta='True']").on('click', function (e){
         validate_herramienta();
    })

    $('#roltrabajo-edit').on('submit', function (e){
        validate_herramienta();
        validate_tarea();
        validate_habilidad();
        validate_conocimiento();
    })



    function validate_herramienta(){

        if ($("[validate_herramienta='True']:checked").length == 0) {
            $("[validate_herramienta='True']").attr('required', true);
        }
        else {
            $("[validate_herramienta='True']").attr('required', false);
        }
    }

    function validate_tarea(){
        if ($("[validate_tarea='True']:checked").length == 0) {
            $("[validate_tarea='True']").attr('required', true);
        }
        else {
            $("[validate_tarea='True']").attr('required', false);
        }
    }

    function validate_habilidad(){
        if ($("[validate_habilidad='True']:checked").length == 0) {
            $("[validate_habilidad='True']").attr('required', true);
        }
        else {
            $("[validate_habilidad='True']").attr('required', false);
        }
    }

    function validate_conocimiento(){
        if ($("[validate_conocimiento='True']:checked").length == 0) {
            $("[validate_conocimiento='True']").attr('required', true);
        }
        else {
            $("[validate_conocimiento='True']").attr('required', false);
        }
    }








