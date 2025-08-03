import json
import string
import secrets
from wsgiref.simple_server import make_server
import cgi

# --- Frontend HTML, CSS (Tailwind), and JavaScript ---
# This entire web interface is stored in a single string and served by our Python backend.
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aegis Pass - Secure Password Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        /* Custom styles for slider */
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            background: #3b82f6; /* blue-500 */
            cursor: pointer;
            border-radius: 50%;
            margin-top: -6px;
        }
        input[type=range]::-moz-range-thumb {
            width: 20px;
            height: 20px;
            background: #3b82f6;
            cursor: pointer;
            border-radius: 50%;
        }
    </style>
</head>
<body class="bg-gray-900 text-gray-200 flex items-center justify-center min-h-screen">

    <div class="w-full max-w-md mx-auto p-4 sm:p-6">
        <header class="text-center mb-6">
            <h1 class="text-3xl sm:text-4xl font-bold text-white">Aegis Pass</h1>
            <p class="text-gray-400 mt-2">Your personal shield for secure passwords.</p>
        </header>

        <main>
            <!-- Password Display -->
            <div class="bg-gray-800 p-4 rounded-lg flex items-center justify-between mb-6 shadow-lg">
                <span id="password-display" class="text-lg font-mono break-all text-gray-300">P4ssw0rd!</span>
                <button id="copy-button" title="Copy to clipboard" class="p-2 rounded-md hover:bg-gray-700 active:bg-gray-600 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                </button>
            </div>

            <!-- Generator Controls -->
            <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
                <form id="password-form">
                    <!-- Length Slider -->
                    <div class="mb-5">
                        <div class="flex justify-between items-center mb-2">
                            <label for="length" class="font-medium text-white">Password Length</label>
                            <span id="length-value" class="text-blue-400 font-semibold text-lg">16</span>
                        </div>
                        <input type="range" id="length" min="8" max="128" value="16" class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer">
                    </div>

                    <!-- Character Options -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
                        <div class="flex items-center">
                            <input id="uppercase" type="checkbox" checked class="w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500 focus:ring-2">
                            <label for="uppercase" class="ml-3 text-sm font-medium text-gray-300">Include Uppercase (A-Z)</label>
                        </div>
                        <div class="flex items-center">
                            <input id="lowercase" type="checkbox" checked class="w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500 focus:ring-2">
                            <label for="lowercase" class="ml-3 text-sm font-medium text-gray-300">Include Lowercase (a-z)</label>
                        </div>
                        <div class="flex items-center">
                            <input id="numbers" type="checkbox" checked class="w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500 focus:ring-2">
                            <label for="numbers" class="ml-3 text-sm font-medium text-gray-300">Include Numbers (0-9)</label>
                        </div>
                        <div class="flex items-center">
                            <input id="special" type="checkbox" checked class="w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500 focus:ring-2">
                            <label for="special" class="ml-3 text-sm font-medium text-gray-300">Include Special (!@#$)</label>
                        </div>
                    </div>

                    <!-- Generate Button -->
                    <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition-colors shadow-md focus:outline-none focus:ring-4 focus:ring-blue-800">
                        Generate Password
                    </button>
                    
                    <!-- Message Area -->
                    <div id="message-area" class="text-center mt-4 h-5 text-sm text-green-400"></div>
                </form>
            </div>
        </main>
    </div>

    <script>
        // --- DOM Element References ---
        const passwordForm = document.getElementById('password-form');
        const passwordDisplay = document.getElementById('password-display');
        const lengthSlider = document.getElementById('length');
        const lengthValue = document.getElementById('length-value');
        const copyButton = document.getElementById('copy-button');
        const messageArea = document.getElementById('message-area');
        
        const options = {
            uppercase: document.getElementById('uppercase'),
            lowercase: document.getElementById('lowercase'),
            numbers: document.getElementById('numbers'),
            special: document.getElementById('special')
        };

        // --- Event Listeners ---
        
        // Update length display when slider moves
        lengthSlider.addEventListener('input', (e) => {
            lengthValue.textContent = e.target.value;
        });

        // Handle form submission to generate a new password
        passwordForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Prevent page reload
            
            const length = parseInt(lengthSlider.value, 10);
            const useUppercase = options.uppercase.checked;
            const useLowercase = options.lowercase.checked;
            const useNumbers = options.numbers.checked;
            const useSpecial = options.special.checked;

            if (!useUppercase && !useLowercase && !useNumbers && !useSpecial) {
                showMessage('Error: Select at least one character type.', 'error');
                return;
            }
            
            // Show loading state
            passwordDisplay.textContent = 'Generating...';
            messageArea.textContent = '';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        length,
                        use_uppercase: useUppercase,
                        use_lowercase: useLowercase,
                        use_numbers: useNumbers,
                        use_special: useSpecial
                    })
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                passwordDisplay.textContent = data.password;

            } catch (error) {
                console.error('Error generating password:', error);
                passwordDisplay.textContent = 'Error!';
                showMessage('Failed to contact server.', 'error');
            }
        });

        // Handle copy to clipboard
        copyButton.addEventListener('click', () => {
            const password = passwordDisplay.textContent;
            if (password && password !== 'Generating...' && password !== 'Error!') {
                navigator.clipboard.writeText(password).then(() => {
                    showMessage('Password copied to clipboard!', 'success');
                }).catch(err => {
                    console.error('Failed to copy:', err);
                    showMessage('Failed to copy password.', 'error');
                });
            }
        });

        // --- Utility Functions ---
        
        function showMessage(message, type = 'success') {
            messageArea.textContent = message;
            messageArea.className = `text-center mt-4 h-5 text-sm ${type === 'success' ? 'text-green-400' : 'text-red-400'}`;
            
            // Clear the message after 3 seconds
            setTimeout(() => {
                messageArea.textContent = '';
            }, 3000);
        }
        
        // --- Initial Password Generation on Load ---
        document.addEventListener('DOMContentLoaded', () => {
            passwordForm.dispatchEvent(new Event('submit'));
        });

    </script>
</body>
</html>
"""

# --- Backend Password Generation Logic ---

def generate_secure_password(length, use_uppercase, use_lowercase, use_numbers, use_special):
    """
    Generates a cryptographically strong random password.
    """
    char_pool = []
    password = []

    # Build the pool of available characters based on user selection
    if use_uppercase:
        char_pool.extend(string.ascii_uppercase)
        password.append(secrets.choice(string.ascii_uppercase))
    if use_lowercase:
        char_pool.extend(string.ascii_lowercase)
        password.append(secrets.choice(string.ascii_lowercase))
    if use_numbers:
        char_pool.extend(string.digits)
        password.append(secrets.choice(string.digits))
    if use_special:
        # A common set of special characters
        special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        char_pool.extend(special_chars)
        password.append(secrets.choice(special_chars))

    # If no character sets were selected, we can't generate a password.
    if not char_pool:
        return ""

    # Fill the rest of the password length with random characters from the pool
    remaining_length = length - len(password)
    for _ in range(remaining_length):
        password.append(secrets.choice(char_pool))

    # Shuffle the list to ensure random placement of the guaranteed characters
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


# --- WSGI Application ---

def application(environ, start_response):
    """
    The main WSGI application to handle HTTP requests.
    """
    path = environ.get('PATH_INFO', '/')

    # Route for the main HTML page
    if path == '/':
        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [HTML_CONTENT.encode('utf-8')]

    # Route for the password generation API endpoint
    elif path == '/generate' and environ['REQUEST_METHOD'] == 'POST':
        try:
            # Get the length of the request body
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            # Read the request body
            request_body = environ['wsgi.input'].read(request_body_size)
            data = json.loads(request_body)

            # Extract parameters from the JSON body
            length = int(data.get('length', 16))
            use_uppercase = bool(data.get('use_uppercase', True))
            use_lowercase = bool(data.get('use_lowercase', True))
            use_numbers = bool(data.get('use_numbers', True))
            use_special = bool(data.get('use_special', True))

            # Generate the password
            password = generate_secure_password(
                length, use_uppercase, use_lowercase, use_numbers, use_special
            )

            # Prepare the JSON response
            response_data = json.dumps({'password': password})
            status = '200 OK'
            headers = [('Content-type', 'application/json')]
            start_response(status, headers)
            return [response_data.encode('utf-8')]

        except (json.JSONDecodeError, ValueError) as e:
            # Handle bad requests
            status = '400 Bad Request'
            headers = [('Content-type', 'application/json')]
            start_response(status, headers)
            error_response = json.dumps({'error': 'Invalid request data', 'details': str(e)})
            return [error_response.encode('utf-8')]

    # Handle 404 Not Found for any other path
    else:
        status = '404 Not Found'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b'Not Found']

# --- Main execution block to run the server ---

if __name__ == '__main__':
    HOST, PORT = 'localhost', 8080
    with make_server(HOST, PORT, application) as httpd:
        print(f"Aegis Pass server is running on http://{HOST}:{PORT}")
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer is shutting down.")

