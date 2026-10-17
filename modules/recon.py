import time, ipaddress
from core.config import *
from core.engine import *

def menu():
    while True:
        print(f"\n{R2}{B}  ╔══════════════════════════════════════════╗{E}")
        print(f"  {R2}║{E}  {GD}{B}⚔  RECON MODULE{E}                        {R2}║{E}")
        print(f"  {R2}╠══════════════════════════════════════════╣{E}")
        print(f"  {R2}║{E}  {G2}[1]{E} TCP Port Scan (Top Ports)          {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[2]{E} Full Port Scan (1-65535)           {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[3]{E} Custom Port Range                  {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[4]{E} Service + Banner Detection         {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[5]{E} Ping Sweep (CIDR)                  {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[6]{E} DNS Enumeration                    {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[7]{E} DNS Zone Transfer                  {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[0]{E} Back                               {R2}║{E}")
        print(f"  {R2}╚══════════════════════════════════════════╝{E}")
        c = input(f"\n  {R3}DarkPulse/RECON>{E} ").strip()
        if c == "0": break
        elif c == "1": top_scan()
        elif c == "2": full_scan()
        elif c == "3": custom_scan()
        elif c == "4": banner_scan()
        elif c == "5": ping_sweep()
        elif c == "6": dns_enum()
        elif c == "7": zone_xfer()

def _get_host():
    h = input(f"  {GD}Target IP/Domain:{E} ").strip()
    if not h: print(f"  {R}[-] No target{E}"); return None
    ip = resolve(h)
    if not ip: print(f"  {R}[-] Cannot resolve {h}{E}"); return None
    print(f"  {G}[+] Resolved: {h} → {ip}{E}")
    return h

def top_scan():
    h = _get_host()
    if not h: return
    ports = list(TOP_PORTS.keys())
    print(f"\n  {G2}[*] Scanning {len(ports)} top ports on {h}...{E}")
    t0 = time.time()
    results = mass_scan(h, ports, threads=80)
    elapsed = time.time() - t0
    print(f"\n  {R2}{B}  PORT       STATE    SERVICE{E}")
    print(f"  {D}  {'─'*40}{E}")
    for p in results:
        svc = TOP_PORTS.get(p, "unknown")
        print(f"  {G2}  {p:<10} {R3}OPEN{E}     {G}{svc}{E}")
    print(f"\n  {GD}[+] {len(results)} open ports found in {elapsed:.1f}s{E}")

def full_scan():
    h = _get_host()
    if not h: return
    print(f"\n  {R}[!] Full scan 1-65535 — this takes time{E}")
    confirm = input(f"  {GD}Continue? (y/n):{E} ").strip().lower()
    if confirm != "y": return
    ports = list(range(1, 65536))
    print(f"\n  {G2}[*] Scanning 65535 ports on {h}...{E}")
    t0 = time.time()
    results = mass_scan(h, ports, threads=200, timeout=1)
    elapsed = time.time() - t0
    print(f"\n  {R2}{B}  PORT       STATE    SERVICE{E}")
    print(f"  {D}  {'─'*40}{E}")
    for p in results:
        svc = TOP_PORTS.get(p, "unknown")
        print(f"  {G2}  {p:<10} {R3}OPEN{E}     {G}{svc}{E}")
    print(f"\n  {GD}[+] {len(results)} open ports in {elapsed:.1f}s{E}")

def custom_scan():
    h = _get_host()
    if not h: return
    r = input(f"  {GD}Port range (e.g. 1-1000):{E} ").strip()
    try:
        start, end = map(int, r.split("-"))
        ports = list(range(start, end+1))
    except:
        print(f"  {R}[-] Invalid range{E}"); return
    print(f"\n  {G2}[*] Scanning ports {start}-{end} on {h}...{E}")
    t0 = time.time()
    results = mass_scan(h, ports, threads=150)
    elapsed = time.time() - t0
    print(f"\n  {R2}{B}  PORT       STATE    SERVICE{E}")
    print(f"  {D}  {'─'*40}{E}")
    for p in results:
        svc = TOP_PORTS.get(p, "unknown")
        print(f"  {G2}  {p:<10} {R3}OPEN{E}     {G}{svc}{E}")
    print(f"\n  {GD}[+] {len(results)} open ports in {elapsed:.1f}s{E}")

def banner_scan():
    h = _get_host()
    if not h: return
    ports = list(TOP_PORTS.keys())
    print(f"\n  {G2}[*] Scanning + grabbing banners on {h}...{E}")
    results = mass_scan(h, ports, threads=80)
    if not results:
        print(f"  {R}[-] No open ports{E}"); return
    print(f"\n  {R2}{B}  PORT       SERVICE       BANNER{E}")
    print(f"  {D}  {'─'*65}{E}")
    for p in results:
        svc = TOP_PORTS.get(p, "unknown")
        ban = banner_grab(h, p)
        print(f"  {G2}  {p:<10} {G}{svc:<13} {W}{ban}{E}")

def ping_sweep():
    cidr = input(f"  {GD}CIDR Range (e.g. 192.168.1.0/24):{E} ").strip()
    if not cidr: return
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except:
        print(f"  {R}[-] Invalid CIDR{E}"); return
    hosts = list(net.hosts())
    if len(hosts) > 1024:
        print(f"  {R}[!] {len(hosts)} hosts — limiting to 1024{E}")
        hosts = hosts[:1024]
    print(f"\n  {G2}[*] Pinging {len(hosts)} hosts...{E}")
    alive = []
    from concurrent.futures import ThreadPoolExecutor, as_completed
    with ThreadPoolExecutor(max_workers=100) as ex:
        futs = {ex.submit(ping_host, str(ip)): str(ip) for ip in hosts}
        for f in as_completed(futs):
            ip = futs[f]
            if f.result():
                alive.append(ip)
                rdns = reverse_dns(ip) or ""
                print(f"  {G2}[+] {R3}ALIVE{E}  {G}{ip:<18} {D}{rdns}{E}")
    print(f"\n  {GD}[+] {len(alive)} hosts alive{E}")

def dns_enum():
    domain = input(f"  {GD}Target Domain:{E} ").strip()
    if not domain: return
    print(f"\n  {G2}[*] Enumerating subdomains for {domain}...{E}")
    found = []
    from concurrent.futures import ThreadPoolExecutor, as_completed
    def _check(sub):
        fqdn = f"{sub}.{domain}"
        ip = resolve(fqdn)
        if ip:
            return fqdn, ip
        return None
    with ThreadPoolExecutor(max_workers=50) as ex:
        futs = {ex.submit(_check, s): s for s in SUBDOMAINS}
        for f in as_completed(futs):
            r = f.result()
            if r:
                found.append(r)
                print(f"  {G2}[+] {R3}FOUND{E}  {G}{r[0]:<35} {W}{r[1]}{E}")
    print(f"\n  {GD}[+] {len(found)} subdomains found{E}")

def zone_xfer():
    domain = input(f"  {GD}Target Domain:{E} ").strip()
    if not domain: return
    ns = input(f"  {GD}Nameserver (leave blank for auto):{E} ").strip() or None
    print(f"\n  {G2}[*] Attempting zone transfer for {domain}...{E}")
    result = zone_transfer(domain, ns)
    if result:
        print(f"  {R2}[!!!] ZONE TRANSFER SUCCESSFUL!{E}")
        print(f"  {G}{result[:1000]}{E}")
    else:
        print(f"  {D}[-] Zone transfer refused (AXFR blocked){E}")
