# Versión PHP + MySQL (hosting Apache)

Estos archivos son la versión de la plataforma con base de datos MySQL (registro, inicio de sesión, mis cursos, inscripción y reproductor). **No funcionan en GitHub Pages**, que solo sirve archivos estáticos: se suben al hosting Apache de kronosmedicine.com.mx.

## Instalación

1. Sube la carpeta `php/` a tu hosting.
2. Copia `config.example.php` como `config.php` y pon tus datos de MySQL. Lo ideal es que `config.php` quede fuera de `public_html`; si lo mueves, ajusta la ruta en `db.php`.
3. `config.php` está en `.gitignore`: **nunca lo subas a GitHub**.

## Importante

- La contraseña de la base de datos estaba escrita dentro de los archivos originales. Si esos archivos estuvieron en algún lugar público, **cambia la contraseña** desde el panel del hosting.
- La plataforma principal usa Firebase (login con Google). Conviene elegir un solo sistema de usuarios para no tener dos cuentas por alumno.
