import os, sys, time, random, threading

CHARS = "─☸❖♡★ᏦᎥᏁᎶ👑⏤01"
G = "\033[38;5;28m"
G2 = "\033[38;5;34m"
G3 = "\033[38;5;82m"
R = "\033[38;5;88m"
R2 = "\033[38;5;160m"
R3 = "\033[38;5;196m"
RD = "\033[38;5;124m"
GD = "\033[38;5;220m"
W = "\033[97m"
D = "\033[90m"
B = "\033[1m"
E = "\033[0m"

stop_rain = False

def rain():
    cols = os.get_terminal_size().columns if sys.stdout.isatty() else 60
    while not stop_rain:
        line = ""
        for _ in range(cols):
            if random.random() < 0.3:
                c = random.choice(CHARS)
                line += random.choice([G, G2, R, RD]) + c
            else:
                line += " "
        sys.stdout.write(f"\r{line}{E}")
        sys.stdout.flush()
        time.sleep(0.06)

def show():
    global stop_rain
    t = threading.Thread(target=rain, daemon=True)
    t.start()
    time.sleep(0.8)
    stop_rain = True
    t.join(timeout=0.2)
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()
    os.system("clear" if os.name != "nt" else "cls")
    
    logo = f"""
{R3}{B}
    ██████╗  █████╗ ██████╗ ██╗  ██╗██████╗ ██╗   ██╗██╗     ███████╗███████╗
    ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██║   ██║██║     ██╔════╝██╔════╝
    ██║  ██║███████║██████╔╝█████╔╝ ██████╔╝██║   ██║██║     ███████╗█████╗  
    ██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔═══╝ ██║   ██║██║     ╚════██║██╔══╝  
    ██████╔╝██║  ██║██║  ██║██║  ██╗██║     ╚██████╔╝███████╗███████║███████╗
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝
{E}"""
    for line in logo.split("\n"):
        print(line)
        time.sleep(0.05)
    
    print(f"\n{R2}    ════════════════════════════════════════════════════════════════{E}")
    print(f"    {R3}{B}☸ ADVANCED OFFENSIVE SECURITY FRAMEWORK v1.0 ☸{E}")
    print(f"    {G2}  ─── Port Scan ─ SQLi ─ XSS ─ BruteForce ─ Payloads ─ Exploit ───{E}")
    print(f"{R2}    ════════════════════════════════════════════════════════════════{E}")
    print(f"\n    {GD}{B}👑 Developer : https://github.com/anonmoty 👑{E}")
    print(f"    {G}  ⚔  Type   : Offensive Penetration Testing{E}")
    print(f"    {G}  🛡  Use    : Authorized Security Testing Only{E}")
    print(f"    {D}  ─────────────────────────────────────────────{E}")
    
    info = [
        ("RECON", "Port Scan • Banner Grab • Ping Sweep • DNS Enum"),
        ("WEBATTACK", "SQLi • XSS • LFI • Command Injection"),
        ("BRUTE", "Hash Crack • Dir Bruteforce • Login Bruteforce"),
        ("PAYLOAD", "Reverse Shells • Web Shells • Encoders"),
        ("EXPLOIT", "Header Inject • Open Redirect • CORS • Takeover"),
    ]
    print()
    for name, desc in info:
        print(f"    {R3}[{name}]{E} {G2}{desc}{E}")
    print()
    
    for i in range(30):
        c = random.choice(CHARS)
        color = random.choice([G, G2, R, RD, GD])
        sys.stdout.write(f"{color}{c}{E}")
        sys.stdout.flush()
        time.sleep(0.02)
    print(f"\n{E}")
