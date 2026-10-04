# sender_client.py
import socket
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import receiver_server  # Borrows Receiver's public key for the demo

HOST = "127.0.0.1"
PORT = 9999

with open("financial_payload.txt", "rb") as f:
    payload = f.read()

# 1. Ephemeral AES-128 session key
aes_key = os.urandom(16)
iv = os.urandom(16)

# 2. Encrypt Payload with AES
cipher = AES.new(aes_key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(payload, 16))

# 3. Encrypt AES Key with Receiver's RSA Public Key
enc_aes_key = receiver_server.rx_pub_key.encrypt(
    aes_key,
    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

# 4. Transmit over Network Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Send: [Encrypted AES Key (256 B)] + [IV (16 B)] + [Ciphertext]
client_socket.sendall(enc_aes_key)
client_socket.sendall(iv)
client_socket.sendall(ciphertext)
client_socket.close()

print("[+] Encrypted financial dispatch sent across network port 9999.")
