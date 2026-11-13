<?php
header('Content-Type: application/json');

require_once __DIR__ . '/db.php';
try {
    $pdo = kronos_db();
} catch(PDOException $e) {
    echo json_encode(['success' => false, 'message' => 'Error de conexión a la base de datos.']);
    exit;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = trim($_POST['nombre'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $pass = $_POST['password'] ?? '';

    // Validaciones básicas
    if (empty($nombre) || empty($email) || empty($pass)) {
        echo json_encode(['success' => false, 'message' => 'Todos los campos son obligatorios.']);
        exit;
    }

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo json_encode(['success' => false, 'message' => 'El formato del correo es inválido.']);
        exit;
    }

    // Verificar si el correo ya existe
    $stmt = $pdo->prepare("SELECT id FROM usuarios WHERE email = ?");
    $stmt->execute([$email]);
    if ($stmt->rowCount() > 0) {
        echo json_encode(['success' => false, 'message' => 'Este correo ya está registrado.']);
        exit;
    }

    // Encriptar la contraseña
    $hash = password_hash($pass, PASSWORD_DEFAULT);

    // Insertar nuevo usuario
    $sql = "INSERT INTO usuarios (nombre_completo, email, password_hash) VALUES (?, ?, ?)";
    $stmt = $pdo->prepare($sql);
    
    if ($stmt->execute([$nombre, $email, $hash])) {
        echo json_encode(['success' => true, 'message' => 'Registro exitoso. Ya puedes iniciar sesión.']);
    } else {
        echo json_encode(['success' => false, 'message' => 'Hubo un error al registrar el usuario.']);
    }
}
?>