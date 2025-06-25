'''import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import time
from blockchain import add_block
from encryption import encrypt_file  # Ensure this function is correctly defined

# Ensure the 'users/' directory exists
if not os.path.exists("users"):
    os.makedirs("users")

class KYCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-KYC Registration")

        # User Input Fields
        tk.Label(root, text="Aadhar Number:").grid(row=0, column=0)
        tk.Label(root, text="PAN Number:").grid(row=1, column=0)
        tk.Label(root, text="Name:").grid(row=2, column=0)
        tk.Label(root, text="DOB (YYYY-MM-DD):").grid(row=3, column=0)

        self.aadhar_entry = tk.Entry(root)
        self.pan_entry = tk.Entry(root)
        self.name_entry = tk.Entry(root)
        self.dob_entry = tk.Entry(root)

        self.aadhar_entry.grid(row=0, column=1)
        self.pan_entry.grid(row=1, column=1)
        self.name_entry.grid(row=2, column=1)
        self.dob_entry.grid(row=3, column=1)

        # Upload Document Buttons
        self.upload_aadhar_button = tk.Button(root, text="Upload Aadhaar", command=self.upload_aadhar)
        self.upload_pan_button = tk.Button(root, text="Upload PAN", command=self.upload_pan)
        self.upload_aadhar_button.grid(row=4, column=0, columnspan=2)
        self.upload_pan_button.grid(row=5, column=0, columnspan=2)

        # Capture Face Button
        self.capture_button = tk.Button(root, text="Capture Face", command=self.capture_face)
        self.capture_button.grid(row=6, column=0, columnspan=2)

        # Submit KYC Button (Initially Disabled)
        self.submit_button = tk.Button(root, text="Submit KYC", command=self.submit_kyc, state=tk.DISABLED)
        self.submit_button.grid(row=7, column=0, columnspan=2)

        self.aadhar_path = None
        self.pan_path = None
        self.captured_face = None

    def upload_aadhar(self):
        """ Upload Aadhaar document """
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.aadhar_path = file_path
            messagebox.showinfo("Success", "Aadhaar Uploaded Successfully!")

    def upload_pan(self):
        """ Upload PAN document """
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.pan_path = file_path
            messagebox.showinfo("Success", "PAN Uploaded Successfully!")

    def capture_face(self):
        """ Capture live face from webcam """
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Show a frame for face alignment
            cv2.imshow("Align your face & Press 'C' to Capture", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("c"):  # Press 'C' to capture
                break

        cap.release()
        cv2.destroyAllWindows()

        # Save Captured Face
        face_path = f"users/{int(time.time())}_captured_face.jpg"
        cv2.imwrite(face_path, frame)
        self.captured_face = face_path
        self.submit_button.config(state=tk.NORMAL)  # Enable Submit Button

    def submit_kyc(self):
        """ Submit KYC after collecting user details and encrypting files """
        user_id = int(time.time())
        aadhar = self.aadhar_entry.get().strip()
        pan = self.pan_entry.get().strip()
        name = self.name_entry.get().strip()
        dob = self.dob_entry.get().strip()

        if not all([aadhar, pan, name, dob, self.aadhar_path, self.pan_path, self.captured_face]):
            messagebox.showerror("Error", "All fields & documents are required!")
            return

        try:
            # Encrypt Aadhaar, PAN, and Face Images
            encrypted_aadhar_path = encrypt_file(self.aadhar_path,aadhar)  # ✅ Fixed
            encrypted_pan_path = encrypt_file(self.pan_path,aadhar)        # ✅ Fixed
            encrypted_face_path = encrypt_file(self.captured_face,aadhar)  # ✅ Fixed

            # Add KYC details to Blockchain (No Face Comparison)
            add_block(user_id, aadhar, encrypted_face_path, {
                "bank_verification_status": "Pending ⏳",
                "aadhar_doc": encrypted_aadhar_path,
                "pan_doc": encrypted_pan_path
            })

            messagebox.showinfo("Success", "KYC Request Submitted!")
            self.root.destroy()  # Close the app after submission

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Run the Tkinter App
root = tk.Tk()
app = KYCApp(root)
root.mainloop()
'''

'''This one is working'''
'''import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import time
from blockchain import add_block
from encryption import encrypt_file  # Ensure this function is correctly defined

# Ensure the 'users/' directory exists
if not os.path.exists("users"):
    os.makedirs("users")

class KYCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-KYC Registration")

        # User Input Fields
        tk.Label(root, text="Aadhar Number:").grid(row=0, column=0)
        tk.Label(root, text="PAN Number:").grid(row=1, column=0)
        tk.Label(root, text="Name:").grid(row=2, column=0)
        tk.Label(root, text="DOB (YYYY-MM-DD):").grid(row=3, column=0)

        self.aadhar_entry = tk.Entry(root)
        self.pan_entry = tk.Entry(root)
        self.name_entry = tk.Entry(root)
        self.dob_entry = tk.Entry(root)

        self.aadhar_entry.grid(row=0, column=1)
        self.pan_entry.grid(row=1, column=1)
        self.name_entry.grid(row=2, column=1)
        self.dob_entry.grid(row=3, column=1)

        # Upload Document Buttons
        self.upload_aadhar_button = tk.Button(root, text="Upload Aadhaar", command=self.upload_aadhar)
        self.upload_pan_button = tk.Button(root, text="Upload PAN", command=self.upload_pan)
        self.upload_aadhar_button.grid(row=4, column=0, columnspan=2)
        self.upload_pan_button.grid(row=5, column=0, columnspan=2)

        # Capture Face Button
        self.capture_button = tk.Button(root, text="Capture Face", command=self.capture_face)
        self.capture_button.grid(row=6, column=0, columnspan=2)

        # Submit KYC Button (Initially Disabled)
        self.submit_button = tk.Button(root, text="Submit KYC", command=self.submit_kyc, state=tk.DISABLED)
        self.submit_button.grid(row=7, column=0, columnspan=2)

        self.aadhar_path = None
        self.pan_path = None
        self.captured_face = None

    def upload_aadhar(self):
        """ Upload Aadhaar document """
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.aadhar_path = file_path
            messagebox.showinfo("Success", "Aadhaar Uploaded Successfully!")

    def upload_pan(self):
        """ Upload PAN document """
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.pan_path = file_path
            messagebox.showinfo("Success", "PAN Uploaded Successfully!")

    def capture_face(self):
        """ Capture live face from webcam """
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Show a frame for face alignment
            cv2.imshow("Align your face & Press 'C' to Capture", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("c"):  # Press 'C' to capture
                break

        cap.release()
        cv2.destroyAllWindows()

        # Save Captured Face
        face_path = f"users/{int(time.time())}_captured_face.jpg"
        cv2.imwrite(face_path, frame)
        self.captured_face = face_path
        self.submit_button.config(state=tk.NORMAL)  # Enable Submit Button

    def submit_kyc(self):
        """ Submit KYC after collecting user details and encrypting files """
        user_id = int(time.time())
        aadhar = self.aadhar_entry.get().strip()
        pan = self.pan_entry.get().strip()
        name = self.name_entry.get().strip()
        dob = self.dob_entry.get().strip()

        if not all([aadhar, pan, name, dob, self.aadhar_path, self.pan_path, self.captured_face]):
            messagebox.showerror("Error", "All fields & documents are required!")
            return

        try:
            # Encrypt Aadhaar, PAN, and Face Images
            encrypted_aadhar_path = encrypt_file(self.aadhar_path, aadhar)  
            encrypted_pan_path = encrypt_file(self.pan_path, aadhar)        
            encrypted_face_path = encrypt_file(self.captured_face, aadhar)  

            # Initial verification statuses (all pending)
            verification_statuses = {
                "bank_verification_status": "Pending ⏳",
                "aadhar_verification_status": "Pending ⏳",
                "pan_verification_status": "Pending ⏳",
                "rbi_verification_status": "Pending ⏳"
            }

            # Add KYC details to Blockchain
            add_block(user_id, aadhar, encrypted_face_path, verification_statuses, {
                "aadhar_doc": encrypted_aadhar_path,
                "pan_doc": encrypted_pan_path
            })

            messagebox.showinfo("Success", "KYC Request Submitted!")
            self.root.destroy()  # Close the app after submission

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Run the Tkinter App
root = tk.Tk()
app = KYCApp(root)
root.mainloop()'''


'''Adding liveness feature'''
'''import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import time
from blockchain import add_block
from encryption import encrypt_file  # Takes (file_path, user_id) and returns encrypted path

# Ensure the 'users/' directory exists
if not os.path.exists("users"):
    os.makedirs("users")

class KYCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E‑KYC Registration")

        # User Input Fields
        tk.Label(root, text="Aadhar Number:").grid(row=0, column=0, sticky="e")
        tk.Label(root, text="PAN Number:").grid(row=1, column=0, sticky="e")
        tk.Label(root, text="Name:").grid(row=2, column=0, sticky="e")
        tk.Label(root, text="DOB (YYYY-MM-DD):").grid(row=3, column=0, sticky="e")

        self.aadhar_entry = tk.Entry(root)
        self.pan_entry    = tk.Entry(root)
        self.name_entry   = tk.Entry(root)
        self.dob_entry    = tk.Entry(root)

        self.aadhar_entry.grid(row=0, column=1)
        self.pan_entry   .grid(row=1, column=1)
        self.name_entry  .grid(row=2, column=1)
        self.dob_entry   .grid(row=3, column=1)

        # Upload Document Buttons
        self.upload_aadhar_button = tk.Button(root, text="Upload Aadhaar", command=self.upload_aadhar)
        self.upload_pan_button    = tk.Button(root, text="Upload PAN",     command=self.upload_pan)
        self.upload_aadhar_button.grid(row=4, column=0, columnspan=2, pady=5)
        self.upload_pan_button   .grid(row=5, column=0, columnspan=2, pady=5)

        # Capture Face Button
        self.capture_button = tk.Button(root, text="Capture Face", command=self.capture_face)
        self.capture_button.grid(row=6, column=0, columnspan=2, pady=5)

        # Submit KYC Button (Initially Disabled)
        self.submit_button = tk.Button(root, text="Submit KYC", command=self.submit_kyc, state=tk.DISABLED)
        self.submit_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.aadhar_path   = None
        self.pan_path      = None
        self.captured_face = None

    def upload_aadhar(self):
        file_path = filedialog.askopenfilename(
            title="Select Aadhaar Image",
            filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")]
        )
        if file_path:
            self.aadhar_path = file_path
            messagebox.showinfo("Success", "Aadhaar uploaded.")

    def upload_pan(self):
        file_path = filedialog.askopenfilename(
            title="Select PAN Image",
            filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")]
        )
        if file_path:
            self.pan_path = file_path
            messagebox.showinfo("Success", "PAN uploaded.")

    def capture_face(self):
        face_cascade  = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")
        smile_cascade = cv2.CascadeClassifier("cascades/haarcascade_smile.xml")

        cap = cv2.VideoCapture(0)
        start = time.time()
        smile_start_time = None
        captured = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elapsed = time.time() - start

            if elapsed < 3:
                cv2.putText(frame, f"Get Ready: {3 - int(elapsed)}",
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                cv2.imshow("Capture Face", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                   break
                continue

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face_roi_gray  = gray[y:y+h, x:x+w]
                face_roi_color = frame[y:y+h, x:x+w]

                smiles = smile_cascade.detectMultiScale(face_roi_gray, scaleFactor=2.0, minNeighbors=20)

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                for (sx, sy, sw, sh) in smiles:
                    smile_ratio = sw / w
                    if smile_ratio > 0.3:
                        if smile_start_time is None:
                            smile_start_time = time.time()
                        elif time.time() - smile_start_time > 0.8 and not captured:
                             face_img = frame[y:y+h, x:x+w]
                             face_file = f"users/{int(time.time())}_captured_face.jpg"
                             cv2.imwrite(face_file, face_img)
                             self.captured_face = face_file
                             self.submit_button.config(state=tk.NORMAL)
                             messagebox.showinfo("Success", "Smile detected! Face captured.")
                             captured = True
                             break
                    else:
                        smile_start_time = None

                if captured:
                    break

            cv2.imshow("Capture Face", frame)
            if captured or cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def submit_kyc(self):
        user_id = str(time.time())
        aadhar = self.aadhar_entry.get().strip()
        pan    = self.pan_entry.get().strip()
        name   = self.name_entry.get().strip()
        dob    = self.dob_entry.get().strip()

        if not all([aadhar, pan, name, dob, self.aadhar_path, self.pan_path, self.captured_face]):
            messagebox.showerror("Error", "All fields and documents are required!")
            return

        try:
            enc_aadhar = encrypt_file(self.aadhar_path, user_id)
            enc_pan    = encrypt_file(self.pan_path,    user_id)
            enc_face   = encrypt_file(self.captured_face, user_id)

            statuses = {
                "bank_verification_status":    "Pending ⏳",
                "aadhar_verification_status":  "Pending ⏳",
                "pan_verification_status":     "Pending ⏳",
                "rbi_verification_status":     "Pending ⏳",
            }

            add_block(user_id, aadhar, enc_face, statuses, {
                "aadhar_doc": enc_aadhar,
                "pan_doc":    enc_pan
            })

            messagebox.showinfo("Success", "KYC submitted to blockchain!")
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Submission failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KYCApp(root)
    root.mainloop()'''



'''Adding duplicate KYC request detection'''
'''import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import time
from blockchain import add_block, is_duplicate_kyc
from encryption import encrypt_file  # Takes (file_path, user_id) and returns encrypted path

# Ensure the 'users/' directory exists
if not os.path.exists("users"):
    os.makedirs("users")

class KYCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E‑KYC Registration")

        # User Input Fields
        tk.Label(root, text="Aadhar Number:").grid(row=0, column=0, sticky="e")
        tk.Label(root, text="PAN Number:").grid(row=1, column=0, sticky="e")
        tk.Label(root, text="Name:").grid(row=2, column=0, sticky="e")
        tk.Label(root, text="DOB (YYYY-MM-DD):").grid(row=3, column=0, sticky="e")

        self.aadhar_entry = tk.Entry(root)
        self.pan_entry    = tk.Entry(root)
        self.name_entry   = tk.Entry(root)
        self.dob_entry    = tk.Entry(root)

        self.aadhar_entry.grid(row=0, column=1)
        self.pan_entry   .grid(row=1, column=1)
        self.name_entry  .grid(row=2, column=1)
        self.dob_entry   .grid(row=3, column=1)

        # Upload Document Buttons
        self.upload_aadhar_button = tk.Button(root, text="Upload Aadhaar", command=self.upload_aadhar)
        self.upload_pan_button    = tk.Button(root, text="Upload PAN",     command=self.upload_pan)
        self.upload_aadhar_button.grid(row=4, column=0, columnspan=2, pady=5)
        self.upload_pan_button   .grid(row=5, column=0, columnspan=2, pady=5)

        # Capture Face Button
        self.capture_button = tk.Button(root, text="Capture Face", command=self.capture_face)
        self.capture_button.grid(row=6, column=0, columnspan=2, pady=5)

        # Submit KYC Button (Initially Disabled)
        self.submit_button = tk.Button(root, text="Submit KYC", command=self.submit_kyc, state=tk.DISABLED)
        self.submit_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.aadhar_path   = None
        self.pan_path      = None
        self.captured_face = None

    def upload_aadhar(self):
        file_path = filedialog.askopenfilename(
            title="Select Aadhaar Image",
            filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")]
        )
        if file_path:
            self.aadhar_path = file_path
            messagebox.showinfo("Success", "Aadhaar uploaded.")

    def upload_pan(self):
        file_path = filedialog.askopenfilename(
            title="Select PAN Image",
            filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")]
        )
        if file_path:
            self.pan_path = file_path
            messagebox.showinfo("Success", "PAN uploaded.")

    def capture_face(self):
        face_cascade  = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")
        smile_cascade = cv2.CascadeClassifier("cascades/haarcascade_smile.xml")

        cap = cv2.VideoCapture(0)
        start = time.time()
        smile_start_time = None
        captured = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elapsed = time.time() - start

            if elapsed < 3:
                cv2.putText(frame, f"Get Ready: {3 - int(elapsed)}",
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                cv2.imshow("Capture Face", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                   break
                continue

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face_roi_gray  = gray[y:y+h, x:x+w]
                face_roi_color = frame[y:y+h, x:x+w]

                smiles = smile_cascade.detectMultiScale(face_roi_gray, scaleFactor=2.0, minNeighbors=20)

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                for (sx, sy, sw, sh) in smiles:
                    smile_ratio = sw / w
                    if smile_ratio > 0.3:
                        if smile_start_time is None:
                            smile_start_time = time.time()
                        elif time.time() - smile_start_time > 0.8 and not captured:
                             face_img = frame[y:y+h, x:x+w]
                             face_file = f"users/{int(time.time())}_captured_face.jpg"
                             cv2.imwrite(face_file, face_img)
                             self.captured_face = face_file
                             self.submit_button.config(state=tk.NORMAL)
                             messagebox.showinfo("Success", "Smile detected! Face captured.")
                             captured = True
                             break
                    else:
                        smile_start_time = None

                if captured:
                    break

            cv2.imshow("Capture Face", frame)
            if captured or cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

        

    def submit_kyc(self):
        user_id = int(time.time())
        aadhar = self.aadhar_entry.get().strip()
        pan    = self.pan_entry.get().strip()
        name   = self.name_entry.get().strip()
        dob    = self.dob_entry.get().strip()

        if not all([aadhar, pan, name, dob, self.aadhar_path, self.pan_path, self.captured_face]):
            messagebox.showerror("Error", "All fields and documents are required!")
            return

        # ✅ Check for Duplicate KYC Request
        if is_duplicate_kyc(aadhar):
            messagebox.showwarning("Duplicate KYC Request", f"A KYC request already exists for Aadhaar: {aadhar}")
            return

        try:
            enc_aadhar = encrypt_file(self.aadhar_path, aadhar)
            enc_pan    = encrypt_file(self.pan_path,    aadhar)
            enc_face   = encrypt_file(self.captured_face, aadhar)

            statuses = {
                "bank_verification_status":    "Pending ⏳",
                "aadhar_verification_status":  "Pending ⏳",
                "pan_verification_status":     "Pending ⏳",
                "rbi_verification_status":     "Pending ⏳",
            }

            add_block(user_id, aadhar, enc_face, statuses, {
                "aadhar_doc": enc_aadhar,
                "pan_doc":    enc_pan
            })

            messagebox.showinfo("Success", "KYC submitted to blockchain!")
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Submission failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KYCApp(root)
    root.mainloop()'''



'''New version'''

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import time
from blockchain import add_block, is_duplicate_kyc
from encryption import encrypt_file, cipher

# Ensure the 'users/' directory exists
if not os.path.exists("users"):
    os.makedirs("users")


class KYCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 E‑KYC Registration Portal")
        self.root.geometry("420x450")
        self.root.configure(bg="#f5f5f5")

        title = tk.Label(root, text="E‑KYC Registration", font=("Helvetica", 18, "bold"), bg="#f5f5f5", fg="#333")
        title.pack(pady=10)

        form_frame = tk.Frame(root, bg="#f5f5f5")
        form_frame.pack()

        labels = ["Aadhaar Number:", "PAN Number:", "Name:", "DOB (YYYY-MM-DD):", "Address:"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = tk.Label(form_frame, text=label_text, bg="#f5f5f5", font=("Helvetica", 10, "bold"))
            label.grid(row=i, column=0, sticky="e", padx=10, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            self.entries[label_text] = entry

        self.aadhar_path = None
        self.pan_path = None
        self.captured_face = None

        tk.Button(root, text="📎 Upload Aadhaar", command=self.upload_aadhar,
                  bg="#007acc", fg="white", font=("Helvetica", 10, "bold")).pack(pady=5)

        tk.Button(root, text="📎 Upload PAN", command=self.upload_pan,
                  bg="#007acc", fg="white", font=("Helvetica", 10, "bold")).pack(pady=5)

        tk.Button(root, text="📷 Capture Face", command=self.capture_face,
                  bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold")).pack(pady=5)

        self.submit_button = tk.Button(root, text="🚀 Submit KYC", command=self.submit_kyc,
                                       state=tk.DISABLED, bg="#333", fg="white", font=("Helvetica", 10, "bold"))
        self.submit_button.pack(pady=15)

    def upload_aadhar(self):
        file_path = filedialog.askopenfilename(title="Select Aadhaar Image", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.aadhar_path = file_path
            messagebox.showinfo("Success", "✅ Aadhaar uploaded.")

    def upload_pan(self):
        file_path = filedialog.askopenfilename(title="Select PAN Image", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.pan_path = file_path
            messagebox.showinfo("Success", "✅ PAN uploaded.")

    def capture_face(self):
        face_cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")
        smile_cascade = cv2.CascadeClassifier("cascades/haarcascade_smile.xml")

        cap = cv2.VideoCapture(0)
        start = time.time()
        smile_start_time = None
        captured = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elapsed = time.time() - start

            if elapsed < 3:
                cv2.putText(frame, f"Get Ready: {3 - int(elapsed)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                cv2.imshow("Capture Face", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
                continue

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=2.0, minNeighbors=20)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                for (sx, sy, sw, sh) in smiles:
                    smile_ratio = sw / w
                    if smile_ratio > 0.3:
                        if smile_start_time is None:
                            smile_start_time = time.time()
                        elif time.time() - smile_start_time > 0.8 and not captured:
                            face_img = frame[y:y + h, x:x + w]
                            face_file = f"users/{int(time.time())}_captured_face.jpg"
                            cv2.imwrite(face_file, face_img)
                            self.captured_face = face_file
                            self.submit_button.config(state=tk.NORMAL)
                            messagebox.showinfo("Success", "😀 Smile detected! Face captured.")
                            captured = True
                            break
                    else:
                        smile_start_time = None

                if captured:
                    break

            cv2.imshow("Capture Face", frame)
            if captured or cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def submit_kyc(self):
        user_id = int(time.time())

        aadhar = self.entries["Aadhaar Number:"].get().strip()
        pan = self.entries["PAN Number:"].get().strip()
        name = self.entries["Name:"].get().strip()
        dob = self.entries["DOB (YYYY-MM-DD):"].get().strip()
        address = self.entries["Address:"].get().strip()

        if not all([aadhar, pan, name, dob, address, self.aadhar_path, self.pan_path, self.captured_face]):
            messagebox.showerror("Error", "All fields and documents are required!")
            return

        if is_duplicate_kyc(aadhar):
            messagebox.showwarning("Duplicate", f"KYC already exists for Aadhaar: {aadhar}")
            return

        try:
            enc_aadhar_file = encrypt_file(self.aadhar_path, aadhar)
            enc_pan_file = encrypt_file(self.pan_path, aadhar)
            enc_face = encrypt_file(self.captured_face, aadhar)

            enc_data = {
                "aadhar_number": cipher.encrypt(aadhar.encode()).decode(),
                "pan_number": cipher.encrypt(pan.encode()).decode(),
                "name": cipher.encrypt(name.encode()).decode(),
                "date_of_birth": cipher.encrypt(dob.encode()).decode(),
                "address": cipher.encrypt(address.encode()).decode(),
            }

            statuses = {
                "bank_verification_status": "Pending ⏳",
                "aadhar_verification_status": "Pending ⏳",
                "pan_verification_status": "Pending ⏳",
                "rbi_verification_status": "Pending ⏳",
            }

            add_block(
                user_id=user_id,
                aadhar_number=enc_data["aadhar_number"],
                user_details=enc_data,
                captured_face_path=enc_face,
                verification_statuses=statuses,
                documents={"aadhar_doc": enc_aadhar_file, "pan_doc": enc_pan_file}
            )

            messagebox.showinfo("✅ Success", "KYC submitted and encrypted to blockchain!")
            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Submission failed: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = KYCApp(root)
    root.mainloop()

