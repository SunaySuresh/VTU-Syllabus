'''import tkinter as tk
from tkinter import messagebox
import json
import hashlib

BLOCKCHAIN_FILE = "blockchain_data.json"

def calculate_hash(block):
    # Copy block and remove "hash" field before hashing
    block_copy = json.loads(json.dumps(block))  # Deep copy
    block_copy["hash"] = ""
    block_string = json.dumps(block_copy, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def load_blockchain():
    try:
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Blockchain file not found.")
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error decoding blockchain file.")
        return []

def is_block_tampered(block):
    return block["hash"] != calculate_hash(block)

def visualize_blockchain():
    blockchain = load_blockchain()
    if not blockchain:
        return

    root = tk.Tk()
    root.title("Blockchain Visualizer")
    canvas = tk.Canvas(root, width=1800, height=900, bg="white")
    canvas.pack()

    x, y = 100, 100
    box_width, box_height = 300, 160
    space_x = 60

    for i, block in enumerate(blockchain):
        header = block.get("header", {})
        block_text = (
            f"Block #{i + 1}\n"
            f"Aadhaar: {header.get('aadhar_number', '')}\n"
            f"User ID: {header.get('user_id', '')}\n"
            f"Bank Status: {block.get('bank_verification_status', 'N/A')}\n"
            f"Aadhaar Status: {block.get('aadhar_verification_status', 'N/A')}\n"
            f"PAN Status: {block.get('pan_verification_status', 'N/A')}\n"
            f"RBI Status: {block.get('rbi_verification_status', 'N/A')}\n"
        )

        tampered = is_block_tampered(block)
        color = "red" if tampered else "lightgreen"

        # Draw block
        canvas.create_rectangle(x, y, x + box_width, y + box_height, fill=color, outline="black")
        canvas.create_text(x + 10, y + 10, anchor="nw", text=block_text, font=("Courier", 10), fill="black")

        # Draw line from previous block
        if i > 0:
            prev_block = blockchain[i - 1]
            expected_prev_hash = block["header"].get("prev_hash")
            actual_prev_hash = prev_block["hash"]

            if expected_prev_hash == actual_prev_hash:
                canvas.create_line(x - space_x, y + box_height / 2, x, y + box_height / 2, arrow=tk.LAST, width=2)
            else:
                canvas.create_text(x - space_x, y + box_height / 2 - 15, text="❌ Broken Link", fill="red", font=("Arial", 10, "bold"))

        x += box_width + space_x
        if x + box_width > canvas.winfo_reqwidth() - 100:
            x = 100
            y += box_height + 100

    root.mainloop()

if __name__ == "__main__":
    visualize_blockchain()'''


import tkinter as tk
from tkinter import messagebox
import json
import hashlib
from encryption import decrypt_text

BLOCKCHAIN_FILE = "blockchain_data.json"

def calculate_hash(block):
    block_copy = json.loads(json.dumps(block))
    block_copy["hash"] = ""
    block_string = json.dumps(block_copy, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def load_blockchain():
    try:
        with open(BLOCKCHAIN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Blockchain file not found.")
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error decoding blockchain file.")
        return []

def is_block_tampered(block):
    return block["hash"] != calculate_hash(block)

def visualize_blockchain():
    blockchain = load_blockchain()
    if not blockchain:
        return

    root = tk.Tk()
    root.title("Blockchain Visualizer")

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = tk.Frame(main_frame, width=300, bg="#eeeeee")
    right_frame.pack(side="right", fill="y")

    title_label = tk.Label(right_frame, text="Tampered Blocks", font=("Arial", 14, "bold"), bg="#eeeeee")
    title_label.pack(pady=10)

    tampered_listbox = tk.Listbox(right_frame, font=("Arial", 12))
    tampered_listbox.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(left_frame, bg="#f0f0f0")
    scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Block sizes
    block_width, block_height = 400, 180
    margin_x, margin_y = 50, 50
    space_y = 100

    x = margin_x
    y = margin_y

    block_centers = []
    tampered_blocks = []

    block_tampered_flags = []

    for i, block in enumerate(blockchain):
        header = block.get("header", {})

        encrypted_aadhar = header.get('aadhar_number', '')
        try:
            decrypted_aadhar = decrypt_text(encrypted_aadhar)
        except:
            decrypted_aadhar = "(Decryption Failed)"

        bank_status = block.get('bank_verification_status', 'N/A')
        aadhar_status = block.get('aadhar_verification_status', 'N/A')
        pan_status = block.get('pan_verification_status', 'N/A')
        rbi_status = block.get('rbi_verification_status', 'N/A')

        def format_status(status):
            return f"{status} ⏳" if status == "Pending" else f"{status}"

        tampered = is_block_tampered(block)

        broken_link = False
        if i > 0:
            prev_block = blockchain[i-1]
            expected_prev_hash = header.get('prev_hash')
            actual_prev_hash = prev_block["hash"]
            if expected_prev_hash != actual_prev_hash:
                broken_link = True

        this_block_tampered = tampered or broken_link
        block_tampered_flags.append(this_block_tampered)

        if this_block_tampered:
            tampered_blocks.append(i + 1)

        color = "#ff9999" if this_block_tampered else "#ccffcc"

        frame = tk.Frame(canvas, width=block_width, height=block_height, bg=color, highlightbackground="black", highlightthickness=2)
        frame.pack_propagate(False)

        label_text = (
            f"Block #{i + 1}\n\n"
            f"Aadhaar: {decrypted_aadhar}\n"
            f"User ID: {header.get('user_id', 'N/A')}\n\n"
            f"Bank: {format_status(bank_status)}\n"
            f"Aadhaar: {format_status(aadhar_status)}\n"
            f"PAN: {format_status(pan_status)}\n"
            f"RBI: {format_status(rbi_status)}"
        )

        label = tk.Label(frame, text=label_text, bg=color, font=("Courier New", 10), justify="left")
        label.pack(fill="both", expand=True)

        canvas.create_window(x, y, window=frame, anchor="nw")

        center_x = x + block_width // 2
        center_y = y + block_height
        block_centers.append((center_x, center_y))

        y += block_height + space_y

    # Draw arrows
    arrow_ids = []
    arrow_colors = []

    for i in range(len(block_centers) - 1):
        x1, y1 = block_centers[i]
        x2, y2 = block_centers[i + 1]

        # If current or next block is tampered => break link
        if block_tampered_flags[i] or block_tampered_flags[i+1]:
            arrow_ids.append(None)
            arrow_colors.append(None)
            continue

        arrow = canvas.create_line(x1, y1, x2, y2 - block_height + 20, arrow=tk.LAST, width=2, fill="black")
        arrow_ids.append(arrow)
        arrow_colors.append("black")

    # Animation
    def animate_arrows():
        for idx, arrow in enumerate(arrow_ids):
            if arrow is None:
                continue
            current_color = canvas.itemcget(arrow, 'fill')
            new_color = "blue" if current_color == "black" else "black"
            canvas.itemconfig(arrow, fill=new_color)
        root.after(500, animate_arrows)

    animate_arrows()

    # Update right side tampered list
    if tampered_blocks:
        for blk_no in tampered_blocks:
            tampered_listbox.insert(tk.END, f"Block #{blk_no} Tampered!")
    else:
        tampered_listbox.insert(tk.END, "All Blocks are Valid ✅")

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'))

    root.mainloop()

if __name__ == "__main__":
    visualize_blockchain()

