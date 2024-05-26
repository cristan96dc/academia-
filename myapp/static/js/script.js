document.addEventListener('DOMContentLoaded', function() {
    var menuToggle = document.querySelector('.menu-toggle');
    var navbarLinks = document.querySelector('.navbar-links');

    menuToggle.addEventListener('click', function() {
        navbarLinks.classList.toggle('active');
    });
})

        // Obtener el enlace de notificaciones y la ventana modal
        var notificacionesLink = document.getElementById("notificaciones");
        var modal = document.getElementById("modal");
        var notificacionesContent = document.getElementById("notificaciones-content");

        // Cuando se hace clic en el enlace de notificaciones, mostrar la ventana modal
        notificacionesLink.onclick = function() {
            // Hacer una solicitud AJAX para obtener el contenido de las notificaciones
            var xhr = new XMLHttpRequest();
            xhr.open("GET", notificacionesLink.getAttribute("data-url"), true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    // Insertar el contenido de las notificaciones dentro de la ventana modal
                    notificacionesContent.innerHTML = xhr.responseText;
                    modal.style.display = "block"; // Mostrar la ventana modal
                }
            };
            xhr.send();
        }

        // Cuando se hace clic en la X para cerrar la ventana modal, ocultarla
        document.getElementsByClassName("close")[0].onclick = function() {
            modal.style.display = "none";
        }

        // Cuando se hace clic fuera de la ventana modal, ocultarla
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }