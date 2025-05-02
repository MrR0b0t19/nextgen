import os
import json

def load_settings():
    with open("config/settings.json", "r") as f:
        return json.load(f)

def compile_menu():
    settings = load_settings()
    out_dir = settings["executable_output_dir"]
    os.makedirs(out_dir, exist_ok=True)

    print("\n[+] Seleccione plataforma de compilacion:")
    print("[1] Windows (.exe)")
    print("[2] Linux (ELF)")
    opt = input(">> ").strip()

    if opt == "1":
        compiler = settings["compiler_windows"]
        cmd = f"{compiler} core/loader.c core/menu.c -o {out_dir}/nextgen_loader.exe -mwindows -O2"
    elif opt == "2":
        compiler = settings["compiler_linux"]
        cmd = f"{compiler} linux/nextgen_loader.c -o {out_dir}/nextgen_loader -O2"
    else:
        print("[-] Opcion invalida")
        return

    print(f"[+] Ejecutando compilacion:\n{cmd}")
    result = os.system(cmd)
    if result == 0:
        print("[+] Compilacion exitosa")
    else:
        print("[-] Error durante la compilacion")
