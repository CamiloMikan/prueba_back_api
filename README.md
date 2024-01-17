# Prueba Back API

Este proyecto es una aplicación de prueba que implementa un REST API usando Django y Django REST Framework.

## Configuración del Entorno

1. **Clonar el Repositorio:**
   git clone https://github.com/CamiloMikan/prueba_back_api.git
   cd prueba_back_api

2. **Crear un Entorno Virtual:**
  python -m venv venv

3. **Activar el Entorno Virtual:**
  En Windows:
        venv\Scripts\activate
   
  En Linux/Mac:
        source venv/bin/activate

5. **Instalar Dependencias:**
   pip install -r requirements.txt

## Configuración de la Base de Datos

1. **Aplicar Migraciones:**
  python manage.py migrate

2. **Crear un Superusuario**
  python manage.py createsuperuser

## Ejecutar el Servidor de Desarrollo:
  python manage.py runserver

  ## Endpoints del API
  
**Listar Clientes:**
  GET /api/clients/

**Detalles de Cliente:**
  GET /api/clients/<id>/

**Crear Cliente:**
  POST /api/clients/

**Actualizar Cliente:**
  PUT /api/clients/<id>/

**Eliminar Cliente:**
  DELETE /api/clients/<id>/

