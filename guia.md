



# Verificar versión de Docker Compose
docker-compose --version


```

Construir y ejecutar el proyecto

Desde la carpeta raíz del proyecto (`naruto-ninja-system/`):

```bash
#Construir las imágenes y levantar los contenedores
docker-compose up --build
```

Verificar que todo funciona

Verás logs similares a:

```
naruto_db    | database system is ready to accept connections
naruto_web   | * Running on all addresses (0.0.0.0)
naruto_web   | * Running on http://127.0.0.1:5000
naruto_web   | * Running on http://172.18.0.3:5000
```

Acceder a la aplicación

Abre tu navegador y visita:

**http://localhost:5000**


##  Probar la aplicación

1. **Registra un ninja:**
   - Ve a la pestaña "Ninjas"
   - Completa el formulario
   - Haz clic en "Registrar Ninja"

2. **Crea una misión:**
   - Ve a la pestaña "Misiones"
   - Completa el formulario
   - Haz clic en "Registrar Misión"

3. **Asigna una misión:**
   - Ve a la pestaña "Asignaciones"
   - Selecciona un ninja y una misión
   - Haz clic en "Asignar Misión"

4. **Ver reportes:**
   - Ve a la pestaña "Reportes"
   - Haz clic en "Generar Reporte de Ninjas"

## Comandos útiles para gestionar la aplicación

### Detener la aplicación:
```bash
# Presiona Ctrl+C en la terminal donde está corriendo

# O en otra terminal:
docker-compose down
```

### Reiniciar la aplicación:
```bash
docker-compose restart
```

### Ver logs en tiempo real:
```bash
docker-compose logs -f
```

### Limpiar todo (incluyendo base de datos):
```bash
docker-compose down -v
```

### Ejecutar en segundo plano:
```bash
docker-compose up -d
```

### Ver estado de los contenedores:
```bash
docker-compose ps
```

## Solución de problemas comunes

### Error: "Port 5000 is already in use"
```bash
# Opción 1: Detener el proceso que usa el puerto
sudo lsof -i :5000
kill -9 <PID>

# Opción 2: Cambiar el puerto en docker-compose.yml
# En la sección web, cambiar:
ports:
  - "8080:5000"  # Ahora usar http://localhost:8080
```

### Error: "Cannot connect to Docker daemon"
```bash
# Iniciar Docker
sudo systemctl start docker

# O en macOS/Windows, asegúrate de que Docker Desktop esté corriendo
```

### Error: "Database connection failed"
```bash
# Esperar unos segundos más, la base de datos puede tardar en iniciar
# O reiniciar los contenedores:
docker-compose down
docker-compose up
```

### Los cambios no se reflejan
```bash
# Reconstruir las imágenes
docker-compose up --build
```

## Acceder a la base de datos directamente

Si necesitas revisar o modificar datos directamente:

```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U naruto_user -d naruto_db

# Comandos útiles en PostgreSQL:
\dt                    # Listar tablas
SELECT * FROM ninjas;  # Ver todos los ninjas
SELECT * FROM misiones;
\q                     # Salir