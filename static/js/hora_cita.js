flatpickr("#hora_cita", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    minuteIncrement: 30,
    allowInput: false,

    minTime: "08:00",
    maxTime: "17:30",

    onChange: function(selectedDates, dateStr, instance) {
        if (!selectedDates.length) return;

        let fecha = selectedDates[0];
        let hora = fecha.getHours();
        let minutos = fecha.getMinutes();

        // ❌ BLOQUEAR TODO LO QUE NO SEA válido
        const esValido =
            (hora >= 8 && (hora < 11 || (hora === 11 && minutos <= 30))) ||
            (hora >= 14 && (hora < 17 || (hora === 17 && minutos <= 30)));

        if (!esValido) {
            instance.clear(); // borra la hora inválida
        }
    }
});