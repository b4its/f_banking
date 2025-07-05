from cryptography.fernet import Fernet
import base64
import hashlib

# Fungsi untuk membuat key berdasarkan nik + kk
def generate_key(nik: str, kk: str) -> bytes:
    # Buat key dari kombinasi nik + kk
    raw_key = f"{nik}{kk}".encode()
    hashed = hashlib.sha256(raw_key).digest()
    return base64.urlsafe_b64encode(hashed)

# Fungsi enkripsi data
def encrypt_data(nik, kk, sim, npwp, paspor, id_value):
    key = generate_key(nik, kk)
    fernet = Fernet(key)
    combined_data = f"{nik}|{kk}|{sim}|{npwp}|{paspor}|{id_value}"
    encrypted = fernet.encrypt(combined_data.encode())
    return encrypted

# Fungsi dekripsi data
def decrypt_data(encrypted_data, nik, kk):
    key = generate_key(nik, kk)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data).decode()
    return decrypted  # format: nik|kk|sim|npwp|paspor|id

# cara penggunaan
# encrypted = cryptographyAlgorithm.encrypt_data(112,211,404,505,404,11)
# decrypted = cryptographyAlgorithm.decrypt_data(encrypted, form_nik, form_kk)
# print("Hasil Dekripsi:", decrypted)