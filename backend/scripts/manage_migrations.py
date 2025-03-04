import os
import sys
import subprocess
from pathlib import Path
import shutil
from alembic import command
from alembic.config import Config

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)

def reset_migrations():
    """Remove existing migrations and create a fresh one."""
    print("Removing existing migrations...")
    migrations_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "migrations")
    versions_dir = os.path.join(migrations_dir, "versions")
    
    if os.path.exists(versions_dir):
        shutil.rmtree(versions_dir)
        os.makedirs(versions_dir)
    
    print("Creating fresh migration...")
    alembic_cfg = Config("alembic.ini")
    try:
        # Create a new migration
        command.revision(alembic_cfg, autogenerate=True, message="initial_schema")
        print("Running migration...")
        # Run the migration
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"Error running command: {str(e)}")
        raise

def create_migration(message):
    """Create a new migration"""
    run_command(f"alembic revision --autogenerate -m '{message}'")
    print("Don't forget to review the migration before running it!")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_migrations.py reset  # Reset all migrations")
        print("  python manage_migrations.py create 'migration message'  # Create new migration")
        print("  python manage_migrations.py upgrade  # Run all pending migrations")
        sys.exit(1)

    command = sys.argv[1]
    if command == "reset":
        reset_migrations()
    elif command == "create":
        if len(sys.argv) < 3:
            print("Please provide a migration message")
            sys.exit(1)
        create_migration(sys.argv[2])
    elif command == "upgrade":
        run_command("alembic upgrade head")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main() 