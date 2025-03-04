from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from models import Base  # Import our SQLAlchemy Base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# this is the Alembic Config object
config = context.config

# Set the sqlalchemy url from environment variable
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for migrations
target_metadata = Base.metadata  # Use our SQLAlchemy models

# ... rest of the file remains the same ... 