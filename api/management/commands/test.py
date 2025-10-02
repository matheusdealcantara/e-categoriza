import os
import subprocess
import time

from django.core.management.commands.test import Command as DjangoTestCommand


class Command(DjangoTestCommand):
    help = "Starts the server, runs tests, and stops the server after tests."

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
            # Start the database using docker compose
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

            self.stdout.write(self.style.SUCCESS('Database started.'))

        try:
            # Run tests
            self.stdout.write(self.style.NOTICE('Running tests...'))
            result = super().handle(*args, **options)
        finally:
            # Stop the server
            self.stdout.write(self.style.NOTICE('Stopping development server...'))

            if os.getenv('ENVIRONMENT') == 'development':
                # Stop the database service
                self.stdout.write(self.style.NOTICE('Stopping database with Docker Compose...'))
                db_down = subprocess.run([
                    'docker', 'compose', '-f', 'infra/compose.yaml', 'down'
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if db_down.returncode != 0:
                    self.stderr.write(self.style.ERROR('Failed to stop database with Docker Compose.'))
                    self.stderr.write(db_down.stderr.decode())
        return result