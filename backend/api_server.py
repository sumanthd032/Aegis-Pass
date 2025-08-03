import json
from wsgiref.simple_server import make_server
import sys
import os

# --- Add the 'logic' directory to the Python path ---
# This allows us to import from the 'logic' module.
# It finds the path of the current script ('api_server.py') and adds the 'logic'
# subdirectory to the places Python looks for modules.
sys.path.append(os.path.join(os.path.dirname(__file__), 'logic'))

# --- Import the core logic functions ---
# Now that the path is set, we can import our logic functions.
from password_logic import (
    generate_random_password,
    generate_memorable_password,
    calculate_strength
)

# --- WSGI Application ---

def application(environ, start_response):
    """The main WSGI application to handle HTTP requests."""
    
    headers = [
        ('Content-type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'POST, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type')
    ]

    if environ['REQUEST_METHOD'] == 'OPTIONS':
        status = '200 OK'
        start_response(status, headers)
        return []

    path = environ.get('PATH_INFO', '/')

    if path == '/generate' and environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            data = json.loads(request_body)

            gen_type = data.get('type', 'random')
            count = min(int(data.get('count', 1)), 10)
            passwords = []
            strength_info = {}

            for _ in range(count):
                if gen_type == 'random':
                    password, pool_size = generate_random_password(
                        length=int(data.get('length', 16)),
                        use_uppercase=bool(data.get('use_uppercase', True)),
                        use_lowercase=bool(data.get('use_lowercase', True)),
                        use_numbers=bool(data.get('use_numbers', True)),
                        use_special=bool(data.get('use_special', True)),
                        exclude_similar=bool(data.get('exclude_similar', False))
                    )
                else: # memorable
                    password, pool_size = generate_memorable_password(
                        word_count=int(data.get('word_count', 4)),
                        separator=data.get('separator', '-')
                    )
                
                if password:
                    passwords.append(password)
                    strength_info[password] = calculate_strength(password, pool_size)

            if not passwords:
                raise ValueError("Could not generate password with given constraints.")

            response_data = json.dumps({'passwords': passwords, 'strength': strength_info})
            status = '200 OK'
            start_response(status, headers)
            return [response_data.encode('utf-8')]

        except Exception as e:
            status = '400 Bad Request'
            start_response(status, headers)
            error_response = json.dumps({'error': str(e)})
            return [error_response.encode('utf-8')]

    else:
        status = '404 Not Found'
        start_response(status, headers)
        return [json.dumps({'error': 'Not Found'}).encode('utf-8')]

# --- Main execution block to run the server ---
if __name__ == '__main__':
    HOST, PORT = 'localhost', 8080
    with make_server(HOST, PORT, application) as httpd:
        print(f"Aegis Pass API server is running on http://{HOST}:{PORT}")
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer is shutting down.")
