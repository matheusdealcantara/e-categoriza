import os
import subprocess
import time

from django.core.management.commands.runserver import \
    Command as RunserverCommand


class Command(RunserverCommand):
    help = "Starts the development server."

    def wait_for_database(self):
        """Wait for the database container to be ready."""
        self.stdout.write(self.style.NOTICE('Waiting for database to be ready...'))
        
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            try:
                # Check if postgres-dev container is ready
                pg_check = subprocess.run([
                    'docker', 'exec', 'postgres-dev', 'pg_isready', 
                    '-U', os.getenv('POSTGRES_USER', 'local_user'),
                    '-d', os.getenv('POSTGRES_DB', 'local_db')
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                if pg_check.returncode == 0:
                    self.stdout.write(self.style.SUCCESS('Database is ready!'))
                    return True
                    
            except subprocess.SubprocessError:
                pass
            
            attempt += 1
            if attempt <= max_attempts:
                self.stdout.write(f'Attempt {attempt}/{max_attempts} - Database not ready, waiting...')
            time.sleep(2)
        
        self.stderr.write(self.style.ERROR('Database failed to become ready within timeout.'))
        return False

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
            
            if not self.wait_for_database():
                return 1
            
            self.stdout.write(self.style.NOTICE('Database started.'))


        try:
            self.stdout.write(self.style.NOTICE('Starting development server...'))
            super().handle(*args, **options)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error starting server: {e}'))
            return 1
