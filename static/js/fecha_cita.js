flatpickr("#fecha_cita", {
    dateFormat: "Y-m-d",
    // Mínimo: mañana
    minDate: new Date().fp_incr(1),
    // Máximo: último día del siguiente mes
    maxDate: (function () {
        let hoy = new Date();
        // Ir al siguiente mes
        let siguienteMes = new Date(hoy.getFullYear(), hoy.getMonth() + 2, 0);
        // +2 y día 0 = último día del siguiente mes
        return siguienteMes;
    })(),
    // Bloquear sábados y domingos
    disable: [
        function (date) {
            return (date.getDay() === 0 || date.getDay() === 6);
        }
    ]
});