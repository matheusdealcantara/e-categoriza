import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request

from django.core.management.commands.test import Command as DjangoTestCommand


class Command(DjangoTestCommand):
    help = "Starts the server, runs tests, and stops the server after tests."

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

    def _wait_for_server(self, url='http://localhost:8000', timeout=30):
        """Poll the server until it's ready or timeout is reached."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with urllib.request.urlopen(url, timeout=5) as response:
                    if response.status == 200:
                        return  # Server is ready
            except (urllib.error.URLError, ConnectionResetError):
                pass  # Server not ready yet, continue polling
            time.sleep(1)  # Wait 1 second before retrying
        raise RuntimeError(f"Server at {url} did not become ready within {timeout} seconds.")