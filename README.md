# Aegis Pass - Secure Password Generator

Aegis Pass is a modern, web-based password generator designed to create strong, secure, and memorable passwords. It features a clean user interface and a robust Python backend, providing a seamless experience for generating passwords tailored to your security needs.

---

## Features

* **Two Generation Modes**:
    * **Random**: Creates cryptographically secure passwords with a mix of uppercase letters, lowercase letters, numbers, and special characters.
    * **Memorable**: Generates easy-to-remember passphrases based on the Diceware method (e.g., `word-word-word`).
* **Customizable Options**:
    * Adjust password length or the number of words.
    * Generate multiple passwords at once.
    * Optionally exclude visually similar characters (like `i`, `l`, `1`, `O`, `0`).
    * Choose from various separators for memorable passphrases.
* **Password Strength Meter**: A real-time visual indicator estimates the strength of the generated passwords, helping you make informed security choices.
* **Modern UI**: A clean, responsive, and intuitive user interface with a built-in help guide.
* **Copy to Clipboard**: Easily copy any generated password with a single click.

---

## How to Run

To run Aegis Pass, you need to start the backend server and then access the application in your web browser.

### Prerequisites

* Python 3.6+

### 1. Start the Backend Server

First, get the Python API server running.

1.  **Open a terminal** or command prompt.
2.  **Navigate to the `backend` directory** of the project.
    ```bash
    cd aegis-pass/backend
    ```
3.  **Run the server script**.
    ```bash
    python api_server.py
    ```
4.  The terminal will show a confirmation message. **Keep this terminal window open.**

### 2. Launch the Frontend

Now, access the user interface.

1.  **Open your web browser** (Chrome, Firefox, etc.).
2.  Go to the following address:
    ```
    http://localhost:8080
    ```

The application should now be fully functional in your browser.

---

## Technology Stack

* **Backend**:
    * **Python 3**: The core programming language.
    * **WSGI (`wsgiref`)**: A standard interface between the web server and the Python application, built into Python.
* **Frontend**:
    * **HTML5**: For the structure of the web page.
    * **CSS3**: For custom styling.
    * **Tailwind CSS**: A utility-first CSS framework for rapid UI development.
    * **JavaScript (ES6+)**: For all client-side interactivity and API communication.
