import json
from wsgiref.simple_server import make_server
import sys
import os
import mimetypes

# --- Add the 'logic' directory to the Python path ---
sys.path.append(os.path.join(os.path.dirname(__file__), 'logic'))

# --- Import the core logic functions ---
from password_logic import (
    generate_random_password,
    generate_memorable_password,
    calculate_strength
)

# --- Define the base path for the frontend files ---
# This version is more robust for finding the frontend directory.
# It gets the absolute path of the directory containing this script (backend/)
backend_dir = os.path.dirname(os.path.abspath(__file__))
# It then gets the parent directory of 'backend/' (the project root)
project_root = os.path.dirname(backend_dir)
# Finally, it constructs the full path to the 'frontend' directory.
FRONTEND_BASE_PATH = os.path.join(project_root, 'frontend')


def serve_static_file(path):
    """Serves a static file from the frontend directory."""
    # The path from the browser already includes 'static/', so we join it directly.
    file_path = os.path.join(FRONTEND_BASE_PATH, path.lstrip('/'))
    
    # Security: Ensure the path is within the intended frontend directory
    if not os.path.realpath(file_path).startswith(os.path.realpath(FRONTEND_BASE_PATH)):
        return '403 Forbidden', [], b'Forbidden'

    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        mime_type, _ = mimetypes.guess_type(file_path)
        headers = [('Content-type', mime_type or 'application/octet-stream')]
        return '200 OK', headers, content
    except FileNotFoundError:
        # If a file isn't found, return a clear text error.
        return '404 Not Found', [('Content-type', 'text/plain')], f"File Not Found: {file_path}".encode()
    except IOError:
        return '500 Internal Server Error', [], b'Internal Server Error'

def serve_template(template_name):
    """Serves an HTML template from the frontend/templates directory."""
    # This specifically looks inside the 'templates' subfolder for the html file.
    return serve_static_file(os.path.join('templates', template_name))

def handle_api_request(environ):
    """Handles the /generate API endpoint."""
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        data = json.loads(request_body)

        gen_type = data.get('type', 'random')
        count = min(int(data.get('count', 1)), 10)
        passwords, strength_info = [], {}

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
            else:
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
        return '200 OK', [('Content-type', 'application/json')], response_data.encode('utf-8')

    except Exception as e:
        error_response = json.dumps({'error': str(e)})
        return '400 Bad Request', [('Content-type', 'application/json')], error_response.encode('utf-8')

# --- Main WSGI Application ---
def application(environ, start_response):
    """The main WSGI application to handle all HTTP requests."""
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    cors_headers = [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'POST, GET, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type')
    ]

    if method == 'OPTIONS':
        start_response('200 OK', cors_headers)
        return []

    if path == '/':
        status, headers, response = serve_template('index.html')
    elif path.startswith('/static/'):
        status, headers, response = serve_static_file(path)
    elif path == '/generate' and method == 'POST':
        status, api_headers, response = handle_api_request(environ)
        headers = api_headers + cors_headers
    else:
        # Return a JSON error for any other path, as you observed.
        status = '404 Not Found'
        headers = [('Content-type', 'application/json')] + cors_headers
        response = json.dumps({'error': 'Not Found'}).encode('utf-8')

    start_response(status, headers)
    return [response]

# --- Main execution block ---
if __name__ == '__main__':
    HOST, PORT = 'localhost', 8080
    with make_server(HOST, PORT, application) as httpd:
        print(f"Aegis Pass server is running on http://{HOST}:{PORT}")
        print("You can now access the application at this address in your browser.")
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer is shutting down.")