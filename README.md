# API — Sistema de Detección de Fraude

API construida con FastAPI que expone 3 de las consultas JOIN desarrolladas
en la Parte 1 de la evaluación, sobre el esquema de detección de fraude en
pagos (PostgreSQL).

## Endpoints

| Método | Ruta | Consulta que expone | Tipo de JOIN |
|---|---|---|---|
| GET | `/transacciones-detalle` | Detalle de cada transacción con titular y comercio | INNER JOIN (3 tablas) |
| GET | `/alertas-sin-asignar` | Alertas de fraude sin analista asignado | LEFT JOIN |
| GET | `/comercios-riesgo-alto` | Comercios con score de riesgo promedio > 50 | JOIN + GROUP BY / HAVING |

Documentación interactiva generada automáticamente: `/docs` (Swagger UI) y `/redoc` (ReDoc).

## Cómo correrlo en local

```bash
# 1. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar la base de datos
cp .env.example .env
# Edita .env y coloca tu propia cadena de conexión DATABASE_URL

# 4. Levantar el servidor en modo desarrollo
uvicorn main:app --reload

# 5. Abrir la documentación interactiva
# http://127.0.0.1:8000/docs
```

## Despliegue en producción

1. Verifica que `requirements.txt` tenga las versiones exactas (ya generado con `pip freeze`).
2. Nunca subas el archivo `.env` a git — está excluido en `.gitignore`. En la plataforma de despliegue, configura `DATABASE_URL` como variable de entorno desde su panel, no en el código.
3. El comando de arranque en producción está en `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
4. Si despliegas en **Render**: crea un nuevo "Web Service", conecta el repositorio, define `pip install -r requirements.txt` como build command, usa el comando del `Procfile` como start command, y agrega `DATABASE_URL` en la sección Environment.
5. La base de datos debe ser accesible desde el entorno donde despliegues la API (por ejemplo, una base PostgreSQL gestionada en la nube, no `localhost`).

## Estructura del proyecto

```
proyecto_api/
├── main.py           # Endpoints de la API
├── database.py        # Conexión a la base de datos (SQLAlchemy)
├── requirements.txt    # Dependencias exactas
├── Procfile            # Comando de arranque en producción
├── .env.example         # Plantilla de variables de entorno
├── .gitignore
└── README.md
```
