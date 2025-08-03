// --- CONSTANTS ---
const API_URL = 'http://localhost:8080/generate';

// SVG icons for copy button feedback
const COPY_ICON_SVG = `<rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>`;
const CHECK_ICON_SVG = `<polyline points="20 6 9 17 4 12"></polyline>`;

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

// Modal elements
const helpButton = document.getElementById('help-button');
const helpModal = document.getElementById('help-modal');
const modalOverlay = document.getElementById('modal-overlay');
const modalContent = document.getElementById('modal-content');
const modalCloseButton = document.getElementById('modal-close-button');

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

// --- FUNCTIONS ---

function openModal() {
    helpModal.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
    requestAnimationFrame(() => {
        modalOverlay.classList.remove('opacity-0');
        modalOverlay.classList.add('opacity-100');
        modalContent.classList.remove('scale-95');
        modalContent.classList.add('scale-100');
    });
}

function closeModal() {
    modalOverlay.classList.remove('opacity-100');
    modalOverlay.classList.add('opacity-0');
    modalContent.classList.remove('scale-100');
    modalContent.classList.add('scale-95');
    setTimeout(() => {
        helpModal.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
    }, 300);
}

function switchTab(tabName) {
    currentTab = tabName;
    const isRandom = tabName === 'random';

    tabRandom.className = isRandom ? 'tab-active' : 'tab-inactive';
    tabMemorable.className = !isRandom ? 'tab-active' : 'tab-inactive';
    
    document.querySelectorAll('.tab-active, .tab-inactive').forEach(el => {
        el.classList.add('flex-1', 'py-2.5', 'px-4', 'rounded-t-lg', 'font-semibold', 'transition-colors', 'focus:outline-none', 'focus:ring-2', 'focus:ring-blue-500', 'focus:ring-opacity-50');
    });

    randomForm.classList.toggle('hidden', !isRandom);
    memorableForm.classList.toggle('hidden', isRandom);

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

    resultsContainer.innerHTML = '<div class="text-center text-gray-400 p-5">Generating...</div>';
    messageArea.textContent = '';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ error: `Server responded with status: ${response.status}` }));
            throw new Error(errorData.error || `Server error`);
        }

        const data = await response.json();
        if (data.error) throw new Error(data.error);

        displayResults(data.passwords, data.strength);

    } catch (error) {
        console.error('Error generating password:', error);
        resultsContainer.innerHTML = `<div class="text-center text-red-400 p-5">Error: Could not connect to the API server. Is it running?</div>`;
    }
}

function displayResults(passwords, strengthInfo) {
    resultsContainer.innerHTML = '';
    if (!passwords || passwords.length === 0) {
        resultsContainer.innerHTML = '<div class="text-center text-gray-400 p-5">No passwords generated.</div>';
        return;
    }
    passwords.forEach(password => {
        const passwordDiv = document.createElement('div');
        passwordDiv.className = 'bg-gray-700/50 p-3 rounded-md flex items-center justify-between';

        let strengthHtml = '';
        if (strengthInfo && strengthInfo[password]) {
            const { text, color, width } = strengthInfo[password];
            const textColorClass = color.replace('bg-', 'text-');
            strengthHtml = `
                <div class="w-1/4 ml-4">
                    <div class="w-full bg-gray-600 rounded-full h-2">
                        <div class="${color} h-2 rounded-full" style="width: ${width}"></div>
                    </div>
                    <p class="text-xs ${textColorClass} text-center mt-1.5">${text}</p>
                </div>
            `;
        }

        passwordDiv.innerHTML = `
            <span class="text-md font-mono break-all text-gray-300 flex-1">${password}</span>
            <div class="flex items-center">
                ${strengthHtml}
                <button title="Copy to clipboard" class="copy-btn p-2 ml-4 rounded-md text-gray-400 hover:bg-gray-600 hover:text-white active:bg-gray-500 transition-colors" data-password="${password}">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${COPY_ICON_SVG}</svg>
                </button>
            </div>
        `;
        resultsContainer.appendChild(passwordDiv);
    });

    // Add event listeners to the newly created copy buttons
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const thisButton = e.currentTarget;
            const passwordToCopy = thisButton.dataset.password;
            const icon = thisButton.querySelector('svg');

            navigator.clipboard.writeText(passwordToCopy).then(() => {
                showMessage('Password copied to clipboard!', 'success');
                // Change icon to checkmark
                icon.innerHTML = CHECK_ICON_SVG;
                // Revert icon back after 2 seconds
                setTimeout(() => {
                    icon.innerHTML = COPY_ICON_SVG;
                }, 2000);
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

// --- INITIALIZATION ---
// Add all event listeners when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
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

    // Modal listeners
    helpButton.addEventListener('click', openModal);
    modalCloseButton.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', closeModal);
    
    // Generate a password when the page first loads
    handleGeneration();
});
