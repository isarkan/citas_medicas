async function cargar() {
    let res = await fetch("/datos")
    let data = await res.json()

    let lista = document.getElementById("lista")
    lista.innerHTML = ""

    data.forEach(p => {
        // lista.innerHTML += `<li>${p.id} - ${p.nombre} - ${p.edad}</li>`
    })
}

async function crear() {

    let data = {
        id: document.getElementById("id").value,
        nombre: document.getElementById("nombre").value,
        correo: document.getElementById("correo").value,
        fecha_nacimiento: document.getElementById("fecha_nacimiento").value,
        fecha_cita: document.getElementById("fecha_cita").value,
        hora_cita: document.getElementById("hora_cita").value,
        tipo_cita: document.getElementById("tipo_cita").value,
        codigo_cita: document.getElementById("codigo_cita").value,
        motivo: document.getElementById("motivo").value
    }

    await fetch("/crear", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })

    cargar()
}

cargar()