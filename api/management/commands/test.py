import os
import signal
import subprocess
import sys
import time

from django.core.management.commands.test import Command as DjangoTestCommand


class Command(DjangoTestCommand):
    help = "Starts the server, runs tests, and stops the server after tests."

    def handle(self, *args, **options):
        # Start the database using docker compose
        self.stdout.write(self.style.NOTICE('Starting database with Docker Compose...'))
        db_up = subprocess.run([
            'docker', 'compose', '-f', 'infra/compose.yaml', 'up', '-d'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if db_up.returncode != 0:
            self.stderr.write(self.style.ERROR('Failed to start database with Docker Compose.'))
            self.stderr.write(db_up.stderr.decode())
            return 1
        time.sleep(5)  # Wait for the database to be ready
        self.stdout.write(self.style.NOTICE('Database started.'))

        # Start the server in a subprocess
        server = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', '--noreload', '--insecure'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            self.stdout.write(self.style.NOTICE('Starting development server...'))
            time.sleep(5)  # Wait a few seconds for the server to be ready
            self.stdout.write(self.style.NOTICE('Development server started.'))

            # Run tests
            self.stdout.write(self.style.NOTICE('Running tests...'))
            result = super().handle(*args, **options)
        finally:
            # Stop the server
            self.stdout.write(self.style.NOTICE('Stopping development server...'))
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()

            # Stop the database service
            self.stdout.write(self.style.NOTICE('Stopping database with Docker Compose...'))
            db_down = subprocess.run([
                'docker', 'compose', '-f', 'infra/compose.yaml', 'down'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if db_down.returncode != 0:
                self.stderr.write(self.style.ERROR('Failed to stop database with Docker Compose.'))
                self.stderr.write(db_down.stderr.decode())
        return result
