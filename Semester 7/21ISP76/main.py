'''import tkinter as tk
import subprocess
import sys
import os

# Get the current Python interpreter path
python_exec = sys.executable

def open_gui():
    subprocess.Popen([python_exec, os.path.join(os.getcwd(), "gui.py")])

def open_admin_gui():
    subprocess.Popen([python_exec, os.path.join(os.getcwd(), "admin_gui.py")])

def open_admin_interface():
    subprocess.Popen([python_exec, os.path.join(os.getcwd(), "admin_interface.py")])

def show_organization_options():
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Choose Organization Role", font=("Arial", 16))
    label.pack(pady=20)

    officer_btn = tk.Button(root, text="Officer", command=open_admin_gui, width=20, height=2, bg="#007acc", fg="white")
    officer_btn.pack(pady=10)

    admin_btn = tk.Button(root, text="Admin", command=open_admin_interface, width=20, height=2, bg="#007acc", fg="white")
    admin_btn.pack(pady=10)

    back_btn = tk.Button(root, text="← Back", command=show_main_options, width=10, bg="grey", fg="white")
    back_btn.pack(pady=20)

def show_main_options():
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Welcome to KYC Portal", font=("Arial", 18, "bold"))
    label.pack(pady=30)

    user_btn = tk.Button(root, text="User", command=open_gui, width=20, height=2, bg="#28a745", fg="white")
    user_btn.pack(pady=10)

    org_btn = tk.Button(root, text="Organization", command=show_organization_options, width=20, height=2, bg="#17a2b8", fg="white")
    org_btn.pack(pady=10)

# Setup main Tkinter window
root = tk.Tk()
root.title("KYC System Launcher")
root.geometry("400x350")
root.resizable(False, False)

show_main_options()

root.mainloop()'''

'''This is the working code'''
'''import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import os
import json
import sys

# Define blockchain path
BLOCKCHAIN_FILE = os.path.join(os.getcwd(), "blockchain_data.json")
python_exec = sys.executable

# Clear frame function
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Run any script with full path
def run_script(script_name):
    script_path = os.path.join(os.getcwd(), script_name)
    subprocess.Popen([python_exec, script_path])

# Check KYC Status using Aadhaar number
def check_kyc_status():
    aadhar = simpledialog.askstring("Check KYC Status", "Enter Aadhaar Number (xxxx-xxxx-xxxx):")
    if not aadhar:
        return

    try:
        with open(BLOCKCHAIN_FILE, "r") as file:
            blocks = json.load(file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read blockchain: {e}")
        return

    latest_status = None
    for block in reversed(blocks):  # Start from the latest
        if "header" in block and block["header"].get("aadhar_number") == aadhar:
            latest_status = block
            break

    if not latest_status:
        messagebox.showerror("Not Found", "No KYC request found for this Aadhaar number.")
        return

    status_msg = (
        f"Bank Verification: {latest_status.get('bank_verification_status', 'N/A')}\n"
        f"Aadhaar Verification: {latest_status.get('aadhar_verification_status', 'N/A')}\n"
        f"PAN Verification: {latest_status.get('pan_verification_status', 'N/A')}\n"
        f"RBI Verification: {latest_status.get('rbi_verification_status', 'N/A')}"
    )
    messagebox.showinfo("KYC Status", status_msg)

# User Option Page
def open_user_options():
    clear_frame()
    tk.Label(root, text="User Options", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="New KYC", command=lambda: run_script("gui.py"),
              width=20, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

    tk.Button(root, text="Check KYC Status", command=check_kyc_status,
              width=20, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=10)

    tk.Button(root, text="⬅ Back", command=main_menu,
              width=20, font=("Arial", 12), bg="gray", fg="white").pack(pady=10)

# Organization Option Page
def open_organization_options():
    clear_frame()
    tk.Label(root, text="Organization Options", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Admin", command=lambda: run_script("visualize_blockchain.py"),
              width=20, font=("Arial", 12), bg="#FF9800", fg="white").pack(pady=10)

    tk.Button(root, text="Officer", command=lambda: run_script("admin_gui.py"),
              width=20, font=("Arial", 12), bg="#9C27B0", fg="white").pack(pady=10)

    tk.Button(root, text="⬅ Back", command=main_menu,
              width=20, font=("Arial", 12), bg="gray", fg="white").pack(pady=10)

# Main Menu
def main_menu():
    clear_frame()
    tk.Label(root, text="Welcome to e-KYC Portal", font=("Arial", 18, "bold")).pack(pady=20)

    tk.Button(root, text="User", command=open_user_options,
              width=20, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

    tk.Button(root, text="Organization", command=open_organization_options,
              width=20, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=10)

# GUI setup
root = tk.Tk()
root.title("KYC Main Interface")
root.geometry("400x350")
main_menu()
root.mainloop()
'''


import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import os
import json
import sys
from cryptography.fernet import Fernet

# Define blockchain path and secret key path
BLOCKCHAIN_FILE = os.path.join(os.getcwd(), "blockchain_data.json")
SECRET_KEY_FILE = os.path.join(os.getcwd(), "secret.key")
python_exec = sys.executable

# Load secret key
def load_secret_key():
    try:
        with open(SECRET_KEY_FILE, "rb") as key_file:
            return key_file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load secret key: {e}")
        return None

# Clear frame function
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Run any script with full path
def run_script(script_name):
    script_path = os.path.join(os.getcwd(), script_name)
    subprocess.Popen([python_exec, script_path])

# Check KYC Status using Aadhaar number
def check_kyc_status():
    aadhar = simpledialog.askstring("Check KYC Status", "Enter Aadhaar Number (xxxx-xxxx-xxxx):")
    if not aadhar:
        return

    key = load_secret_key()
    if not key:
        return
    cipher = Fernet(key)

    try:
        with open(BLOCKCHAIN_FILE, "r") as file:
            blocks = json.load(file)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read blockchain: {e}")
        return

    latest_status = None
    for block in reversed(blocks):  # Start from the latest block
        if "header" in block:
            try:
                encrypted_aadhar = block["header"].get("aadhar_number", "")
                decrypted_aadhar = cipher.decrypt(encrypted_aadhar.encode()).decode()
                if decrypted_aadhar == aadhar:
                    latest_status = block
                    break
            except Exception as e:
                continue  # If decryption fails, skip this block

    if not latest_status:
        messagebox.showerror("Not Found", "No KYC request found for this Aadhaar number.")
        return

    status_msg = (
        f"Bank Verification: {latest_status.get('bank_verification_status', 'N/A')}\n"
        f"Aadhaar Verification: {latest_status.get('aadhar_verification_status', 'N/A')}\n"
        f"PAN Verification: {latest_status.get('pan_verification_status', 'N/A')}\n"
        f"RBI Verification: {latest_status.get('rbi_verification_status', 'N/A')}"
    )
    messagebox.showinfo("KYC Status", status_msg)

# User Option Page
def open_user_options():
    clear_frame()
    tk.Label(root, text="User Options", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="New KYC", command=lambda: run_script("gui.py"),
              width=20, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

    tk.Button(root, text="Check KYC Status", command=check_kyc_status,
              width=20, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=10)

    tk.Button(root, text="⬅ Back", command=main_menu,
              width=20, font=("Arial", 12), bg="gray", fg="white").pack(pady=10)

# Organization Option Page
def open_organization_options():
    clear_frame()
    tk.Label(root, text="Organization Options", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Admin", command=lambda: run_script("visualize_blockchain.py"),
              width=20, font=("Arial", 12), bg="#FF9800", fg="white").pack(pady=10)

    tk.Button(root, text="Officer", command=lambda: run_script("admin_gui.py"),
              width=20, font=("Arial", 12), bg="#9C27B0", fg="white").pack(pady=10)

    tk.Button(root, text="⬅ Back", command=main_menu,
              width=20, font=("Arial", 12), bg="gray", fg="white").pack(pady=10)

# Main Menu
def main_menu():
    clear_frame()
    tk.Label(root, text="Welcome to e-KYC Portal", font=("Arial", 18, "bold")).pack(pady=20)

    tk.Button(root, text="User", command=open_user_options,
              width=20, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

    tk.Button(root, text="Organization", command=open_organization_options,
              width=20, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=10)

# GUI setup
root = tk.Tk()
root.title("KYC Main Interface")
root.geometry("400x350")
main_menu()
root.mainloop()

