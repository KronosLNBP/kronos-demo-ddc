<?php
session_start();
header('Content-Type: application/json');

// Verificar si el usuario tiene sesión activa
if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
    echo json_encode(['success' => false, 'message' => 'Debes iniciar sesión.']);
    exit;
}

// Obtener los datos enviados por JavaScript (Fetch API)
$datos = json_decode(file_get_contents("php://input"), true);
$curso_id = $datos['curso_id'] ?? null;
$usuario_id = $_SESSION['usuario_id'];

if (!$curso_id) {
    echo json_encode(['success' => false, 'message' => 'ID de curso no válido.']);
    exit;
}

require_once __DIR__ . '/db.php';
try {
    $pdo = kronos_db();

    // 1. Verificar si el usuario ya está inscrito en este curso para evitar duplicados
    $stmt_check = $pdo->prepare("SELECT id FROM inscripciones WHERE usuario_id = ? AND curso_id = ?");
    $stmt_check->execute([$usuario_id, $curso_id]);
    
    if ($stmt_check->rowCount() > 0) {
        echo json_encode(['success' => false, 'message' => 'Ya estás inscrito en este curso.']);
        exit;
    }

    // 2. Insertar la nueva inscripción (con 0% de progreso al inicio)
    $stmt = $pdo->prepare("INSERT INTO inscripciones (usuario_id, curso_id, progreso) VALUES (?, ?, 0)");
    
    if ($stmt->execute([$usuario_id, $curso_id])) {
        echo json_encode(['success' => true, 'message' => 'Inscripción exitosa.']);
    } else {
        echo json_encode(['success' => false, 'message' => 'Error al procesar la inscripción.']);
    }

} catch(PDOException $e) {
    error_log($e->getMessage()); echo json_encode(['success' => false, 'message' => 'Error de base de datos.']);
}
?>