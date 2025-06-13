from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import sys
from pathlib import Path
from app.models import *  # Importa todos tus modelos
from sqlmodel import SQLModel
from app.database import engine  # Importa tu motor configurado

# Agrega el directorio del proyecto al path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Este es el objeto de configuración de Alembic
config = context.config

# Configura el logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Configuración clave: metadata de SQLModel
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Importante para detectar cambios de tipo
        render_as_batch=True,  # Necesario para SQLite
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online' usando tu motor configurado."""
    # Conexión directa con tu motor configurado en database.py
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Detecta cambios en tipos de columnas
            render_as_batch=True,  # Necesario para operaciones batch en SQLite
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()