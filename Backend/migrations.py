from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
import os

def setup_migrations():
    """Setup Alembic migrations"""
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "migrations")
    alembic_cfg.set_main_option("sqlalchemy.url", os.getenv('DATABASE_URL', 'sqlite:///go_game.db'))
    
    # Create migrations directory if it doesn't exist
    if not os.path.exists("migrations"):
        command.init(alembic_cfg, "migrations")
    
    return alembic_cfg

def create_migration(message):
    """Create a new migration"""
    alembic_cfg = setup_migrations()
    command.revision(alembic_cfg, message=message, autogenerate=True)

def run_migrations():
    """Run all pending migrations"""
    alembic_cfg = setup_migrations()
    command.upgrade(alembic_cfg, "head")