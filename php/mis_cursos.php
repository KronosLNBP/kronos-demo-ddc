<?php
session_start();
// Validar si el usuario está autenticado
if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
    header("Location: login.html");
    exit;
}

$usuario_id = $_SESSION['usuario_id'];

// Configuración de la conexión a la base de datos (PDO)
require_once __DIR__ . '/db.php';
try {
    $pdo = kronos_db();
    
    // Consulta para obtener solo los cursos del usuario activo
    $sql = "SELECT c.id, c.titulo, c.categoria, c.icono, i.progreso 
            FROM inscripciones i
            INNER JOIN cursos c ON i.curso_id = c.id
            WHERE i.usuario_id = :usuario_id
            ORDER BY i.fecha_inscripcion DESC";
            
    $stmt = $pdo->prepare($sql);
    $stmt->execute(['usuario_id' => $usuario_id]);
    $cursos_inscritos = $stmt->fetchAll(PDO::FETCH_ASSOC);

} catch(PDOException $e) {
    error_log($e->getMessage()); die("Error de conexión. Intenta más tarde.");
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mis Cursos | kronosMedicine</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-900 text-gray-100 font-sans antialiased overflow-x-hidden">

    <!-- Navegación Sticky -->
    <header class="sticky top-0 z-50 bg-gray-900 border-b border-gray-800 shadow-md">
        <!-- ... (Mantén exactamente el mismo header y menú móvil de la versión anterior) ... -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <div class="flex-shrink-0 flex items-center cursor-pointer">
                    <a href="index.php"><span class="text-2xl font-bold tracking-tight text-blue-500">kronos<span class="text-white">Medicine</span></span></a>
                </div>
                <nav class="hidden md:flex space-x-8">
                    <a href="index.php" class="text-gray-300 hover:text-blue-400 px-1 py-2 text-sm font-medium transition-colors">Catálogo</a>
                    <a href="mis_cursos.php" class="text-blue-400 border-b-2 border-blue-400 px-1 py-2 text-sm font-medium">Mis Cursos</a>
                    <a href="#" class="text-gray-300 hover:text-blue-400 px-1 py-2 text-sm font-medium transition-colors">Comunidad</a>
                </nav>
                <div class="hidden md:flex items-center space-x-4">
                    <div class="flex items-center space-x-2">
                        <div class="bg-gray-700 h-8 w-8 rounded-full flex items-center justify-center text-sm font-bold text-blue-400">
                            <?php echo strtoupper(substr($_SESSION['nombre'], 0, 1)); ?>
                        </div>
                        <span class="text-gray-300 text-sm font-medium">Hola, <?php echo htmlspecialchars($_SESSION['nombre']); ?></span>
                    </div>
                    <a href="logout.php" class="border border-red-600/50 hover:bg-red-600 hover:text-white text-red-400 px-4 py-2 rounded-md text-sm font-medium transition-colors">Salir</a>
                </div>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 min-h-screen">
        <div class="mb-10">
            <h1 class="text-3xl font-bold text-white mb-2">Mi Aprendizaje</h1>
            <p class="text-gray-400 text-lg">Continúa donde te quedaste y alcanza tus metas.</p>
        </div>

        <?php if (empty($cursos_inscritos)): ?>
            <!-- Estado vacío: El usuario no tiene cursos -->
            <div class="bg-gray-800 border border-gray-700 rounded-lg p-10 text-center flex flex-col items-center">
                <i class="fas fa-folder-open text-6xl text-gray-600 mb-4"></i>
                <h3 class="text-xl font-bold text-white mb-2">Aún no tienes cursos</h3>
                <p class="text-gray-400 mb-6">Explora nuestro catálogo y comienza tu formación médica hoy mismo.</p>
                <a href="index.php" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-md transition-colors duration-300">
                    Ir al Catálogo
                </a>
            </div>
        <?php else: ?>
            <!-- Grid de Cursos Dinámico -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                
                <?php foreach ($cursos_inscritos as $curso): ?>
                    
                    <?php 
                    // Determinar estilos según el progreso
                    $es_completado = ($curso['progreso'] >= 100);
                    $color_tema = $es_completado ? 'green' : 'blue';
                    $texto_estado = $es_completado ? 'Completado' : 'En curso';
                    ?>

                    <article class="bg-gray-800 rounded-lg overflow-hidden shadow-lg border border-gray-700 hover:border-<?php echo $color_tema; ?>-500 transition-colors duration-300 flex flex-col relative">
                        
                        <!-- Etiqueta de estado -->
                        <div class="absolute top-2 right-2 bg-<?php echo $color_tema; ?>-600 text-white text-xs font-bold px-2 py-1 rounded z-10">
                            <?php echo $texto_estado; ?>
                        </div>

                        <div class="relative h-40 bg-gray-700 overflow-hidden flex items-center justify-center">
                            <i class="fas <?php echo htmlspecialchars($curso['icono']); ?> text-5xl text-gray-500"></i>
                            
                            <?php if (!$es_completado): ?>
                            <!-- Botón Play Overlay solo si no está completado -->
                            <div class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity duration-300 cursor-pointer">
                                <i class="fas fa-play-circle text-4xl text-white"></i>
                            </div>
                            <?php endif; ?>
                        </div>
                        
                        <div class="p-5 flex-1 flex flex-col">
                            <span class="text-xs font-semibold text-<?php echo $color_tema; ?>-400 uppercase tracking-wider mb-2 block">
                                <?php echo htmlspecialchars($curso['categoria']); ?>
                            </span>
                            <h2 class="text-lg font-bold text-white mb-4 line-clamp-2">
                                <?php echo htmlspecialchars($curso['titulo']); ?>
                            </h2>
                            
                            <!-- Barra de progreso dinámica -->
                            <div class="mt-auto">
                                <div class="flex justify-between text-xs mb-1">
                                    <span class="text-gray-400">Progreso</span>
                                    <span class="text-<?php echo $color_tema; ?>-400 font-bold"><?php echo $curso['progreso']; ?>%</span>
                                </div>
                                <div class="w-full bg-gray-700 rounded-full h-2 mb-4">
                                    <div class="bg-<?php echo $color_tema; ?>-500 h-2 rounded-full" style="width: <?php echo $curso['progreso']; ?>%"></div>
                                </div>
                                
                                <?php if ($es_completado): ?>
                                    <div class="flex space-x-2">
                                        <a href="reproductor.php?id=<?php echo $curso['id']; ?>" class="flex-1 text-center bg-gray-700 hover:bg-gray-600 text-white font-medium py-2 px-2 rounded transition-colors duration-300 text-sm">
                                            Repasar
                                        </a>
                                        <a href="certificado.php?id=<?php echo $curso['id']; ?>" class="flex-1 text-center border border-green-500 text-green-400 hover:bg-green-500 hover:text-white font-medium py-2 px-2 rounded transition-colors duration-300 text-sm">
                                            Certificado
                                        </a>
                                    </div>
                                <?php else: ?>
                                    <a href="reproductor.php?id=<?php echo $curso['id']; ?>" class="block w-full text-center bg-gray-700 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded transition-colors duration-300">
                                        Continuar clase
                                    </a>
                                <?php endif; ?>
                            </div>
                        </div>
                    </article>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
    </main>

</body>
</html>