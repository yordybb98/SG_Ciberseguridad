window.addEventListener('DOMContentLoaded', event => {

    const datatablesSimple = document.querySelectorAll('#datatablesSimple')
    if (datatablesSimple){
        datatablesSimple.forEach(CrearTabla);
    }

    function CrearTabla(item){
        new simpleDatatables.DataTable(item, {
           searchable: true,
        });
    }

    /* Exportar a csv
        a.export({
            type:"csv",
            download: true,
            lineDelimiter: "\n",
            columnDelimiter: ","
        })
    */
});
