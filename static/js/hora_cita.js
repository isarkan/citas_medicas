function generarHoras() {
    let horas = [];

    function agregarRango(inicio, fin) {
        let [h, m] = inicio.split(":").map(Number);
        let [hFin, mFin] = fin.split(":").map(Number);

        let fecha = new Date();
        fecha.setHours(h, m, 0);

        while (true) {
            let hora = fecha.getHours().toString().padStart(2, "0");
            let min = fecha.getMinutes().toString().padStart(2, "0");
            horas.push(`${hora}:${min}`);

            // salir cuando llegue al límite
            if (hora == hFin.toString().padStart(2, "0") &&
                min == mFin.toString().padStart(2, "0")) break;

            fecha.setMinutes(fecha.getMinutes() + 30);
        }
    }

    // Rangos permitidos
    agregarRango("08:00", "11:30");
    agregarRango("14:00", "17:30");

    return horas;
}

flatpickr("#hora_cita", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    minuteIncrement: 30,

    enable: generarHoras()
});