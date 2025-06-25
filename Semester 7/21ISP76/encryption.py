import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"
USER_FOLDER = "users"  # Main directory to store user data

# Ensure users folder exists
if not os.path.exists(USER_FOLDER):
    os.makedirs(USER_FOLDER)

def generate_key():
    """Generate and save an encryption key if not already generated."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    """Load the encryption key from file."""
    generate_key()  # Ensure key exists before loading
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read().strip()

# Load the encryption key properly
KEY = load_key()
cipher = Fernet(KEY)

def encrypt_file(file_path, aadhar_number):
    """Encrypts a file and stores it in a folder named after the Aadhaar number."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Create a user-specific folder inside "users/"
    user_folder = os.path.join(USER_FOLDER, aadhar_number)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    with open(file_path, "rb") as file:
        encrypted_data = cipher.encrypt(file.read())

    # Generate new encrypted file path inside user's folder
    filename = os.path.basename(file_path) + ".enc"
    encrypted_path = os.path.join(user_folder, filename)

    with open(encrypted_path, "wb") as file:
        file.write(encrypted_data)

    print(f"[INFO] Encryption successful: {encrypted_path}")
    return encrypted_path  # Return new encrypted file path

def decrypt_file(encrypted_file_path):
    """Decrypts an encrypted file and saves the original content."""
    if not os.path.exists(encrypted_file_path):
        print(f"[ERROR] Encrypted file '{encrypted_file_path}' not found!")
        return None

    try:
        with open(encrypted_file_path, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = cipher.decrypt(encrypted_data)

        # Ensure the correct file extension is used
        decrypted_file_path = encrypted_file_path.replace(".enc", "")

        with open(decrypted_file_path, "wb") as file:
            file.write(decrypted_data)

        print(f"[INFO] Decryption successful: {decrypted_file_path}")
        return decrypted_file_path  # Return the correct path

    except Exception as e:
        print(f"[ERROR] Decryption failed: {e}")
        return None

def decrypt_text(encrypted_string):
    """Decrypts an encrypted string (e.g., user detail field)."""
    if not isinstance(encrypted_string, str):
        raise ValueError("Encrypted token must be a string.")

    try:
        decrypted = cipher.decrypt(encrypted_string.encode()).decode()
        return decrypted
    except Exception as e:
        print(f"[ERROR] Decryption error: {e}")
        return ""
