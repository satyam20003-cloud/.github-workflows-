# receiver_server.py
import socket
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

HOST = "127.0.0.1"
PORT = 9999

# 1. Receiver generates RSA-2048 keypair
rx_priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
rx_pub_key = rx_priv_key.public_key()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[*] Receiver listening on {HOST}:{PORT} ... Ready for wire transfer.")

conn, addr = server_socket.accept()
print(f"[*] Connection accepted from {addr}")

# Receive Encrypted AES Key (256 bytes for RSA-2048)
enc_aes_key = conn.recv(256)

# Receive IV (16 bytes)
iv = conn.recv(16)

# Receive Ciphertext
ciphertext = b""
while True:
    chunk = conn.recv(1024)
    if not chunk:
        break
    ciphertext += chunk

conn.close()
server_socket.close()

# 2. Decrypt AES Key using RSA Private Key
aes_key = rx_priv_key.decrypt(
    enc_aes_key,
    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

# 3. Decrypt Payload using AES-128-CBC
cipher = AES.new(aes_key, AES.MODE_CBC, iv)
decrypted_payload = unpad(cipher.decrypt(ciphertext), 16)
rx_hash = hashlib.sha256(decrypted_payload).hexdigest()

print("[+] Payload received and decrypted successfully!")
print(f"[+] Decrypted Payload Hash: {rx_hash}")
print("[+] Decrypted Content Sample:")
print(decrypted_payload[:180].decode() + "...\n")
