<?php
session_start(); // Obligatorio para manejar sesiones en PHP
header('Content-Type: application/json');

require_once __DIR__ . '/db.php';
try {
    $pdo = kronos_db();
} catch(PDOException $e) {
    echo json_encode(['success' => false, 'message' => 'Error de conexión a la base de datos.']);
    exit;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = trim($_POST['email'] ?? '');
    $pass = $_POST['password'] ?? '';

    if (empty($email) || empty($pass)) {
        echo json_encode(['success' => false, 'message' => 'Por favor, ingresa correo y contraseña.']);
        exit;
    }

    // Buscar al usuario por correo
    $stmt = $pdo->prepare("SELECT id, nombre_completo, password_hash FROM usuarios WHERE email = ?");
    $stmt->execute([$email]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    // Verificar si el usuario existe y la contraseña coincide
    if ($user && password_verify($pass, $user['password_hash'])) {
        
        // Regenerar el ID de sesión por seguridad (evita Session Fixation)
        session_regenerate_id(true);

        // Guardar datos en la sesión activa
        $_SESSION['usuario_id'] = $user['id'];
        $_SESSION['nombre'] = $user['nombre_completo'];
        $_SESSION['logged_in'] = true;

        echo json_encode(['success' => true]);
    } else {
        // Mensaje genérico por seguridad (no revelar si falló el correo o la clave)
        echo json_encode(['success' => false, 'message' => 'Credenciales incorrectas.']);
    }
}
?>