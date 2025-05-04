document.addEventListener('DOMContentLoaded', function () {
    const tipoUsuario = document.getElementById('tipoUsuario');
    const datosPersonales = document.getElementById('datosPersonales');
    const asignacionUsuario = document.getElementById('asignacionUsuario');
    const asignacionPuesto = document.getElementById('asignacionPuesto');

    function actualizarCampos() {
        if (tipoUsuario.value === "residente") {
            datosPersonales.classList.remove('d-none');
            asignacionUsuario.classList.remove('d-none');
            asignacionPuesto.classList.add('d-none');
        } else if (tipoUsuario.value === "trabajador") {
            datosPersonales.classList.remove('d-none');
            asignacionUsuario.classList.remove('d-none');
            asignacionPuesto.classList.remove('d-none');
        } else {
            datosPersonales.classList.add('d-none');
            asignacionUsuario.classList.add('d-none');
            asignacionPuesto.classList.add('d-none');
        }
    }
    tipoUsuario.addEventListener('change', actualizarCampos);
    actualizarCampos();
});