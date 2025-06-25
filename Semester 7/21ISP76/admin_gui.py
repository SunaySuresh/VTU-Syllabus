'''import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from encryption import decrypt_file  # Import the decrypt function from your decryption file

USER_FOLDER = "users"

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel - KYC Verification")

        # Aadhaar Number Input
        tk.Label(root, text="Enter Aadhaar Number:").grid(row=0, column=0, padx=10, pady=10)
        self.aadhar_entry = tk.Entry(root)
        self.aadhar_entry.grid(row=0, column=1, padx=10, pady=10)

        # Load Button
        self.load_button = tk.Button(root, text="Load KYC Data", command=self.load_kyc_data)
        self.load_button.grid(row=0, column=2, padx=10, pady=10)

        # Image Display Labels
        self.aadhar_label = tk.Label(root, text="Aadhaar Image:")
        self.aadhar_label.grid(row=1, column=0, padx=10, pady=10)
        self.aadhar_canvas = tk.Label(root)
        self.aadhar_canvas.grid(row=1, column=1, padx=10, pady=10)

        self.pan_label = tk.Label(root, text="PAN Image:")
        self.pan_label.grid(row=2, column=0, padx=10, pady=10)
        self.pan_canvas = tk.Label(root)
        self.pan_canvas.grid(row=2, column=1, padx=10, pady=10)

        self.face_label = tk.Label(root, text="Captured Face:")
        self.face_label.grid(row=3, column=0, padx=10, pady=10)
        self.face_canvas = tk.Label(root)
        self.face_canvas.grid(row=3, column=1, padx=10, pady=10)

    def load_kyc_data(self):
        """Load and display the decrypted KYC images for the entered Aadhaar number."""
        aadhar_number = self.aadhar_entry.get().strip()
        if not aadhar_number:
            messagebox.showerror("Error", "Please enter a valid Aadhaar number.")
            return

        user_folder = os.path.join(USER_FOLDER, aadhar_number)
        if not os.path.exists(user_folder):
            messagebox.showerror("Error", f"No records found for Aadhaar: {aadhar_number}")
            return

        # File paths for encrypted images
        aadhar_enc = os.path.join(user_folder, "aadhar.jpeg.enc")
        pan_enc = os.path.join(user_folder, "pan.jpeg.enc")
        face_enc = None

        # Find the captured face file dynamically (since the name includes timestamp)
        for file in os.listdir(user_folder):
            if file.endswith("_captured_face.jpg.enc"):
                face_enc = os.path.join(user_folder, file)
                break

        # Attempt to decrypt and display images
        self.display_decrypted_image(aadhar_enc, self.aadhar_canvas)
        self.display_decrypted_image(pan_enc, self.pan_canvas)
        if face_enc:
            self.display_decrypted_image(face_enc, self.face_canvas)
        else:
            messagebox.showwarning("Warning", "Captured face image not found.")

    def display_decrypted_image(self, encrypted_path, image_label):
        """Decrypt the image and display it in the Tkinter window."""
        if os.path.exists(encrypted_path):
            decrypted_path = decrypt_file(encrypted_path)
            if decrypted_path and os.path.exists(decrypted_path):
                img = Image.open(decrypted_path)
                img = img.resize((200, 200))  # Resize for display
                img = ImageTk.PhotoImage(img)
                image_label.config(image=img)
                image_label.image = img  # Keep a reference to prevent garbage collection
            else:
                messagebox.showerror("Error", f"Failed to decrypt: {os.path.basename(encrypted_path)}")
        else:
            messagebox.showwarning("Warning", f"Encrypted file not found: {os.path.basename(encrypted_path)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()
'''

'''Try 2'''

'''import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from encryption import decrypt_file
from blockchain import add_block  # Import add_block for blockchain updates
from deepface import DeepFace

USER_FOLDER = "users"

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel - KYC Verification")
        self.root.geometry("800x600")

        # Scrollable Frame
        self.canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Aadhaar Number Input
        ttk.Label(self.scrollable_frame, text="Enter Aadhaar Number:").grid(row=0, column=0, padx=10, pady=10)
        self.aadhar_entry = ttk.Entry(self.scrollable_frame)
        self.aadhar_entry.grid(row=0, column=1, padx=10, pady=10)

        # Load Button
        self.load_button = ttk.Button(self.scrollable_frame, text="Load KYC Data", command=self.load_kyc_data)
        self.load_button.grid(row=0, column=2, padx=10, pady=10)

        # Image Labels & Placeholders
        self.aadhar_label = ttk.Label(self.scrollable_frame, text="Aadhaar Image:")
        self.aadhar_label.grid(row=1, column=0, padx=10, pady=10)
        self.aadhar_canvas = ttk.Label(self.scrollable_frame)
        self.aadhar_canvas.grid(row=1, column=1, padx=10, pady=10)
        self.aadhar_canvas.bind("<Button-1>", lambda e: self.enlarge_image(self.decrypted_aadhar))

        self.pan_label = ttk.Label(self.scrollable_frame, text="PAN Image:")
        self.pan_label.grid(row=2, column=0, padx=10, pady=10)
        self.pan_canvas = ttk.Label(self.scrollable_frame)
        self.pan_canvas.grid(row=2, column=1, padx=10, pady=10)
        self.pan_canvas.bind("<Button-1>", lambda e: self.enlarge_image(self.decrypted_pan))

        self.face_label = ttk.Label(self.scrollable_frame, text="Captured Face:")
        self.face_label.grid(row=3, column=0, padx=10, pady=10)
        self.face_canvas = ttk.Label(self.scrollable_frame)
        self.face_canvas.grid(row=3, column=1, padx=10, pady=10)
        self.face_canvas.bind("<Button-1>", lambda e: self.enlarge_image(self.decrypted_face))

        # Compare Button (Initially Hidden)
        self.compare_button = ttk.Button(self.scrollable_frame, text="Compare Faces", command=self.compare_faces)
        self.compare_button.grid(row=4, column=1, pady=10)
        self.compare_button.grid_remove()  # Hide initially

    def load_kyc_data(self):
        """Load and display the decrypted KYC images for the entered Aadhaar number."""
        aadhar_number = self.aadhar_entry.get().strip()
        if not aadhar_number:
            messagebox.showerror("Error", "Please enter a valid Aadhaar number.")
            return

        user_folder = os.path.join(USER_FOLDER, aadhar_number)
        if not os.path.exists(user_folder):
            messagebox.showerror("Error", f"No records found for Aadhaar: {aadhar_number}")
            return

        aadhar_enc = os.path.join(user_folder, "aadhar.jpeg.enc")
        pan_enc = os.path.join(user_folder, "pan.jpeg.enc")
        face_enc = None

        for file in os.listdir(user_folder):
            if file.endswith("_captured_face.jpg.enc"):
                face_enc = os.path.join(user_folder, file)
                break

        self.decrypted_aadhar = self.display_decrypted_image(aadhar_enc, self.aadhar_canvas)
        self.decrypted_pan = self.display_decrypted_image(pan_enc, self.pan_canvas)
        self.decrypted_face = self.display_decrypted_image(face_enc, self.face_canvas) if face_enc else None

        if self.decrypted_aadhar and self.decrypted_face:
            self.compare_button.grid()  # Show the compare button

    def display_decrypted_image(self, encrypted_path, image_label):
        """Decrypt and display the image."""
        if os.path.exists(encrypted_path):
            decrypted_path = decrypt_file(encrypted_path)
            if decrypted_path and os.path.exists(decrypted_path):
                img = Image.open(decrypted_path)
                img = img.resize((200, 200))
                img = ImageTk.PhotoImage(img)
                image_label.config(image=img)
                image_label.image = img
                return decrypted_path
            else:
                messagebox.showerror("Error", f"Failed to decrypt: {os.path.basename(encrypted_path)}")
        else:
            messagebox.showwarning("Warning", f"Encrypted file not found: {os.path.basename(encrypted_path)}")
        return None

    def compare_faces(self):
        """Compares the captured face with the Aadhaar image."""
        if not self.decrypted_aadhar or not self.decrypted_face:
            messagebox.showerror("Error", "Missing images for comparison.")
            return

        try:
            result = DeepFace.verify(self.decrypted_face, self.decrypted_aadhar, model_name="Facenet", enforce_detection=False)

            if result["verified"]:
                messagebox.showinfo("Success", "Face matched successfully!")
                self.update_blockchain(self.aadhar_entry.get().strip(), self.decrypted_face, "Face Matched")
            else:
                messagebox.showerror("Mismatch", "Face does not match the Aadhaar image!")

        except Exception as e:
            messagebox.showerror("Error", f"Face comparison failed: {e}")

    def update_blockchain(self, aadhar_number, captured_face_path, status):
        """Updates the blockchain with verification status."""
        try:
            user_id = aadhar_number  # Assuming user_id is same as Aadhaar
            encrypted_aadhar_path = os.path.join(USER_FOLDER, aadhar_number, "aadhar.jpeg.enc")
            encrypted_pan_path = os.path.join(USER_FOLDER, aadhar_number, "pan.jpeg.enc")

            add_block(user_id, aadhar_number, captured_face_path, status, encrypted_aadhar_path, encrypted_pan_path)
            messagebox.showinfo("Blockchain", "Status updated in blockchain!")
        except Exception as e:
            messagebox.showerror("Error", f"Blockchain update failed: {e}")

    def enlarge_image(self, image_path):
        """Displays an enlarged version of the image in a new window."""
        if not image_path:
            return

        top = tk.Toplevel(self.root)
        top.title("Enlarged Image")

        img = Image.open(image_path)
        img = img.resize((500, 500))  # Resize for larger view
        img = ImageTk.PhotoImage(img)

        lbl = tk.Label(top, image=img)
        lbl.image = img
        lbl.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()
'''

'''Try 3'''
'''This is perfect but images are not much viewable'''
'''
import os
import time
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from encryption import decrypt_file
from blockchain import add_block
from mock_apis import verify_aadhar, verify_pan, verify_rbi
from deepface import DeepFace

USER_FOLDER = "users"

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel - KYC Verification")
        self.root.geometry("800x600")

        # Scrollable Frame
        self.canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Aadhaar Number Input
        ttk.Label(self.scrollable_frame, text="Enter Aadhaar Number:").grid(row=0, column=0, padx=10, pady=10)
        self.aadhar_entry = ttk.Entry(self.scrollable_frame)
        self.aadhar_entry.grid(row=0, column=1, padx=10, pady=10)

        # Load Button
        self.load_button = ttk.Button(self.scrollable_frame, text="Load KYC Data", command=self.load_kyc_data)
        self.load_button.grid(row=0, column=2, padx=10, pady=10)

        # Image Labels & Placeholders
        self.aadhar_label = ttk.Label(self.scrollable_frame, text="Aadhaar Image:")
        self.aadhar_label.grid(row=1, column=0, padx=10, pady=10)
        self.aadhar_canvas = ttk.Label(self.scrollable_frame)
        self.aadhar_canvas.grid(row=1, column=1, padx=10, pady=10)

        self.pan_label = ttk.Label(self.scrollable_frame, text="PAN Image:")
        self.pan_label.grid(row=2, column=0, padx=10, pady=10)
        self.pan_canvas = ttk.Label(self.scrollable_frame)
        self.pan_canvas.grid(row=2, column=1, padx=10, pady=10)

        self.face_label = ttk.Label(self.scrollable_frame, text="Captured Face:")
        self.face_label.grid(row=3, column=0, padx=10, pady=10)
        self.face_canvas = ttk.Label(self.scrollable_frame)
        self.face_canvas.grid(row=3, column=1, padx=10, pady=10)

        # Compare & Verify Buttons
        self.compare_button = ttk.Button(self.scrollable_frame, text="Compare Faces", command=self.compare_faces)
        self.compare_button.grid(row=4, column=1, pady=10)
        self.compare_button.grid_remove()  # Initially hidden

        self.verify_button = ttk.Button(self.scrollable_frame, text="Run Full Verification", command=self.run_full_verification)
        self.verify_button.grid(row=5, column=1, pady=10)
        self.verify_button.grid_remove()  # Initially hidden

    def load_kyc_data(self):
        """Load and display decrypted KYC images for the entered Aadhaar number."""
        aadhar_number = self.aadhar_entry.get().strip()
        if not aadhar_number:
            messagebox.showerror("Error", "Please enter a valid Aadhaar number.")
            return

        user_folder = os.path.join(USER_FOLDER, aadhar_number)
        if not os.path.exists(user_folder):
            messagebox.showerror("Error", f"No records found for Aadhaar: {aadhar_number}")
            return

        aadhar_enc = os.path.join(user_folder, "aadhar.jpeg.enc")
        pan_enc = os.path.join(user_folder, "pan.jpeg.enc")
        face_enc = None

        for file in os.listdir(user_folder):
            if file.endswith("_captured_face.jpg.enc"):
                face_enc = os.path.join(user_folder, file)
                break

        self.decrypted_aadhar = self.display_decrypted_image(aadhar_enc, self.aadhar_canvas)
        self.decrypted_pan = self.display_decrypted_image(pan_enc, self.pan_canvas)
        self.decrypted_face = self.display_decrypted_image(face_enc, self.face_canvas) if face_enc else None

        if self.decrypted_aadhar and self.decrypted_face:
            self.compare_button.grid()  # Show compare button

    def display_decrypted_image(self, encrypted_path, image_label):
        """Decrypt and display the image."""
        if os.path.exists(encrypted_path):
            decrypted_path = decrypt_file(encrypted_path)
            if decrypted_path and os.path.exists(decrypted_path):
                img = Image.open(decrypted_path).resize((200, 200))
                img = ImageTk.PhotoImage(img)
                image_label.config(image=img)
                image_label.image = img
                return decrypted_path
            else:
                messagebox.showerror("Error", f"Failed to decrypt: {os.path.basename(encrypted_path)}")
        return None

    def compare_faces(self):
        """Compares the captured face with the Aadhaar image."""
        if not self.decrypted_aadhar or not self.decrypted_face:
            messagebox.showerror("Error", "Missing images for comparison.")
            return

        try:
            result = DeepFace.verify(self.decrypted_face, self.decrypted_aadhar, model_name="Facenet", enforce_detection=False)
            if result["verified"]:
                messagebox.showinfo("Success", "Face matched successfully!")
                self.face_matched = True
            else:
                messagebox.showerror("Mismatch", "Face does not match the Aadhaar image!")
                self.face_matched = False

            self.verify_button.grid()  # Show verification button after face check
        except Exception as e:
            messagebox.showerror("Error", f"Face comparison failed: {e}")

    def run_full_verification(self):
        """Runs Aadhaar, PAN, and RBI verification and updates the blockchain."""
        aadhar_number = self.aadhar_entry.get().strip()
        if not aadhar_number:
            messagebox.showerror("Error", "Aadhaar number missing.")
            return

        user_folder = os.path.join(USER_FOLDER, aadhar_number)
        user_id = aadhar_number  # Assuming user_id is the Aadhaar number

        encrypted_aadhar_path = os.path.join(user_folder, "aadhar.jpeg.enc")
        encrypted_pan_path = os.path.join(user_folder, "pan.jpeg.enc")

        # Run verifications
        bank_verification = "Approved" if self.face_matched else "Rejected"
        aadhar_verification = "Approved" if verify_aadhar(aadhar_number) else "Rejected"
        pan_verification = "Approved" if verify_pan(aadhar_number) else "Rejected"
        rbi_verification = "Approved" if verify_rbi(user_id) else "Rejected"

        verification_statuses = {
            "bank_verification_status": bank_verification,
            "aadhar_verification_status": aadhar_verification,
            "pan_verification_status": pan_verification,
            "rbi_verification_status": rbi_verification
        }

        documents = {
            "aadhar_doc": encrypted_aadhar_path,
            "pan_doc": encrypted_pan_path
        }

        add_block(user_id, aadhar_number, self.decrypted_face, verification_statuses, documents)
        messagebox.showinfo("Blockchain", "KYC verification status updated in blockchain!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()
'''

'''This is working '''

'''import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from encryption import decrypt_file
from blockchain import add_block
from mock_apis import verify_aadhar, verify_pan, verify_rbi
from deepface import DeepFace

USER_FOLDER = "users"

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel - KYC Verification")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Aadhaar input
        ttk.Label(self.scrollable_frame, text="Enter Aadhaar Number:")\
            .grid(row=0, column=0, padx=10, pady=10)
        self.aadhar_entry = ttk.Entry(self.scrollable_frame)
        self.aadhar_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(
            self.scrollable_frame,
            text="Load KYC Data",
            command=self.load_kyc_data
        ).grid(row=0, column=2, padx=10, pady=10)

        # Aadhaar image
        ttk.Label(self.scrollable_frame, text="Aadhaar Image:")\
            .grid(row=1, column=0, padx=10, pady=10)
        self.aadhar_canvas = ttk.Label(self.scrollable_frame)
        self.aadhar_canvas.grid(row=1, column=1, padx=10, pady=10)
        self.aadhar_zoom_btn = ttk.Button(
            self.scrollable_frame,
            text="View Aadhaar Image",
            command=lambda: self.open_zoom_window(self.decrypted_aadhar)
        )
        self.aadhar_zoom_btn.grid(row=1, column=2, padx=10, pady=10)

        # PAN image
        ttk.Label(self.scrollable_frame, text="PAN Image:")\
            .grid(row=2, column=0, padx=10, pady=10)
        self.pan_canvas = ttk.Label(self.scrollable_frame)
        self.pan_canvas.grid(row=2, column=1, padx=10, pady=10)
        self.pan_zoom_btn = ttk.Button(
            self.scrollable_frame,
            text="View PAN Image",
            command=lambda: self.open_zoom_window(self.decrypted_pan)
        )
        self.pan_zoom_btn.grid(row=2, column=2, padx=10, pady=10)

        # Captured face
        ttk.Label(self.scrollable_frame, text="Captured Face:")\
            .grid(row=3, column=0, padx=10, pady=10)
        self.face_canvas = ttk.Label(self.scrollable_frame)
        self.face_canvas.grid(row=3, column=1, padx=10, pady=10)
        self.face_zoom_btn = ttk.Button(
            self.scrollable_frame,
            text="View Captured Face",
            command=lambda: self.open_zoom_window(self.decrypted_face)
        )
        self.face_zoom_btn.grid(row=3, column=2, padx=10, pady=10)

        # Compare & verify buttons
        self.compare_button = ttk.Button(
            self.scrollable_frame,
            text="Compare Faces",
            command=self.compare_faces
        )
        self.compare_button.grid(row=4, column=1, pady=10)
        self.compare_button.grid_remove()

        self.verify_button = ttk.Button(
            self.scrollable_frame,
            text="Run Full Verification",
            command=self.run_full_verification
        )
        self.verify_button.grid(row=5, column=1, pady=10)
        self.verify_button.grid_remove()

    def load_kyc_data(self):
        aadhar_number = self.aadhar_entry.get().strip()
        if not aadhar_number:
            messagebox.showerror("Error", "Please enter a valid Aadhaar number.")
            return

        user_folder = os.path.join(USER_FOLDER, aadhar_number)
        if not os.path.exists(user_folder):
            messagebox.showerror("Error", f"No records found for Aadhaar: {aadhar_number}")
            return

        aadhar_enc = os.path.join(user_folder, "aadhar.jpeg.enc")
        pan_enc = os.path.join(user_folder, "pan.jpeg.enc")
        face_enc = next(
            (os.path.join(user_folder, f) for f in os.listdir(user_folder)
             if f.endswith("_captured_face.jpg.enc")), None
        )

        self.decrypted_aadhar = self.display_decrypted_image(aadhar_enc, self.aadhar_canvas)
        self.decrypted_pan = self.display_decrypted_image(pan_enc, self.pan_canvas)
        self.decrypted_face = (
            self.display_decrypted_image(face_enc, self.face_canvas)
            if face_enc else None
        )

        if self.decrypted_aadhar and self.decrypted_face:
            self.compare_button.grid()

    def display_decrypted_image(self, encrypted_path, image_label):
        if not encrypted_path or not os.path.exists(encrypted_path):
            return None

        decrypted_path = decrypt_file(encrypted_path)
        if not decrypted_path or not os.path.exists(decrypted_path):
            messagebox.showerror("Error", f"Failed to decrypt: {os.path.basename(encrypted_path)}")
            return None

        img = Image.open(decrypted_path)
        resized_img = img.resize((200, 200), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(resized_img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
        return decrypted_path

    def open_zoom_window(self, image_path):
        if not image_path or not os.path.exists(image_path):
            messagebox.showerror("Error", "Decrypted image not found.")
            return

        zoom_win = tk.Toplevel(self.root)
        zoom_win.title("Zoom Image")
        zoom_win.geometry("800x600")

        canvas = tk.Canvas(zoom_win, bg="gray")
        h_scroll = ttk.Scrollbar(zoom_win, orient="horizontal", command=canvas.xview)
        v_scroll = ttk.Scrollbar(zoom_win, orient="vertical", command=canvas.yview)
        canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        canvas.pack(fill="both", expand=True, side="left")
        v_scroll.pack(fill="y", side="right")
        h_scroll.pack(fill="x", side="bottom")

        pil_img = Image.open(image_path)
        self.zoom_factor = 1.0

        def update_image():
            new_size = (
                int(pil_img.width * self.zoom_factor),
                int(pil_img.height * self.zoom_factor)
            )
            zoomed = pil_img.resize(new_size, Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(zoomed)
            canvas.delete("IMG")
            canvas.create_image(0, 0, image=img_tk, anchor="nw", tags="IMG")
            canvas.config(scrollregion=canvas.bbox("all"))
            canvas.image = img_tk

        def zoom_in():
            self.zoom_factor *= 1.2
            update_image()

        def zoom_out():
            self.zoom_factor /= 1.2
            update_image()

        zoom_in_btn = ttk.Button(zoom_win, text="Zoom In", command=zoom_in)
        zoom_in_btn.pack(side="top", anchor="ne", padx=5, pady=5)

        zoom_out_btn = ttk.Button(zoom_win, text="Zoom Out", command=zoom_out)
        zoom_out_btn.pack(side="top", anchor="ne", padx=5)

        update_image()

    def compare_faces(self):
        if not self.decrypted_aadhar or not self.decrypted_face:
            messagebox.showerror("Error", "Missing images for comparison.")
            return

        try:
            result = DeepFace.verify(
                self.decrypted_face,
                self.decrypted_aadhar,
                model_name="Facenet",
                enforce_detection=False
            )
            if result["verified"]:
                messagebox.showinfo("Success", "Face matched successfully!")
                self.face_matched = True
            else:
                messagebox.showerror("Mismatch", "Face does not match the Aadhaar image!")
                self.face_matched = False

            self.verify_button.grid()
        except Exception as e:
            messagebox.showerror("Error", f"Face comparison failed: {e}")

    def run_full_verification(self):
        aadhar_number = self.aadhar_entry.get().strip()
        if not aadhar_number:
            messagebox.showerror("Error", "Aadhaar number missing.")
            return

        user_folder = os.path.join(USER_FOLDER, aadhar_number)
        user_id = aadhar_number

        encrypted_aadhar_path = os.path.join(user_folder, "aadhar.jpeg.enc")
        encrypted_pan_path = os.path.join(user_folder, "pan.jpeg.enc")

        statuses = {
            "bank_verification_status": "Approved" if getattr(self, 'face_matched', False) else "Rejected",
            "aadhar_verification_status": "Approved" if verify_aadhar(aadhar_number) else "Rejected",
            "pan_verification_status": "Approved" if verify_pan(aadhar_number) else "Rejected",
            "rbi_verification_status": "Approved" if verify_rbi(user_id) else "Rejected"
        }

        documents = {
            "aadhar_doc": encrypted_aadhar_path,
            "pan_doc": encrypted_pan_path
        }

        add_block(user_id, aadhar_number, self.decrypted_face, statuses, documents)
        messagebox.showinfo("Blockchain", "KYC verification status updated")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()'''


'''Scroable list integrated code'''

'''import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import json

from encryption import decrypt_file, decrypt_text
from blockchain import add_block, load_blockchain
from mock_apis import verify_aadhar, verify_pan, verify_rbi
from deepface import DeepFace

USER_FOLDER = "users"

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel - KYC Verification")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        ttk.Label(self.scrollable_frame, text="Enter Aadhaar Number:").grid(row=0, column=0, padx=10, pady=10)
        self.aadhar_entry = ttk.Entry(self.scrollable_frame)
        self.aadhar_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.scrollable_frame, text="Load KYC Data", command=self.load_kyc_data)\
            .grid(row=0, column=2, padx=10, pady=10)

        # Aadhaar image
        ttk.Label(self.scrollable_frame, text="Aadhaar Image:").grid(row=1, column=0, padx=10, pady=10)
        self.aadhar_canvas = ttk.Label(self.scrollable_frame)
        self.aadhar_canvas.grid(row=1, column=1, padx=10, pady=10)
        self.aadhar_zoom_btn = ttk.Button(self.scrollable_frame, text="View Aadhaar Image", command=lambda: self.open_zoom_window(self.decrypted_aadhar))
        self.aadhar_zoom_btn.grid(row=1, column=2, padx=10, pady=10)

        # PAN image
        ttk.Label(self.scrollable_frame, text="PAN Image:").grid(row=2, column=0, padx=10, pady=10)
        self.pan_canvas = ttk.Label(self.scrollable_frame)
        self.pan_canvas.grid(row=2, column=1, padx=10, pady=10)
        self.pan_zoom_btn = ttk.Button(self.scrollable_frame, text="View PAN Image", command=lambda: self.open_zoom_window(self.decrypted_pan))
        self.pan_zoom_btn.grid(row=2, column=2, padx=10, pady=10)

        # Captured face
        ttk.Label(self.scrollable_frame, text="Captured Face:").grid(row=3, column=0, padx=10, pady=10)
        self.face_canvas = ttk.Label(self.scrollable_frame)
        self.face_canvas.grid(row=3, column=1, padx=10, pady=10)
        self.face_zoom_btn = ttk.Button(self.scrollable_frame, text="View Captured Face", command=lambda: self.open_zoom_window(self.decrypted_face))
        self.face_zoom_btn.grid(row=3, column=2, padx=10, pady=10)

        # Decrypted user details display
        self.details_text = tk.Text(self.scrollable_frame, height=10, width=80)
        self.details_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Compare button
        self.compare_button = ttk.Button(self.scrollable_frame, text="Compare Faces", command=self.compare_faces)
        self.compare_button.grid(row=5, column=1, pady=10)
        self.compare_button.grid_remove()

        self.verify_button = ttk.Button(self.scrollable_frame, text="Run Full Verification", command=self.run_full_verification)
        self.verify_button.grid(row=6, column=1, pady=10)
        self.verify_button.grid_remove()

    def load_kyc_data(self):
        aadhar_number = self.aadhar_entry.get().strip()
        if not aadhar_number:
            messagebox.showerror("Error", "Please enter a valid Aadhaar number.")
            return

        # Load latest matching block from blockchain
        blockchain = load_blockchain()
        user_block = next((b for b in blockchain if decrypt_text(b["header"]["aadhar_number"]) == aadhar_number), None)
        if not user_block:
            messagebox.showerror("Error", f"No records found for Aadhaar: {aadhar_number}")
            return

        header = user_block["header"]
        self.user_id = header["user_id"]

        # Decrypt user details
        self.user_details = {
            "name": decrypt_text(header["name"]),
            "pan_number": decrypt_text(header["pan_number"]),
            "date_of_birth": decrypt_text(header["date_of_birth"]),
            "address": decrypt_text(header["address"])
        }

        # Display decrypted details
        details_text = "\n".join(f"{k.replace('_', ' ').title()}: {v}" for k, v in self.user_details.items())
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert(tk.END, details_text)

        user_folder = os.path.dirname(header["aadhar_doc"])

        self.decrypted_aadhar = self.display_decrypted_image(header["aadhar_doc"], self.aadhar_canvas)
        self.decrypted_pan = self.display_decrypted_image(header["pan_doc"], self.pan_canvas)
        self.decrypted_face = self.display_decrypted_image(header["captured_face_path"], self.face_canvas)

        if self.decrypted_aadhar and self.decrypted_face:
            self.compare_button.grid()

    def display_decrypted_image(self, encrypted_path, image_label):
        if not encrypted_path or not os.path.exists(encrypted_path):
            return None
        decrypted_path = decrypt_file(encrypted_path)
        if not decrypted_path or not os.path.exists(decrypted_path):
            messagebox.showerror("Error", f"Failed to decrypt: {os.path.basename(encrypted_path)}")
            return None
        img = Image.open(decrypted_path)
        resized_img = img.resize((200, 200), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(resized_img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
        return decrypted_path

    def open_zoom_window(self, image_path):
        if not image_path or not os.path.exists(image_path):
            messagebox.showerror("Error", "Decrypted image not found.")
            return

        zoom_win = tk.Toplevel(self.root)
        zoom_win.title("Zoom Image")
        zoom_win.geometry("800x600")

        canvas = tk.Canvas(zoom_win, bg="gray")
        h_scroll = ttk.Scrollbar(zoom_win, orient="horizontal", command=canvas.xview)
        v_scroll = ttk.Scrollbar(zoom_win, orient="vertical", command=canvas.yview)
        canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        canvas.pack(fill="both", expand=True, side="left")
        v_scroll.pack(fill="y", side="right")
        h_scroll.pack(fill="x", side="bottom")

        pil_img = Image.open(image_path)
        self.zoom_factor = 1.0

        def update_image():
            new_size = (int(pil_img.width * self.zoom_factor), int(pil_img.height * self.zoom_factor))
            zoomed = pil_img.resize(new_size, Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(zoomed)
            canvas.delete("IMG")
            canvas.create_image(0, 0, image=img_tk, anchor="nw", tags="IMG")
            canvas.config(scrollregion=canvas.bbox("all"))
            canvas.image = img_tk

        def zoom_in():
            self.zoom_factor *= 1.2
            update_image()

        def zoom_out():
            self.zoom_factor /= 1.2
            update_image()

        ttk.Button(zoom_win, text="Zoom In", command=zoom_in).pack(side="top", anchor="ne", padx=5, pady=5)
        ttk.Button(zoom_win, text="Zoom Out", command=zoom_out).pack(side="top", anchor="ne", padx=5)
        update_image()

    def compare_faces(self):
        if not self.decrypted_aadhar or not self.decrypted_face:
            messagebox.showerror("Error", "Missing images for comparison.")
            return
        try:
            result = DeepFace.verify(self.decrypted_face, self.decrypted_aadhar, model_name="Facenet", enforce_detection=False)
            if result["verified"]:
                messagebox.showinfo("Success", "Face matched successfully!")
                self.face_matched = True
            else:
                messagebox.showerror("Mismatch", "Face does not match the Aadhaar image!")
                self.face_matched = False
            self.verify_button.grid()
        except Exception as e:
            messagebox.showerror("Error", f"Face comparison failed: {e}")

    def run_full_verification(self):
        if not hasattr(self, "user_id"):
            messagebox.showerror("Error", "User not loaded.")
            return

        aadhar_number = self.aadhar_entry.get().strip()

        statuses = {
            "bank_verification_status": "Approved" if getattr(self, 'face_matched', False) else "Rejected",
            "aadhar_verification_status": "Approved" if verify_aadhar(aadhar_number) else "Rejected",
            "pan_verification_status": "Approved" if verify_pan(aadhar_number) else "Rejected",
            "rbi_verification_status": "Approved" if verify_rbi(self.user_id) else "Rejected"
        }

        documents = {
            "aadhar_doc": self.decrypted_aadhar,
            "pan_doc": self.decrypted_pan
        }

        add_block(self.user_id, aadhar_number, self.decrypted_face, statuses, documents, self.user_details)
        messagebox.showinfo("Blockchain", "KYC verification status updated")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()


'''


'''Version 4'''

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import json

from encryption import decrypt_file, decrypt_text, cipher
from blockchain import add_block, load_blockchain
from mock_apis import verify_aadhar, verify_pan, verify_rbi
from deepface import DeepFace

USER_FOLDER = "users"

class AdminGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel - KYC Verification")
        self.root.geometry("800x600")

        self.canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        ttk.Label(self.scrollable_frame, text="Enter Aadhaar Number:").grid(row=0, column=0, padx=10, pady=10)
        self.aadhar_entry = ttk.Entry(self.scrollable_frame)
        self.aadhar_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.scrollable_frame, text="Load KYC Data", command=self.load_kyc_data)\
            .grid(row=0, column=2, padx=10, pady=10)

        # Aadhaar image
        ttk.Label(self.scrollable_frame, text="Aadhaar Image:").grid(row=1, column=0, padx=10, pady=10)
        self.aadhar_canvas = ttk.Label(self.scrollable_frame)
        self.aadhar_canvas.grid(row=1, column=1, padx=10, pady=10)
        self.aadhar_zoom_btn = ttk.Button(self.scrollable_frame, text="View Aadhaar Image", command=lambda: self.open_zoom_window(self.decrypted_aadhar))
        self.aadhar_zoom_btn.grid(row=1, column=2, padx=10, pady=10)

        # PAN image
        ttk.Label(self.scrollable_frame, text="PAN Image:").grid(row=2, column=0, padx=10, pady=10)
        self.pan_canvas = ttk.Label(self.scrollable_frame)
        self.pan_canvas.grid(row=2, column=1, padx=10, pady=10)
        self.pan_zoom_btn = ttk.Button(self.scrollable_frame, text="View PAN Image", command=lambda: self.open_zoom_window(self.decrypted_pan))
        self.pan_zoom_btn.grid(row=2, column=2, padx=10, pady=10)

        # Captured face
        ttk.Label(self.scrollable_frame, text="Captured Face:").grid(row=3, column=0, padx=10, pady=10)
        self.face_canvas = ttk.Label(self.scrollable_frame)
        self.face_canvas.grid(row=3, column=1, padx=10, pady=10)
        self.face_zoom_btn = ttk.Button(self.scrollable_frame, text="View Captured Face", command=lambda: self.open_zoom_window(self.decrypted_face))
        self.face_zoom_btn.grid(row=3, column=2, padx=10, pady=10)

        # Decrypted user details display
        self.details_text = tk.Text(self.scrollable_frame, height=10, width=80)
        self.details_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Compare button
        self.compare_button = ttk.Button(self.scrollable_frame, text="Compare Faces", command=self.compare_faces)
        self.compare_button.grid(row=5, column=1, pady=10)
        self.compare_button.grid_remove()

        self.verify_button = ttk.Button(self.scrollable_frame, text="Run verification", command=self.run_full_verification)
        self.verify_button.grid(row=6, column=1, pady=10)
        self.verify_button.grid_remove()

    def load_kyc_data(self):
        aadhar_number = self.aadhar_entry.get().strip()
        if not aadhar_number:
            messagebox.showerror("Error", "Please enter a valid Aadhaar number.")
            return

        blockchain = load_blockchain()
        user_block = next((b for b in blockchain if decrypt_text(b["header"]["aadhar_number"]) == aadhar_number), None)
        if not user_block:
            messagebox.showerror("Error", f"No records found for Aadhaar: {aadhar_number}")
            return

        header = user_block["header"]
        self.user_id = header["user_id"]

        self.user_details = {
            "name": decrypt_text(header["name"]),
            "pan_number": decrypt_text(header["pan_number"]),
            "date_of_birth": decrypt_text(header["date_of_birth"]),
            "address": decrypt_text(header["address"]),
        }

        details_text = "\n".join(f"{k.replace('_', ' ').title()}: {v}" for k, v in self.user_details.items())
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert(tk.END, details_text)

        self.user_folder = os.path.dirname(header["aadhar_doc"])

        self.decrypted_aadhar = self.display_decrypted_image(header["aadhar_doc"], self.aadhar_canvas)
        self.decrypted_pan = self.display_decrypted_image(header["pan_doc"], self.pan_canvas)
        self.decrypted_face = self.display_decrypted_image(header["captured_face_path"], self.face_canvas)

        if self.decrypted_aadhar and self.decrypted_face:
            self.compare_button.grid()

    def display_decrypted_image(self, encrypted_path, image_label):
        if not encrypted_path or not os.path.exists(encrypted_path):
            return None
        decrypted_path = decrypt_file(encrypted_path)
        if not decrypted_path or not os.path.exists(decrypted_path):
            messagebox.showerror("Error", f"Failed to decrypt: {os.path.basename(encrypted_path)}")
            return None
        img = Image.open(decrypted_path)
        resized_img = img.resize((200, 200), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(resized_img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
        return decrypted_path

    def open_zoom_window(self, image_path):
        if not image_path or not os.path.exists(image_path):
            messagebox.showerror("Error", "Decrypted image not found.")
            return

        zoom_win = tk.Toplevel(self.root)
        zoom_win.title("Zoom Image")
        zoom_win.geometry("800x600")

        canvas = tk.Canvas(zoom_win, bg="gray")
        h_scroll = ttk.Scrollbar(zoom_win, orient="horizontal", command=canvas.xview)
        v_scroll = ttk.Scrollbar(zoom_win, orient="vertical", command=canvas.yview)
        canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        canvas.pack(fill="both", expand=True, side="left")
        v_scroll.pack(fill="y", side="right")
        h_scroll.pack(fill="x", side="bottom")

        pil_img = Image.open(image_path)
        self.zoom_factor = 1.0

        def update_image():
            new_size = (int(pil_img.width * self.zoom_factor), int(pil_img.height * self.zoom_factor))
            zoomed = pil_img.resize(new_size, Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(zoomed)
            canvas.delete("IMG")
            canvas.create_image(0, 0, image=img_tk, anchor="nw", tags="IMG")
            canvas.config(scrollregion=canvas.bbox("all"))
            canvas.image = img_tk

        def zoom_in():
            self.zoom_factor *= 1.2
            update_image()

        def zoom_out():
            self.zoom_factor /= 1.2
            update_image()

        ttk.Button(zoom_win, text="Zoom In", command=zoom_in).pack(side="top", anchor="ne", padx=5, pady=5)
        ttk.Button(zoom_win, text="Zoom Out", command=zoom_out).pack(side="top", anchor="ne", padx=5)
        update_image()

    def compare_faces(self):
        if not self.decrypted_aadhar or not self.decrypted_face:
            messagebox.showerror("Error", "Missing images for comparison.")
            return
        try:
            result = DeepFace.verify(self.decrypted_face, self.decrypted_aadhar, model_name="Facenet", enforce_detection=False)
            if result["verified"]:
                messagebox.showinfo("Success", "Face matched successfully!")
                self.face_matched = True
            else:
                messagebox.showerror("Mismatch", "Face does not match the Aadhaar image!")
                self.face_matched = False
            self.verify_button.grid()
        except Exception as e:
            messagebox.showerror("Error", f"Face comparison failed: {e}")

    def run_full_verification(self):
        if not hasattr(self, "user_id"):
            messagebox.showerror("Error", "User not loaded.")
            return

        aadhar_number = self.aadhar_entry.get().strip()

        if getattr(self, 'face_matched', False):
            statuses = {
                "bank_verification_status": "Approved",
                "aadhar_verification_status": "Approved" if verify_aadhar(aadhar_number) else "Rejected",
                "pan_verification_status": "Approved" if verify_pan(aadhar_number) else "Rejected",
                "rbi_verification_status": "Approved" if verify_rbi(self.user_id) else "Rejected"
            }
        else:
            # If face mismatch, reject everything
            statuses = {
                "bank_verification_status": "Rejected",
                "aadhar_verification_status": "Rejected",
                "pan_verification_status": "Rejected",
                "rbi_verification_status": "Rejected"
            }

        documents = {
            "aadhar_doc": self.decrypted_aadhar,
            "pan_doc": self.decrypted_pan
        }

        enc_data = {
            "name": cipher.encrypt(self.user_details["name"].encode()).decode(),
            "pan_number": cipher.encrypt(self.user_details["pan_number"].encode()).decode(),
            "date_of_birth": cipher.encrypt(self.user_details["date_of_birth"].encode()).decode(),
            "address": cipher.encrypt(self.user_details["address"].encode()).decode(),
            "aadhar_number": cipher.encrypt(aadhar_number.encode()).decode()
        }

        add_block(
            user_id=self.user_id,
            aadhar_number=enc_data["aadhar_number"],
            user_details=enc_data,
            captured_face_path=self.decrypted_face,
            verification_statuses=statuses,
            documents=documents
        )

        messagebox.showinfo("Blockchain", "KYC verification status updated successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminGUI(root)
    root.mainloop()
