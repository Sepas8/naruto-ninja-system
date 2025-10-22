🍥 Sistema de Gestión de Ninjas - Konohagakure
Sistema monolítico cliente-servidor para la gestión de ninjas, misiones y asignaciones de la Aldea Oculta de la Hoja.

📋 Características
✅ Gestión completa de ninjas (CRUD)
✅ Gestión de misiones por rango
✅ Asignación inteligente de misiones con validación de rangos
✅ Sistema de reportes y estadísticas
✅ Interfaz web moderna y responsive
✅ API REST completa
✅ Base de datos PostgreSQL
✅ Dockerizado y listo para producción
🏗️ Arquitectura
Monolítica Cliente-Servidor:

Backend: Flask (Python) con SQLAlchemy
Frontend: HTML5, CSS3, JavaScript (Vanilla)
Base de Datos: PostgreSQL
Contenedorización: Docker + Docker Compose
📁 Estructura de Archivos
naruto-ninja-system/
│
├── app.py                      # Servidor Flask principal
├── models.py                   # Modelos de base de datos (ORM)
├── requirements.txt            # Dependencias Python
├── Dockerfile                  # Imagen Docker del servidor
├── docker-compose.yml          # Orquestación de servicios
├── .gitignore                  # Archivos a ignorar en Git
├── README.md                   # Este archivo
│
└── templates/
    └── index.html              # Cliente web (interfaz de usuario)
🚀 Instalación y Configuración
Prerrequisitos
Docker (versión 20.10 o superior)
Docker Compose (versión 2.0 o superior)
Paso 1: Clonar o crear el proyecto
Crea una carpeta para tu proyecto y organiza los archivos según la estructura mostrada arriba.

Paso 2: Construir y ejecutar con Docker
bash
# En el directorio raíz del proyecto

# Construir y levantar los contenedores
docker-compose up --build

# O en modo detached (segundo plano)
docker-compose up -d --build
Paso 3: Acceder a la aplicación
Una vez que los contenedores estén corriendo:

Interfaz Web: http://localhost:5000
API REST: http://localhost:5000/api
🛠️ Comandos Útiles
bash
# Ver logs
docker-compose logs -f

# Ver logs solo del servidor web
docker-compose logs -f web

# Detener los contenedores
docker-compose down

# Detener y eliminar volúmenes (borra la base de datos)
docker-compose down -v

# Reiniciar solo el servidor web
docker-compose restart web

# Acceder al contenedor del servidor
docker-compose exec web bash

# Acceder a PostgreSQL
docker-compose exec db psql -U naruto_user -d naruto_db
📡 Endpoints de la API
Ninjas
GET /api/ninjas - Listar todos los ninjas
GET /api/ninjas/<id> - Consultar un ninja específico
POST /api/ninjas - Registrar un nuevo ninja
PUT /api/ninjas/<id> - Actualizar un ninja
DELETE /api/ninjas/<id> - Eliminar un ninja
Misiones
GET /api/misiones - Listar todas las misiones
GET /api/misiones/<id> - Consultar una misión específica
POST /api/misiones - Registrar una nueva misión
DELETE /api/misiones/<id> - Eliminar una misión
Asignaciones
GET /api/asignaciones - Listar todas las asignaciones
POST /api/asignaciones - Asignar una misión a un ninja
PUT /api/asignaciones/<id>/completar - Marcar misión como completada
Reportes
GET /api/reportes/ninjas - Reporte detallado de ninjas
GET /api/reportes/misiones - Reporte detallado de misiones
📊 Modelo de Datos
Ninja
id: Integer (PK)
nombre: String
rango: String (Genin, Chūnin, Jōnin)
ataque: Integer
defensa: Integer
chakra: Integer
aldea: String
jutsus: Text
fecha_registro: DateTime
Mision
id: Integer (PK)
nombre: String
rango: String (D, C, B, A, S)
recompensa: Integer
descripcion: Text
fecha_creacion: DateTime
AsignacionMision
id: Integer (PK)
ninja_id: Integer (FK)
mision_id: Integer (FK)
fecha_asignacion: DateTime
fecha_completado: DateTime
completada: Boolean
🔧 Variables de Entorno
El archivo docker-compose.yml ya incluye las variables necesarias:

yaml
DATABASE_URL: postgresql://naruto_user:konoha123@db:5432/naruto_db
POSTGRES_USER: naruto_user
POSTGRES_PASSWORD: konoha123
POSTGRES_DB: naruto_db
🧪 Ejemplos de Uso con cURL
bash
# Registrar un ninja
curl -X POST http://localhost:5000/api/ninjas \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Naruto Uzumaki",
    "rango": "Genin",
    "ataque": 70,
    "defensa": 60,
    "chakra": 150,
    "aldea": "Konohagakure",
    "jutsus": "Rasengan,Kage Bunshin"
  }'

# Registrar una misión
curl -X POST http://localhost:5000/api/misiones \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Rescatar al gato Tora",
    "rango": "D",
    "recompensa": 500,
    "descripcion": "Encontrar y capturar al gato perdido"
  }'

# Asignar misión
curl -X POST http://localhost:5000/api/asignaciones \
  -H "Content-Type: application/json" \
  -d '{
    "ninja_id": 1,
    "mision_id": 1
  }'
🐛 Solución de Problemas
El contenedor de base de datos no inicia
bash
docker-compose down -v
docker-compose up --build
Error de conexión a la base de datos
Verifica que el servicio de base de datos esté saludable:

bash
docker-compose ps
Puerto 5000 ya está en uso
Cambia el puerto en docker-compose.yml:

yaml
ports:
  - "8080:5000"  # Usar puerto 8080 en vez de 5000
📝 Notas Adicionales
La base de datos se persiste en un volumen Docker llamado postgres_data
Los cambios en el código Python se reflejan automáticamente (hot reload)
Para producción, considera cambiar FLASK_ENV a production y usar un servidor WSGI como Gunicorn
👨‍💻 Desarrollo
Para desarrollo sin Docker:

bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variable de entorno
export DATABASE_URL="postgresql://naruto_user:konoha123@localhost:5432/naruto_db"

# Ejecutar servidor
python app.py
📄 Licencia
Este proyecto es de código abierto y está disponible bajo la licencia MIT.

Desarrollado por el equipo de Konohagakure 🍥

