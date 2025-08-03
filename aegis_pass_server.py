import json
import string
import secrets
from wsgiref.simple_server import make_server
import math
import os

# --- Built-in Wordlist for Memorable Passwords ---
# Sourced from a common, effective wordlist for generating passphrases.
# In a real-world, larger application, this might be loaded from a file.
EASY_WORDS = [
    "acid", "acorn", "acre", "acts", "afar", "affix", "aged", "agent",
    "agile", "aging", "agony", "ahead", "aide", "aids", "aim", "air",
    "aisle", "ajar", "alarm", "album", "ale", "alert", "alga", "alia",
    "alias", "alibi", "alien", "align", "alike", "alive", "alkali",
    "all", "alley", "alloy", "ally", "aloe", "aloft", "aloha", "alone",
    "amaze", "amber", "ambit", "amble", "ambush", "amend", "amid",
    "amide", "amino", "ample", "amply", "amuck", "amuse", "anew",
    "ankle", "annex", "annoy", "annul", "anthem", "any", "anyhow",
    "anyway", "apart", "apathy", "apex", "aphid", "aplomb", "appeal",
    "apple", "apply", "apron", "apt", "aptly", "arbor", "arc", "arcane",
    "arch", "area", "arena", "argon", "argue", "arise", "ark", "arm",
    "armful", "armpit", "army", "aroma", "array", "arrow", "arson",
    "art", "ascot", "ashen", "ash", "aside", "ask", "askew", "asleep",
    "aspect", "assay", "asset", "atlas", "atom", "atomic", "attic",
    "audio", "audit", "auger", "aunt", "aura", "auto", "autumn", "avail",
    "avert", "avian", "avoid", "await", "awake", "award", "aware",
    "awash", "away", "awful", "awoke", "axial", "axiom", "axis", "axle",
    "bacon", "badge", "badly", "bag", "baggy", "bail", "bait", "bake",
    "baker", "balance", "bald", "ball", "ballet", "ballot", "balm",
    "balsa", "bamboo", "band", "banjo", "bank", "bar", "barb", "bard",
    "barely", "barge", "bark", "barley", "barn", "baron", "barrel",
    "base", "basic", "basil", "basin", "basis", "basket", "bass",
    "bat", "batch", "bath", "baton", "battle", "bay", "beach", "bead",
    "beak", "beam", "bean", "bear", "beard", "beast", "beat", "beauty",
    "beaver", "beckon", "bed", "bee", "beech", "beef", "beep", "beer",
    "beet", "befit", "beg", "began", "beget", "begin", "begun", "beige",
    "being", "belch", "bell", "belly", "below", "belt", "bench", "bend",
    "best", "bet", "beta", "bevel", "bevy", "bias", "bible", "bicep",
    "bidet", "big", "bike", "bile", "bilge", "bill", "billion", "bin",
    "bind", "bingo", "biped", "birch", "bird", "birth", "bison", "bit",
    "bitch", "bite", "black", "blade", "blame", "bland", "blast",
    "blaze", "bleak", "bleat", "bleed", "bleep", "blend", "bless",
    "blimp", "blink", "blip", "bliss", "blitz", "bloat", "blob", "block",
    "blond", "blood", "bloom", "blow", "blue", "bluff", "blunt", "blur",
    "blurt", "blush", "boar", "board", "boast", "boat", "body", "bog",
    "bogus", "boil", "bold", "bolt", "bomb", "bond", "bone", "bonnet",
    "bonus", "bony", "book", "boom", "boost", "boot", "booth", "booze",
    "bop", "borax", "bore", "born", "boron", "boss", "botch", "both",
    "bottle", "bottom", "bough", "bouncy", "bound", "bow", "bowl",
    "box", "boy", "bra", "brace", "brad", "brag", "braid", "brain",
    "brake", "bran", "brand", "brash", "brass", "brat", "brave", "brawl",
    "brawn", "bread", "break", "breed", "breeze", "bribe", "brick",
    "bride", "brief", "brig", "brim", "brine", "bring", "brink", "brisk",
    "broad", "broil", "broke", "bronze", "brood", "brook", "broom",
    "broth", "brown", "browse", "brunt", "brush", "brute", "bubble",
    "buck", "bucket", "buckle", "buddy", "budge", "budget", "buff",
    "bug", "buggy", "build", "bulb", "bulge", "bulk", "bulky", "bull",
    "bully", "bump", "bumpy", "bunch", "bungee", "bunk", "bunny",
    "bunt", "buoy", "burly", "burn", "burp", "burrow", "bursar", "burst",
    "bus", "bush", "bust", "busy", "but", "butane", "butch", "butt",
    "buy", "buyer", "buzz", "bye", "bygone", "bylaw", "bypass", "byte"
]


# --- Frontend HTML, CSS (Tailwind), and JavaScript ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aegis Pass - Advanced Password Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; appearance: none; width: 20px; height: 20px; background: #3b82f6; cursor: pointer; border-radius: 50%; margin-top: -6px; }
        input[type=range]::-moz-range-thumb { width: 20px; height: 20px; background: #3b82f6; cursor: pointer; border-radius: 50%; }
        .tab-active { background-color: #3b82f6; color: white; }
        .tab-inactive { background-color: #374151; color: #d1d5db; }
    </style>
</head>
<body class="bg-gray-900 text-gray-200 flex items-center justify-center min-h-screen p-4">

    <div class="w-full max-w-2xl mx-auto">
        <header class="text-center mb-6">
            <h1 class="text-4xl sm:text-5xl font-bold text-white">Aegis Pass</h1>
            <p class="text-gray-400 mt-2">Your personal shield for secure passwords.</p>
        </header>

        <main>
            <!-- Results Display Area -->
            <div id="results-container" class="bg-gray-800 p-4 rounded-lg mb-6 shadow-lg space-y-3">
                <!-- Placeholder for generated passwords -->
            </div>

            <!-- Generator Controls -->
            <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
                <!-- Tabs -->
                <div class="flex border-b border-gray-700 mb-6">
                    <button id="tab-random" class="tab-active flex-1 py-2 px-4 rounded-t-lg font-semibold transition-colors focus:outline-none">Random</button>
                    <button id="tab-memorable" class="tab-inactive flex-1 py-2 px-4 rounded-t-lg font-semibold transition-colors focus:outline-none">Memorable</button>
                </div>

                <!-- Random Password Form -->
                <form id="random-form">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-5">
                        <!-- Left Column -->
                        <div>
                            <div class="mb-5">
                                <div class="flex justify-between items-center mb-2">
                                    <label for="length" class="font-medium text-white">Password Length</label>
                                    <span id="length-value" class="text-blue-400 font-semibold text-lg">16</span>
                                </div>
                                <input type="range" id="length" min="8" max="128" value="16" class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer">
                            </div>
                            <div class="mb-5">
                                <div class="flex justify-between items-center mb-2">
                                    <label for="count" class="font-medium text-white">Password Count</label>
                                    <span id="count-value" class="text-blue-400 font-semibold text-lg">1</span>
                                </div>
                                <input type="range" id="count" min="1" max="10" value="1" class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer">
                            </div>
                        </div>
                        <!-- Right Column -->
                        <div>
                            <div class="space-y-3">
                                <div class="flex items-center"><input id="uppercase" type="checkbox" checked class="w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"><label for="uppercase" class="ml-3 text-sm font-medium text-gray-300">Uppercase (A-Z)</label></div>
                                <div class="flex items-center"><input id="lowercase" type="checkbox" checked class="w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"><label for="lowercase" class="ml-3 text-sm font-medium text-gray-300">Lowercase (a-z)</label></div>
                                <div class="flex items-center"><input id="numbers" type="checkbox" checked class="w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"><label for="numbers" class="ml-3 text-sm font-medium text-gray-300">Numbers (0-9)</label></div>
                                <div class="flex items-center"><input id="special" type="checkbox" checked class="w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"><label for="special" class="ml-3 text-sm font-medium text-gray-300">Special Chars (!@#)</label></div>
                                <div class="flex items-center"><input id="exclude-similar" type="checkbox" class="w-5 h-5 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"><label for="exclude-similar" class="ml-3 text-sm font-medium text-gray-300">Exclude Similar (i,l,1,O,0)</label></div>
                            </div>
                        </div>
                    </div>
                </form>

                <!-- Memorable Password Form -->
                <form id="memorable-form" class="hidden">
                     <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-5">
                        <!-- Left Column -->
                        <div>
                            <div class="mb-5">
                                <div class="flex justify-between items-center mb-2">
                                    <label for="word-count" class="font-medium text-white">Number of Words</label>
                                    <span id="word-count-value" class="text-blue-400 font-semibold text-lg">4</span>
                                </div>
                                <input type="range" id="word-count" min="3" max="10" value="4" class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer">
                            </div>
                             <div class="mb-5">
                                <div class="flex justify-between items-center mb-2">
                                    <label for="memorable-count" class="font-medium text-white">Password Count</label>
                                    <span id="memorable-count-value" class="text-blue-400 font-semibold text-lg">1</span>
                                </div>
                                <input type="range" id="memorable-count" min="1" max="10" value="1" class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer">
                            </div>
                        </div>
                        <!-- Right Column -->
                        <div>
                            <label for="separator" class="block mb-2 text-sm font-medium text-white">Separator</label>
                            <select id="separator" class="bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5">
                                <option value="-">Hyphen (-)</option>
                                <option value=" ">Space ( )</option>
                                <option value=".">Period (.)</option>
                                <option value="_">Underscore (_)</option>
                                <option value=",">Comma (,)</option>
                            </select>
                        </div>
                    </div>
                </form>

                <!-- Generate Button & Message Area -->
                <div class="mt-8">
                    <button id="generate-button" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition-colors shadow-md focus:outline-none focus:ring-4 focus:ring-blue-800">
                        Generate Password
                    </button>
                    <div id="message-area" class="text-center mt-4 h-5 text-sm text-green-400"></div>
                </div>
            </div>
        </main>
    </div>

    <script>
        // --- DOM Element References ---
        const resultsContainer = document.getElementById('results-container');
        const messageArea = document.getElementById('message-area');
        const generateButton = document.getElementById('generate-button');

        // Tabs
        const tabRandom = document.getElementById('tab-random');
        const tabMemorable = document.getElementById('tab-memorable');
        
        // Forms
        const randomForm = document.getElementById('random-form');
        const memorableForm = document.getElementById('memorable-form');

        // Random Form Controls
        const lengthSlider = document.getElementById('length');
        const lengthValue = document.getElementById('length-value');
        const countSlider = document.getElementById('count');
        const countValue = document.getElementById('count-value');
        const randomOptions = {
            uppercase: document.getElementById('uppercase'),
            lowercase: document.getElementById('lowercase'),
            numbers: document.getElementById('numbers'),
            special: document.getElementById('special'),
            excludeSimilar: document.getElementById('exclude-similar')
        };
        
        // Memorable Form Controls
        const wordCountSlider = document.getElementById('word-count');
        const wordCountValue = document.getElementById('word-count-value');
        const memorableCountSlider = document.getElementById('memorable-count');
        const memorableCountValue = document.getElementById('memorable-count-value');
        const separatorSelect = document.getElementById('separator');

        let currentTab = 'random';

        // --- Event Listeners ---
        
        // Tab switching
        tabRandom.addEventListener('click', () => switchTab('random'));
        tabMemorable.addEventListener('click', () => switchTab('memorable'));

        // Slider value updates
        lengthSlider.addEventListener('input', (e) => lengthValue.textContent = e.target.value);
        countSlider.addEventListener('input', (e) => countValue.textContent = e.target.value);
        wordCountSlider.addEventListener('input', (e) => wordCountValue.textContent = e.target.value);
        memorableCountSlider.addEventListener('input', (e) => memorableCountValue.textContent = e.target.value);
        
        // Generate button click
        generateButton.addEventListener('click', handleGeneration);

        // --- Functions ---
        
        function switchTab(tabName) {
            currentTab = tabName;
            if (tabName === 'random') {
                tabRandom.className = 'tab-active flex-1 py-2 px-4 rounded-t-lg font-semibold transition-colors focus:outline-none';
                tabMemorable.className = 'tab-inactive flex-1 py-2 px-4 rounded-t-lg font-semibold transition-colors focus:outline-none';
                randomForm.classList.remove('hidden');
                memorableForm.classList.add('hidden');
            } else {
                tabRandom.className = 'tab-inactive flex-1 py-2 px-4 rounded-t-lg font-semibold transition-colors focus:outline-none';
                tabMemorable.className = 'tab-active flex-1 py-2 px-4 rounded-t-lg font-semibold transition-colors focus:outline-none';
                randomForm.classList.add('hidden');
                memorableForm.classList.remove('hidden');
            }
            handleGeneration();
        }

        async function handleGeneration() {
            let payload;
            if (currentTab === 'random') {
                const useUppercase = randomOptions.uppercase.checked;
                const useLowercase = randomOptions.lowercase.checked;
                const useNumbers = randomOptions.numbers.checked;
                const useSpecial = randomOptions.special.checked;

                if (!useUppercase && !useLowercase && !useNumbers && !useSpecial) {
                    showMessage('Error: Select at least one character type.', 'error');
                    return;
                }
                
                payload = {
                    type: 'random',
                    length: parseInt(lengthSlider.value, 10),
                    count: parseInt(countSlider.value, 10),
                    use_uppercase: useUppercase,
                    use_lowercase: useLowercase,
                    use_numbers: useNumbers,
                    use_special: useSpecial,
                    exclude_similar: randomOptions.excludeSimilar.checked
                };
            } else {
                payload = {
                    type: 'memorable',
                    word_count: parseInt(wordCountSlider.value, 10),
                    count: parseInt(memorableCountSlider.value, 10),
                    separator: separatorSelect.value
                };
            }

            // Show loading state
            resultsContainer.innerHTML = '<div class="text-center text-gray-400">Generating...</div>';
            messageArea.textContent = '';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) throw new Error(`Server error: ${response.statusText}`);

                const data = await response.json();
                if (data.error) throw new Error(data.error);
                
                displayResults(data.passwords, data.strength);

            } catch (error) {
                console.error('Error generating password:', error);
                resultsContainer.innerHTML = `<div class="text-center text-red-400">Error: ${error.message}</div>`;
            }
        }

        function displayResults(passwords, strengthInfo) {
            resultsContainer.innerHTML = '';
            passwords.forEach(password => {
                const passwordDiv = document.createElement('div');
                passwordDiv.className = 'bg-gray-700 p-3 rounded-md flex items-center justify-between';

                let strengthHtml = '';
                if (strengthInfo && strengthInfo[password]) {
                    const { text, color, width } = strengthInfo[password];
                    strengthHtml = `
                        <div class="w-1/4 ml-4">
                            <div class="w-full bg-gray-600 rounded-full h-2.5">
                                <div class="${color} h-2.5 rounded-full" style="width: ${width}"></div>
                            </div>
                            <p class="text-xs text-center mt-1" style="color:${color.replace('bg-','text-')}">${text}</p>
                        </div>
                    `;
                }

                passwordDiv.innerHTML = `
                    <span class="text-md font-mono break-all text-gray-300">${password}</span>
                    <div class="flex items-center">
                        ${strengthHtml}
                        <button title="Copy to clipboard" class="copy-btn p-2 ml-4 rounded-md hover:bg-gray-600 active:bg-gray-500 transition-colors" data-password="${password}">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                        </button>
                    </div>
                `;
                resultsContainer.appendChild(passwordDiv);
            });
            
            // Add event listeners to new copy buttons
            document.querySelectorAll('.copy-btn').forEach(button => {
                button.addEventListener('click', (e) => {
                    const passwordToCopy = e.currentTarget.dataset.password;
                    navigator.clipboard.writeText(passwordToCopy).then(() => {
                        showMessage('Password copied to clipboard!', 'success');
                    }).catch(err => {
                        console.error('Failed to copy:', err);
                        showMessage('Failed to copy password.', 'error');
                    });
                });
            });
        }
        
        function showMessage(message, type = 'success') {
            messageArea.textContent = message;
            messageArea.className = `text-center mt-4 h-5 text-sm ${type === 'success' ? 'text-green-400' : 'text-red-400'}`;
            setTimeout(() => { messageArea.textContent = ''; }, 3000);
        }
        
        // Initial Password Generation on Load
        document.addEventListener('DOMContentLoaded', handleGeneration);
    </script>
</body>
</html>
"""

# --- Backend Logic ---

def calculate_strength(password, char_pool_size):
    """Calculates password strength based on entropy."""
    if not password:
        return {"text": "N/A", "color": "bg-gray-500", "width": "0%"}
    
    entropy = len(password) * math.log2(char_pool_size)
    
    if entropy < 40:
        text, color, width = "Very Weak", "bg-red-500", "20%"
    elif entropy < 60:
        text, color, width = "Weak", "bg-orange-500", "40%"
    elif entropy < 80:
        text, color, width = "Medium", "bg-yellow-500", "60%"
    elif entropy < 100:
        text, color, width = "Strong", "bg-blue-500", "80%"
    else:
        text, color, width = "Very Strong", "bg-green-500", "100%"
        
    return {"text": text, "color": color, "width": width}

def generate_random_password(length, use_uppercase, use_lowercase, use_numbers, use_special, exclude_similar):
    """Generates a cryptographically strong random password."""
    char_pool_str = ""
    if use_uppercase: char_pool_str += string.ascii_uppercase
    if use_lowercase: char_pool_str += string.ascii_lowercase
    if use_numbers: char_pool_str += string.digits
    if use_special: char_pool_str += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    if exclude_similar:
        char_pool_str = "".join(c for c in char_pool_str if c not in "il1LoO")

    if not char_pool_str:
        return "", 0

    password = "".join(secrets.choice(char_pool_str) for _ in range(length))
    return password, len(char_pool_str)

def generate_memorable_password(word_count, separator):
    """Generates a memorable passphrase from a wordlist."""
    words = [secrets.choice(EASY_WORDS) for _ in range(word_count)]
    password = separator.join(words)
    # For memorable passwords, the pool size is the number of words in the list.
    return password, len(EASY_WORDS)


# --- WSGI Application ---

def application(environ, start_response):
    """The main WSGI application to handle HTTP requests."""
    path = environ.get('PATH_INFO', '/')

    if path == '/':
        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [HTML_CONTENT.encode('utf-8')]

    elif path == '/generate' and environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size)
            data = json.loads(request_body)

            gen_type = data.get('type', 'random')
            count = min(int(data.get('count', 1)), 10) # Cap at 10
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
            headers = [('Content-type', 'application/json')]
            start_response(status, headers)
            return [response_data.encode('utf-8')]

        except Exception as e:
            status = '400 Bad Request'
            headers = [('Content-type', 'application/json')]
            start_response(status, headers)
            error_response = json.dumps({'error': str(e)})
            return [error_response.encode('utf-8')]

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
