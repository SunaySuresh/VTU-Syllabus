'''import json
import hashlib
import time

BLOCKCHAIN_FILE = "blockchain_data.json"

def calculate_hash(block):
    """Calculate SHA-256 hash of a block."""
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def load_blockchain():
    """Load blockchain from file or create a new one."""
    try:
        with open(BLOCKCHAIN_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_blockchain(blockchain):
    """Save blockchain to file."""
    with open(BLOCKCHAIN_FILE, "w") as file:
        json.dump(blockchain, file, indent=4)

def update_status_on_rejection(verification_statuses):
    """If any verification is rejected, mark all pending as rejected."""
    if "Rejected ❌" in verification_statuses.values():
        for key in verification_statuses:
            if verification_statuses[key] == "Pending ⏳":
                verification_statuses[key] = "Rejected ❌"
    return verification_statuses

def add_block(user_id, aadhar_number, captured_face_path, verification_statuses, documents):
    """Add a new verification block to the blockchain."""
    blockchain = load_blockchain()
    prev_hash = blockchain[-1]["hash"] if blockchain else "0"
    timestamp = int(time.time())

    # Ensure verification statuses follow the rejection rules
    verification_statuses = update_status_on_rejection(verification_statuses)

    new_block = {
        "header": {
            "user_id": user_id,
            "aadhar_number": aadhar_number,
            "captured_face_path": captured_face_path,
            "aadhar_doc": documents.get("aadhar_doc"),
            "pan_doc": documents.get("pan_doc"),
            "timestamp": timestamp,
            "prev_hash": prev_hash
        },
        "bank_verification_status": verification_statuses["bank_verification_status"],
        "aadhar_verification_status": verification_statuses["aadhar_verification_status"],
        "pan_verification_status": verification_statuses["pan_verification_status"],
        "rbi_verification_status": verification_statuses["rbi_verification_status"],
        "hash": ""
    }
    
    new_block["hash"] = calculate_hash(new_block)
    blockchain.append(new_block)
    save_blockchain(blockchain)
    return new_block
'''


'Adding blockchain integrity'
'''import json
import hashlib
import time
import os

BLOCKCHAIN_FILE = "blockchain_data.json"

def calculate_hash(block):
    block_copy = block.copy()
    block_copy["hash"] = ""  # Exclude hash field for consistent hashing
    block_string = json.dumps(block_copy, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def load_blockchain():
    try:
        with open(BLOCKCHAIN_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_blockchain(blockchain):
    with open(BLOCKCHAIN_FILE, "w") as file:
        json.dump(blockchain, file, indent=4)

def update_status_on_rejection(verification_statuses):
    if "Rejected ❌" in verification_statuses.values():
        for key in verification_statuses:
            if verification_statuses[key] == "Pending ⏳":
                verification_statuses[key] = "Rejected ❌"
    return verification_statuses

def add_block(user_id, aadhar_number, captured_face_path, verification_statuses, documents):
    blockchain = load_blockchain()
    prev_hash = blockchain[-1]["hash"] if blockchain else "0"
    timestamp = int(time.time())

    verification_statuses = update_status_on_rejection(verification_statuses)

    new_block = {
        "header": {
            "user_id": user_id,
            "aadhar_number": aadhar_number,
            "captured_face_path": captured_face_path,
            "aadhar_doc": documents.get("aadhar_doc"),
            "pan_doc": documents.get("pan_doc"),
            "timestamp": timestamp,
            "prev_hash": prev_hash
        },
        "bank_verification_status": verification_statuses["bank_verification_status"],
        "aadhar_verification_status": verification_statuses["aadhar_verification_status"],
        "pan_verification_status": verification_statuses["pan_verification_status"],
        "rbi_verification_status": verification_statuses["rbi_verification_status"],
        "hash": ""
    }

    new_block["hash"] = calculate_hash(new_block)
    blockchain.append(new_block)
    save_blockchain(blockchain)
    return new_block'''

'''def verify_blockchain_integrity():
    blockchain = load_blockchain()
    for i in range(len(blockchain)):
        current_block = blockchain[i]
        recalculated_hash = calculate_hash(current_block)
        if current_block["hash"] != recalculated_hash:
            return f"[ALERT] Tampering detected in block {i}!"
        if i > 0 and current_block["header"]["prev_hash"] != blockchain[i - 1]["hash"]:
            return f"[ALERT] Broken link between block {i-1} and {i}!"
    return "[SUCCESS] Blockchain integrity verified. No tampering detected."

'''

'''def verify_blockchain_integrity():
    blockchain = load_blockchain()

    for i in range(len(blockchain)):
        current_block = blockchain[i]
        original_hash = current_block["hash"]

        # Temporarily remove the hash to recalculate
        block_copy = current_block.copy()
        block_copy["hash"] = ""

        recalculated_hash = calculate_hash(block_copy)

        if original_hash != recalculated_hash:
            # Find exact changes (field-level)
            stored_data = json.loads(json.dumps(block_copy))  # Deep copy
            recalculated_data = json.loads(json.dumps(block_copy))  # For clarity

            changed_fields = []

            # Compare all keys and values recursively
            def compare_dicts(dict1, dict2, path=""):
                for key in dict1:
                    full_path = f"{path}.{key}" if path else key
                    if key not in dict2:
                        changed_fields.append(f"{full_path} removed")
                    elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                        compare_dicts(dict1[key], dict2[key], full_path)
                    elif dict1[key] != dict2[key]:
                        changed_fields.append(f"{full_path} was changed")

            compare_dicts(block_copy, current_block)

            user_id = current_block["header"].get("user_id", "Unknown")
            aadhar = current_block["header"].get("aadhar_number", "Unknown")

            return f"""⚠️ Blockchain Tampering Detected!
User ID: {user_id}
Aadhaar Number: {aadhar}
Tampered Fields:
- """ + "\n- ".join(changed_fields)

        if i > 0 and current_block["header"]["prev_hash"] != blockchain[i - 1]["hash"]:
            prev_user_id = blockchain[i - 1]["header"].get("user_id", "Unknown")
            curr_user_id = current_block["header"].get("user_id", "Unknown")
            return f"""🔗 Broken Chain Link Detected!
Between User ID {prev_user_id} and {curr_user_id}
Block #{i-1} and #{i}
"""

    return "[SUCCESS] Blockchain integrity verified. No tampering detected."
'''



'''This one works'''
'''import json
import hashlib
import time

BLOCKCHAIN_FILE = "blockchain_data.json"

def is_duplicate_kyc(aadhar_number):
    with open("blockchain_data.json", "r") as f:
        chain = json.load(f)

    for block in chain:
        if block["header"]["aadhar_number"] == aadhar_number:
            #status = block["header"].get("status", "").lower()
            #if status in ["pending ", "approved", "rejected"]:
                return True
    return False


def calculate_hash(block):
    """Calculate SHA-256 hash of a block."""
    temp_block = dict(block)
    temp_block["hash"] = ""
    block_string = json.dumps(temp_block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def load_blockchain():
    """Load blockchain from file or create a new one."""
    try:
        with open(BLOCKCHAIN_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_blockchain(blockchain):
    """Save blockchain to file."""
    with open(BLOCKCHAIN_FILE, "w") as file:
        json.dump(blockchain, file, indent=4)

def update_status_on_rejection(verification_statuses):
    """If any verification is rejected, mark all pending as rejected."""
    if "Rejected ❌" in verification_statuses.values():
        for key in verification_statuses:
            if verification_statuses[key] == "Pending ⏳":
                verification_statuses[key] = "Rejected ❌"
    return verification_statuses

def add_block(user_id, aadhar_number, captured_face_path, verification_statuses, documents):
    """Add a new verification block to the blockchain."""
    blockchain = load_blockchain()
    prev_hash = blockchain[-1]["hash"] if blockchain else "0"
    timestamp = int(time.time())

    verification_statuses = update_status_on_rejection(verification_statuses)

    new_block = {
        "header": {
            "user_id": user_id,
            "aadhar_number": aadhar_number,
            "captured_face_path": captured_face_path,
            "aadhar_doc": documents.get("aadhar_doc"),
            "pan_doc": documents.get("pan_doc"),
            "timestamp": timestamp,
            "prev_hash": prev_hash
        },
        "bank_verification_status": verification_statuses["bank_verification_status"],
        "aadhar_verification_status": verification_statuses["aadhar_verification_status"],
        "pan_verification_status": verification_statuses["pan_verification_status"],
        "rbi_verification_status": verification_statuses["rbi_verification_status"],
        "hash": ""
    }

    new_block["hash"] = calculate_hash(new_block)
    blockchain.append(new_block)
    save_blockchain(blockchain)
    return new_block

def verify_blockchain_integrity():
    blockchain = load_blockchain()

    for i in range(len(blockchain)):
        current_block = blockchain[i]
        original_hash = current_block["hash"]

        # Temporarily remove the hash to recalculate
        block_copy = current_block.copy()
        block_copy["hash"] = ""

        recalculated_hash = calculate_hash(block_copy)

        if original_hash != recalculated_hash:
            # Find exact changes (field-level)
            stored_data = json.loads(json.dumps(block_copy))  # Deep copy
            recalculated_data = json.loads(json.dumps(block_copy))  # For clarity

            changed_fields = []

            # Compare all keys and values recursively
            def compare_dicts(dict1, dict2, path=""):
                for key in dict1:
                    full_path = f"{path}.{key}" if path else key
                    if key not in dict2:
                        changed_fields.append(f"{full_path} removed")
                    elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                        compare_dicts(dict1[key], dict2[key], full_path)
                    elif dict1[key] != dict2[key]:
                        changed_fields.append(f"{full_path} was changed")

            compare_dicts(block_copy, current_block)

            user_id = current_block["header"].get("user_id", "Unknown")
            aadhar = current_block["header"].get("aadhar_number", "Unknown")

            return f"""⚠️ Blockchain Tampering Detected!
User ID: {user_id}
Aadhaar Number: {aadhar}
Tampered Fields:
- """ + "\n- ".join(changed_fields)

        if i > 0 and current_block["header"]["prev_hash"] != blockchain[i - 1]["hash"]:
            prev_user_id = blockchain[i - 1]["header"].get("user_id", "Unknown")
            curr_user_id = current_block["header"].get("user_id", "Unknown")
            return f"""🔗 Broken Chain Link Detected!
Between User ID {prev_user_id} and {curr_user_id}
Block #{i-1} and #{i}
"""

    return "[SUCCESS] Blockchain integrity verified. No tampering detected." '''


'''Adding other details'''
import json
import hashlib
import time
import os

BLOCKCHAIN_FILE = "blockchain_data.json"

def is_duplicate_kyc(aadhar_number):
    if not os.path.exists(BLOCKCHAIN_FILE):
        return False

    with open(BLOCKCHAIN_FILE, "r") as f:
        chain = json.load(f)

    for block in chain:
        if block["header"]["aadhar_number"] == aadhar_number:
            return True
    return False

def calculate_hash(block):
    """Calculate SHA-256 hash of a block."""
    temp_block = dict(block)
    temp_block["hash"] = ""
    block_string = json.dumps(temp_block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def load_blockchain():
    """Load blockchain from file or create a new one."""
    try:
        with open(BLOCKCHAIN_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_blockchain(blockchain):
    """Save blockchain to file."""
    with open(BLOCKCHAIN_FILE, "w") as file:
        json.dump(blockchain, file, indent=4)

def update_status_on_rejection(verification_statuses):
    """If any verification is rejected, mark all pending as rejected."""
    if "Rejected ❌" in verification_statuses.values():
        for key in verification_statuses:
            if verification_statuses[key] == "Pending ⏳":
                verification_statuses[key] = "Rejected ❌"
    return verification_statuses

def add_block(user_id, aadhar_number, captured_face_path, verification_statuses, documents, user_details):
    """
    Add a new verification block to the blockchain.

    user_details: dict with keys - name, pan_number, date_of_birth, address
    """
    blockchain = load_blockchain()
    prev_hash = blockchain[-1]["hash"] if blockchain else "0"
    timestamp = int(time.time())

    verification_statuses = update_status_on_rejection(verification_statuses)

    new_block = {
        "header": {
            "user_id": user_id,
            "aadhar_number": aadhar_number,
            "captured_face_path": captured_face_path,
            "aadhar_doc": documents.get("aadhar_doc"),
            "pan_doc": documents.get("pan_doc"),
            "name": user_details.get("name"),
            "pan_number": user_details.get("pan_number"),
            "date_of_birth": user_details.get("date_of_birth"),
            "address": user_details.get("address"),
            "timestamp": timestamp,
            "prev_hash": prev_hash
        },
        "bank_verification_status": verification_statuses["bank_verification_status"],
        "aadhar_verification_status": verification_statuses["aadhar_verification_status"],
        "pan_verification_status": verification_statuses["pan_verification_status"],
        "rbi_verification_status": verification_statuses["rbi_verification_status"],
        "hash": ""
    }

    new_block["hash"] = calculate_hash(new_block)
    blockchain.append(new_block)
    save_blockchain(blockchain)
    return new_block

def verify_blockchain_integrity():
    blockchain = load_blockchain()

    for i in range(len(blockchain)):
        current_block = blockchain[i]
        original_hash = current_block["hash"]

        block_copy = current_block.copy()
        block_copy["hash"] = ""

        recalculated_hash = calculate_hash(block_copy)

        if original_hash != recalculated_hash:
            changed_fields = []

            def compare_dicts(dict1, dict2, path=""):
                for key in dict1:
                    full_path = f"{path}.{key}" if path else key
                    if key not in dict2:
                        changed_fields.append(f"{full_path} removed")
                    elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                        compare_dicts(dict1[key], dict2[key], full_path)
                    elif dict1[key] != dict2[key]:
                        changed_fields.append(f"{full_path} was changed")

            compare_dicts(block_copy, current_block)

            user_id = current_block["header"].get("user_id", "Unknown")
            aadhar = current_block["header"].get("aadhar_number", "Unknown")

            return f"""⚠️ Blockchain Tampering Detected!
User ID: {user_id}
Aadhaar Number: {aadhar}
Tampered Fields:
- """ + "\n- ".join(changed_fields)

        if i > 0 and current_block["header"]["prev_hash"] != blockchain[i - 1]["hash"]:
            prev_user_id = blockchain[i - 1]["header"].get("user_id", "Unknown")
            curr_user_id = current_block["header"].get("user_id", "Unknown")
            return f"""🔗 Broken Chain Link Detected!
Between User ID {prev_user_id} and {curr_user_id}
Block #{i-1} and #{i}
"""

    return "[SUCCESS] Blockchain integrity verified. No tampering detected."
