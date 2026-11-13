<?php
// 1. Reanudar la sesión existente
session_start();

// 2. Vaciar todo el arreglo de variables de sesión
$_SESSION = array();

// 3. Si se desea destruir la sesión completamente, también se debe borrar la cookie de sesión.
// Esto destruirá la sesión, y no solo los datos de la sesión.
if (ini_get("session.use_cookies")) {
    $params = session_get_cookie_params();
    setcookie(session_name(), '', time() - 42000,
        $params["path"], $params["domain"],
        $params["secure"], $params["httponly"]
    );
}

// 4. Finalmente, destruir la sesión en el servidor
session_destroy();

// 5. Redirigir al usuario al formulario de login
header("Location: login.html");
exit;
?>