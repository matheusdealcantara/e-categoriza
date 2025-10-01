import os
import subprocess

from django.core.management.commands.migrate import Command as MigrateCommand


class Command(MigrateCommand):
    help = "Applies database migrations, starting the database with Docker Compose if in development environment."

    def handle(self, *args, **options):
        if os.getenv('ENVIRONMENT') == 'development':
            self.stdout.write(self.style.NOTICE('Starting database with Docker Compose...'))
            db_up = subprocess.run([
                'docker', 'compose', '-f', 'infra/compose.yaml', 'up', '-d'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if db_up.returncode != 0:
                self.stderr.write(self.style.ERROR('Failed to start database with Docker Compose.'))
                self.stderr.write(db_up.stderr.decode())
                return 1
            self.stdout.write(self.style.NOTICE('Database started.'))

        try:
            super().handle(*args, **options)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error during migration: {e}'))
            return 1
        return 0