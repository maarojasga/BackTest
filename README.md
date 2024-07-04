# Proyecto FastAPI con Integración de HubSpot y ClickUp

Este proyecto implementa una API REST en Python usando FastAPI que permite crear contactos en HubSpot y sincronizarlos con ClickUp, al mismo tiempo que registra cada llamada en una base de datos PostgreSQL.

## Requisitos Previos

1. Python 3.7+
2. PostgreSQL
3. pip

## Configuración del proyecto

### 1. Clona el repositorio

Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/maarojasga/BackTest.git
cd BackTest
```

### 2. Crea y activa el entorno virtual

```bash
python -m venv env
source env/bin/activate 
```

### 3. Instala dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura variables de entorno

```plaintext
DATABASE_NAME=...
DATABASE_USER=...
DATABASE_HOST=...
DATABASE_PASSWORD=...
DATABASE_PORT=...
HUBSPOT_API_KEY=...
CLICKUP_API_KEY=...
CLICKUP_LIST_ID=...
```

### 5. Ejecuta0 la aplicación

```bash
uvicorn app.main:app --reload
```

### Bonus

Dentro del repositorio encontrarás la colección de Postman para poder probar la aplicación en local ¡Sólo debes importarla!