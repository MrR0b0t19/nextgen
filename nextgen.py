from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.live import Live
from time import sleep
from modules import crypter, obfuscator, builder, injector_gen, stager_gen, evasion_gen, defense_bypass, ppid_gen

console = Console()

def show_main_menu():
    console.print(Panel.fit(
        "[bold red]NextGen APT Framework[/bold red]\n"
        "[yellow][1][/yellow] Cifrar shellcode (AES/XOR/AES+XOR)\n"
        "[yellow][2][/yellow] Ofuscar .dat\n"
        "[yellow][3][/yellow] Compilar ejecutable (Windows/Linux)\n"
        "[yellow][4][/yellow] Generar codigo Reflective/Manual Mapping\n"
        "[yellow][5][/yellow] Generar Stager HTTP(S)\n"
        "[yellow][6][/yellow] Tecnicas de evasión avanzadas\n"
        "[yellow][7][/yellow] Generar PPID Spoofing\n"
        "[yellow][8][/yellow] Bypass AMSI/ETW + Anti-Debug\n"
        "[red][0][/red] Salir\n"
        "[red][+][/red] Creator: JaibAM",
        title=" Menu Principal", border_style="bold red"
    ))


def run_with_spinner(task_func, message, success_message):
    with Live(Spinner("dots", text=message), refresh_per_second=10) as live:
        try:
            sleep(0.5)  
            task_func()
            sleep(0.3)  
            live.update("[bold green]+[/bold green] " + success_message)
            print("\n")
            sleep(1.2)
        except Exception as e:
            live.update(f"[bold red]x Error:[/bold red] {e}")
            print("\n")
            sleep(2)
            

def main():
    console.clear()
    while True:
        show_main_menu()
        opt = Prompt.ask("[bold cyan]>> Selecciona una opción[/bold cyan]")
        if opt == "1":
            run_with_spinner(crypter.encrypt_shellcode, "Cifrando shellcode...", "Shellcode cifrado correctamente.")
        elif opt == "2":
            run_with_spinner(obfuscator.obfuscate_dat, "Ofuscando .dat...", ".dat ofuscado correctamente.")
        elif opt == "3":
            run_with_spinner(builder.compile_menu, "Compilando ejecutable...", "Compilación finalizada.")
        elif opt == "4":
            run_with_spinner(injector_gen.generate_injector, "Generando Reflective Loader...", "Plantilla generada.")
        elif opt == "5":
            run_with_spinner(stager_gen.generate_stager, "Generando stager HTTP...", "Stager generado.")
        elif opt == "6":
            run_with_spinner(evasion_gen.generate_evasion_code, "Generando evasión avanzada...", "Plantilla de evasión generada.")
        elif opt == "7":
            run_with_spinner(ppid_gen.generate_ppid_code, "Generando PPID Spoofing...", "Spoofer generado.")
        elif opt == "8":
            run_with_spinner(defense_bypass.generate_bypass_code, "Generando bypass AMSI/ETW...", "Bypass listo.")
        elif opt == "0":
            console.print("[bold red]\n[!] Saliendo...[/bold red]")
            break
        else:
            console.print("[bold yellow][-] Opción inválida[/bold yellow]")

#simple menu, disfruten.
        

if __name__ == "__main__":
    main()
