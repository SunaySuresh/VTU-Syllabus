from encryption import decrypt_file
decrypted_path = decrypt_file("users/1234-5678-9012/aadhar.jpeg.enc")

if decrypted_path:
    from PIL import Image
    try:
        img = Image.open(decrypted_path)
        img.show()
        print("✅ Decryption and Image Loading Successful!")
    except Exception as e:
        print(f"❌ Image Error: {e}")
