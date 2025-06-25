import tkinter as tk
from tkinter import messagebox
from blockchain import verify_blockchain_integrity

class CheckIntegrityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Admin Panel")
        self.root.geometry("400x200")

        # Title label
        title_label = tk.Label(root, text="Blockchain Integrity Checker", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Verify Blockchain Button
        check_button = tk.Button(root, text="Verify Blockchain Integrity", command=self.check_integrity, bg="green", fg="white", font=("Arial", 12))
        check_button.pack(pady=10)

    def check_integrity(self):
        result = verify_blockchain_integrity()
        if result.startswith("[SUCCESS]"):
            messagebox.showinfo("Blockchain Integrity", result)
        else:
            messagebox.showerror("Blockchain Tampering Detected", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = CheckIntegrityApp(root)
    root.mainloop()


'''import tkinter as tk
from tkinter import messagebox
from blockchain import verify_blockchain_integrity

def check_integrity():
    result = verify_blockchain_integrity()
    if result.startswith("[SUCCESS]"):
        messagebox.showinfo("Blockchain Integrity", result)
    else:
        messagebox.showerror("Blockchain Tampering Detected", result)

# Tkinter GUI Setup
root = tk.Tk()
root.title("Blockchain Admin Panel")
root.geometry("400x200")

title_label = tk.Label(root, text="Blockchain Integrity Checker", font=("Arial", 16, "bold"))
title_label.pack(pady=20)

check_button = tk.Button(root, text="Verify Blockchain Integrity", command=check_integrity, bg="green", fg="white", font=("Arial", 12))
check_button.pack(pady=10)

root.mainloop()
'''

'''import tkinter as tk
from tkinter import messagebox
from blockchain import check_blockchain_integrity

def show_tampered_info(tampered_data):
    result_text.delete("1.0", tk.END)

    if not tampered_data:
        result_text.insert(tk.END, "✅ Blockchain is intact. No tampering detected.\n")
        return

    result_text.insert(tk.END, "⚠️ Tampering Detected!\n\n")
    for entry in tampered_data:
        user_id = entry.get("user_id", "Unknown")
        aadhar = entry.get("aadhar_number", "Unknown")
        fields = entry.get("tampered_fields", [])
        result_text.insert(tk.END, f"User ID: {user_id} | Aadhaar: {aadhar}\n")
        result_text.insert(tk.END, f"Tampered Fields: {', '.join(fields)}\n\n")

def check_integrity():
    tampered_data = check_blockchain_integrity()
    show_tampered_info(tampered_data)

# GUI setup
root = tk.Tk()
root.title("Blockchain Integrity Checker")
root.geometry("600x400")
root.configure(bg="white")

title = tk.Label(root, text="Admin Panel: Check Blockchain Integrity", font=("Helvetica", 16, "bold"), bg="white")
title.pack(pady=20)

check_button = tk.Button(root, text="Check Integrity", command=check_integrity, font=("Helvetica", 12), bg="lightgray")
check_button.pack(pady=10)

result_text = tk.Text(root, height=15, width=70, font=("Courier", 10), bg="#f9f9f9")
result_text.pack(pady=10)

root.mainloop()'''

'''import tkinter as tk
from blockchain import check_blockchain_integrity

def check_integrity():
    tampered = check_blockchain_integrity()
    if not tampered:
        result_text.set("✅ Blockchain integrity is intact.")
    else:
        msg = "⚠️ Tampering Detected!\n\n"
        for block in tampered:
            msg += f"User ID: {block['user_id']} | Aadhaar: {block['aadhar_number']}\n"
            msg += f"Tampered Fields: {', '.join(block['tampered_fields'])}\n\n"
        result_text.set(msg)

# GUI setup
window = tk.Tk()
window.title("Blockchain Integrity Checker")
window.geometry("600x400")

tk.Label(window, text="Admin Panel: Check Blockchain Integrity", font=("Arial", 14, "bold")).pack(pady=20)

tk.Button(window, text="Check Integrity", font=("Arial", 12), command=check_integrity).pack(pady=10)

result_text = tk.StringVar()
tk.Label(window, textvariable=result_text, font=("Courier", 11), wraplength=550, justify="left").pack(pady=10)

window.mainloop()
'''
