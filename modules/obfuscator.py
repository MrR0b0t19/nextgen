import os
import random
import json

# Cargar configuraciones desde settings.json
def load_settings():
    with open("config/settings.json", "r") as f:
        return json.load(f)
      
def obfuscate_dat():
    settings = load_settings()
    enc_dir = settings["payload_output_dir"]

    # Buscar archivos .dat para mutar
    files = [f for f in os.listdir(enc_dir) if f.endswith(".dat")]
    if not files:
        print("[-] No hay archivos .dat para mutar en:", enc_dir)
        return

    print("\n[+] Archivos disponibles para mutación:")
    for i, f in enumerate(files):
        print(f"[{i}] {f}")

    index = input("Seleccione archivo .dat: ").strip()
    if not index.isdigit() or int(index) >= len(files):
        print("[-] Selección inválida")
        return

    filename = files[int(index)]
    path = os.path.join(enc_dir, filename)

    with open(path, "rb") as f:
        original = bytearray(f.read())

    # Insertar bytes basura para cada byte real
    mutated = bytearray()
    for byte in original:
        mutated.append(byte)
        for _ in range(random.randint(2, 4)):
            mutated.append(random.randint(0, 255))

    # Guardar archivo ofuscado
    obf_name = filename.replace(".dat", ".obf.dat")
    outpath = os.path.join(enc_dir, obf_name)

    with open(outpath, "wb") as f:
        f.write(mutated)

    print(f"[+] Mutacion completa: {outpath}")
