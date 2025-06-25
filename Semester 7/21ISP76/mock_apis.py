'''valid_aadhar_numbers = {"1234-5678-9012", "1111-2222-3333"}
linked_pan_numbers = {"1234-5678-9012": "ABCDE1234F","1111-2222-3333":"FGHIJ5678G"}

def verify_aadhar(aadhar_number):
    """ Simulates Aadhaar verification (checks if Aadhaar exists). """
    return aadhar_number in valid_aadhar_numbers

def verify_pan(aadhar_number):
    """ Simulates PAN verification (checks if Aadhaar is linked to PAN). """
    return aadhar_number in linked_pan_numbers

def verify_rbi(user_id):
    """ Simulates RBI blacklist check (all users are approved for simplicity). """
    return True'''



# mock_apis.py

# Simulated Aadhaar database
valid_aadhar_numbers = {
    "1234-5678-9012": {"name": "Ravi Kumar", "dob": "1990-05-15"},
    "1111-2222-3333": {"name": "Anita Sharma", "dob": "1985-11-20"},
    "9999-8888-7777": {"name": "Suresh Menon", "dob": "1992-03-12"},
    "4444-5555-6666": {"name": "Nikita Verma", "dob": "1998-01-07"},
    "0000-1111-2222": {"name": "Ajay Singh", "dob": "1975-09-09"},
    "8804-5364-2828": {"name": "S KARTHIK", "dob": "2003-04-08"}
}

# PAN linkage with Aadhaar (simulate missing link or invalid PAN)
linked_pan_numbers = {
    "1234-5678-9012": "ABCDE1234F",
    "1111-2222-3333": "FGHIJ5678G",
    "9999-8888-7777": "PLMNO4321Z",
    "8804-5364-2828": "ASDFG8804H",
    #"0000-1111-2222": "INVALIDPAN"  # Simulated incorrect format or forged PAN
}

# RBI blacklist (by Aadhaar number)
rbi_blacklisted_aadhar_numbers = {
    "4444-5555-6666",
    "0000-1111-2222"
}


def verify_aadhar(aadhar_number):
    """
    Simulates Aadhaar verification by checking if the Aadhaar number exists.
    Returns a tuple (status: bool, message: str)
    """
    if aadhar_number in valid_aadhar_numbers:
        return True, "✅ Aadhaar number is valid."
    else:
        return False, "❌ Aadhaar number not found."


def verify_pan(aadhar_number):
    """
    Simulates PAN verification.
    Returns a tuple (status: bool, message: str)
    """
    if aadhar_number not in valid_aadhar_numbers:
        return False, "❌ Aadhaar number does not exist. Cannot verify PAN."

    if aadhar_number not in linked_pan_numbers:
        return False, "⚠️ Aadhaar is not linked to any PAN."

    pan = linked_pan_numbers[aadhar_number]
    if len(pan) != 10 or not pan[:5].isalpha() or not pan[5:9].isdigit() or not pan[9].isalpha():
        return False, f"❌ PAN '{pan}' appears to be invalid or forged."

    return True, f"✅ PAN '{pan}' is valid and linked."


def verify_rbi(aadhar_number):
    """
    Simulates RBI blacklist check using Aadhaar number.
    Returns a tuple (status: bool, message: str)
    """
    if aadhar_number in rbi_blacklisted_aadhar_numbers:
        return False, f"⛔ Aadhaar {aadhar_number} is blacklisted by RBI."
    return True, f"✅ Aadhaar {aadhar_number} is clear as per RBI records."


# For direct testing
if __name__ == "__main__":
    print(verify_aadhar("1234-5678-9012"))
    print(verify_pan("9999-8888-7777"))
    print(verify_rbi("4444-5555-6666"))
    print(verify_rbi("1234-5678-9012"))

