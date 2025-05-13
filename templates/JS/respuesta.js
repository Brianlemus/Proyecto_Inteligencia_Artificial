
    const leidoRadios = document.getElementsByName("leido");
    const resueltoRadios = document.getElementsByName("resuelto");
    const segundaPregunta = document.getElementById("segundaPregunta");
    const form = document.getElementById("ticketForm");
    const mensaje = document.getElementById("mensaje");

    leidoRadios.forEach(radio => {
      radio.addEventListener("change", () => {
        if (radio.value === "si") {
          segundaPregunta.classList.remove("d-none");
          mensaje.textContent = "";
        } else {
          segundaPregunta.classList.add("d-none");
          mensaje.textContent = "Por favor lea las indicaciones antes de continuar.";
        }
      });
    });

    form.addEventListener("submit", function(e) {
      e.preventDefault();

      const leido = document.querySelector('input[name="leido"]:checked');
      const resuelto = document.querySelector('input[name="resuelto"]:checked');

      if (!leido) {
        mensaje.textContent = "Seleccione una opción en la primera pregunta.";
        return;
      }

      if (leido.value === "no") {
        mensaje.textContent = "Por favor lea las indicaciones antes de generar un ticket.";
        return;
      }

      if (!resuelto) {
        mensaje.textContent = "Seleccione una opción en la segunda pregunta.";
        return;
      }

      if (resuelto.value === "si") {
        mensaje.textContent = "¡Perfecto! No es necesario generar un ticket.";
      } else {
        mensaje.textContent = "Ticket generado correctamente.";
        window.location.href = "crearticket.html";
      }
    });
  