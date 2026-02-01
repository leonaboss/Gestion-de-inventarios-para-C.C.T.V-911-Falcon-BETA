# Sistema de Gestión de Inventarios

## Descripción General

Este es un sistema de gestión de inventarios desarrollado como un proyecto universitario para T.S.U. en Informática. La aplicación está construida con Django y permite una gestión detallada de productos, movimientos de inventario y control de usuarios con diferentes niveles de acceso.

## Características Principales

- **Gestión de Usuarios:**
  - Registro público de usuarios.
  - Roles de administrador y usuario regular con permisos diferenciados.
  - Flujo de recuperación de contraseña personalizado mediante una frase de seguridad.

- **Módulo de Inventario:**
  - Creación, Edición, y Eliminación de productos (CRUD).
  - Modelo de datos detallado por producto, incluyendo código, descripción, ubicación, etc.
  - Registro y seguimiento de todos los movimientos (entradas/salidas) para un historial completo de auditoría.
  - Funcionalidad para importar y exportar el listado de productos a través de archivos Excel.

- **Panel de Administración:**
  - Panel dedicado para que los administradores gestionen usuarios y tengan una visión general del sistema.

## Tecnología Utilizada

- **Backend:** Python, Django
- **Base de Datos:** MySQL (según la configuración)
- **Frontend:** HTML, CSS, JavaScript
- **Librerías Python Clave:**
  - `django`: Framework web principal.
  - `mysqlclient`: Conector para la base de datos MySQL.
  - `openpyxl`: Para leer y escribir archivos Excel (.xlsx).
  - `python-decouple`: Para gestionar variables de entorno.

## Instalación y Puesta en Marcha

Sigue estos pasos para configurar y ejecutar el proyecto en un entorno de desarrollo local.

1.  **Prerrequisitos:**
    - Tener Python 3.11 instalado.
    - Tener una instancia de MySQL en ejecución.

2.  **Clonar el Repositorio:**

    ```bash
    git clone <URL-del-repositorio>
    cd nombre-del-directorio
    ```

3.  **Instalar Dependencias:**
    Crea un entorno virtual (recomendado) y luego instala las dependencias listadas en `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la Base de Datos:**
    Asegúrate de que los detalles de conexión a tu base de datos en `sistema_inv/settings.py` sean correctos. La configuración actual utiliza `python-decouple` para leer desde un archivo `.env`.

5.  **Aplicar Migraciones:**
    Ejecuta las migraciones para crear las tablas en la base de datos.

    ```bash
    python manage.py migrate
    ```

6.  **Crear un Superusuario:**
    Para acceder al panel de administración de Django, necesitarás un superusuario.

    ```bash
    python manage.py createsuperuser
    ```

7.  **Ejecutar el Servidor:**
    Puedes iniciar el servidor de desarrollo utilizando el script proporcionado:
    ```bash
    start_server.bat
    ```
    O directamente con manage.py:
    ```bash
    python manage.py runserver
    ```
    La aplicación estará disponible en `http://127.0.0.1:8000`.

## Estructura del Proyecto

- `sistema_inv/`: Directorio principal del proyecto Django.
  - `settings.py`: Archivo de configuración principal.
  - `urls.py`: Rutas URL principales del proyecto.

- `inventario/`: Aplicación Django que maneja toda la lógica del inventario (modelos, vistas, urls).

- `usuarios/`: Aplicación Django para la gestión de usuarios, perfiles y autenticación.

- `static/`: Contiene los archivos estáticos (CSS, JavaScript, imágenes).

- `template/`: Contiene las plantillas HTML que renderiza Django.

- `manage.py`: Utilidad de línea de comandos de Django.
