# GogoCRM — Setup

## Instalación rápida (Windows)

```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# 2. Instalar dependencias
pip install django

# 3. Migrar base de datos
python manage.py migrate

# 4. Crear tu usuario
python manage.py createsuperuser

# 5. Arrancar
python manage.py runserver
```

Abre http://127.0.0.1:8000 e inicia sesión.

## Estructura
- Dashboard → resumen general
- Clientes → tus contactos
- Proyectos → cada proyecto con tareas, pagos y soporte
- Kanban → vista tipo Scrum por proyecto
- Pagos → control de cobros
- Soporte → tickets por proyecto
