// Definimos el tiempo de inactividad en milisegundos (3 minutos)
const INACTIVITY_TIMEOUT = 3 * 60 * 1000;

let inactivityTimer;

// Función para redirigir a la página de cierre de sesión
function logout() {
    // Usamos window.location.href para forzar la recarga de la página de login
    window.location.href = '/logout/'; 
}

// Función para reiniciar el temporizador de inactividad
function resetInactivityTimer() {
    // Limpiamos el temporizador anterior
    clearTimeout(inactivityTimer);
    // Creamos un nuevo temporizador
    inactivityTimer = setTimeout(logout, INACTIVITY_TIMEOUT);
}

// Event listeners para detectar actividad del usuario
// Reinicia el temporizador con cada uno de estos eventos
window.addEventListener('mousemove', resetInactivityTimer);
window.addEventListener('mousedown', resetInactivityTimer);
window.addEventListener('keypress', resetInactivityTimer);
window.addEventListener('touchmove', resetInactivityTimer);
window.addEventListener('scroll', resetInactivityTimer);

// Iniciar el temporizador por primera vez
resetInactivityTimer();

console.log("Mecanismo de cierre de sesión por inactividad iniciado.");
