<?php
session_start();

// 1. Validar sesión
if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
    header("Location: login.html");
    exit;
}

// 2. Obtener el ID del curso de la URL
$curso_id = $_GET['id'] ?? null;
$usuario_id = $_SESSION['usuario_id'];

if (!$curso_id) {
    // Si no hay ID en la URL, lo regresamos a sus cursos
    header("Location: mis_cursos.php");
    exit;
}

require_once __DIR__ . '/db.php';
try {
    $pdo = kronos_db();

    // 3. Consulta estricta: Obtener datos del curso SÓLO SI el usuario está inscrito
    $sql = "SELECT c.titulo, c.descripcion, c.video_url, i.progreso 
            FROM cursos c 
            INNER JOIN inscripciones i ON c.id = i.curso_id 
            WHERE c.id = :curso_id AND i.usuario_id = :usuario_id";
            
    $stmt = $pdo->prepare($sql);
    $stmt->execute(['curso_id' => $curso_id, 'usuario_id' => $usuario_id]);
    $curso = $stmt->fetch(PDO::FETCH_ASSOC);

    // Si la consulta no devuelve nada, significa que no lo ha comprado o no existe
    if (!$curso) {
        die("<div style='background: #1f2937; color: white; padding: 50px; text-align: center; font-family: sans-serif;'>
                <h2 style='color: #ef4444;'>Acceso Denegado</h2>
                <p>No tienes acceso a este curso o no existe.</p>
                <a href='mis_cursos.php' style='color: #3b82f6;'>Volver a Mis Cursos</a>
             </div>");
    }

} catch(PDOException $e) {
    error_log($e->getMessage()); die("Error de base de datos. Intenta más tarde.");
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo htmlspecialchars($curso['titulo']); ?> | kronosMedicine</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        /* Deshabilitar selección de texto para añadir una capa básica de protección anticopia */
        body { user-select: none; }
    </style>
</head>
<body class="bg-gray-950 text-gray-100 font-sans antialiased h-screen flex flex-col" oncontextmenu="return false;">

    <!-- Barra de navegación minimalista para el reproductor -->
    <header class="bg-gray-900 border-b border-gray-800 shadow-sm py-4 px-6 flex justify-between items-center shrink-0">
        <div class="flex items-center space-x-4">
            <a href="mis_cursos.php" class="text-gray-400 hover:text-white transition-colors flex items-center space-x-2">
                <i class="fas fa-arrow-left"></i>
                <span class="text-sm font-medium hidden sm:inline">Volver a Mis Cursos</span>
            </a>
            <div class="h-6 w-px bg-gray-700 hidden sm:block"></div>
            <h1 class="text-white font-semibold truncate max-w-md lg:max-w-2xl">
                <?php echo htmlspecialchars($curso['titulo']); ?>
            </h1>
        </div>
        
        <!-- Progreso actual mostrado en la esquina -->
        <div class="flex items-center space-x-3">
            <span class="text-xs text-gray-400">Progreso:</span>
            <div class="w-24 bg-gray-700 rounded-full h-2">
                <div class="bg-blue-500 h-2 rounded-full" style="width: <?php echo $curso['progreso']; ?>%"></div>
            </div>
            <span class="text-xs font-bold text-blue-400"><?php echo $curso['progreso']; ?>%</span>
        </div>
    </header>

    <!-- Contenedor del Video -->
    <main class="flex-1 flex flex-col lg:flex-row overflow-hidden">
        
        <!-- Área principal (Video) -->
        <div class="flex-1 bg-black flex flex-col justify-center relative shadow-2xl overflow-y-auto">
            <div class="w-full max-w-5xl mx-auto px-4 py-8">
                
                <!-- Reproductor HTML5 -->
                <div class="aspect-w-16 aspect-h-9 bg-gray-900 rounded-xl overflow-hidden border border-gray-800 mb-6">
                    <!-- controlsList="nodownload" oculta el botón de descargar en navegadores modernos -->
                    <video controls controlsList="nodownload" class="w-full h-full object-contain" poster="https://via.placeholder.com/1280x720/1f2937/3b82f6?text=Cargando+Clase...">
                        <source src="<?php echo htmlspecialchars($curso['video_url']); ?>" type="video/mp4">
                        Tu navegador no soporta la reproducción de este video.
                    </video>
                </div>

                <!-- Título y Descripción debajo del video -->
                <div class="bg-gray-900 p-6 rounded-xl border border-gray-800">
                    <h2 class="text-2xl font-bold text-white mb-2"><?php echo htmlspecialchars($curso['titulo']); ?></h2>
                    <p class="text-gray-400 leading-relaxed">
                        <?php echo htmlspecialchars($curso['descripcion']); ?>
                    </p>
                </div>
            </div>
        </div>

    </main>

    <!-- Script básico anticopia -->
    <script>
        // Prevenir atajos de teclado comunes para guardar/inspeccionar (Ctrl+S, F12, etc.)
        document.addEventListener('keydown', function(e) {
            if (e.key === 'F12' || 
               (e.ctrlKey && e.shiftKey && e.key === 'I') || 
               (e.ctrlKey && e.key === 's') || 
               (e.ctrlKey && e.key === 'p')) {
                e.preventDefault();
            }
        });
    </script>
</body>
</html>