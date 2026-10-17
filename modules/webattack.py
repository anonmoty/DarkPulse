import time, re, urllib.parse
from core.config import *
from core.engine import *

def menu():
    while True:
        print(f"\n{R2}{B}  ╔══════════════════════════════════════════╗{E}")
        print(f"  {R2}║{E}  {R3}{B}💉 WEBATTACK MODULE{E}                     {R2}║{E}")
        print(f"  {R2}╠══════════════════════════════════════════╣{E}")
        print(f"  {R2}║{E}  {G2}[1]{E} SQL Injection Scanner              {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[2]{E} XSS Reflected Scanner              {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[3]{E} LFI / Path Traversal               {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[4]{E} Command Injection                  {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[5]{E} Full Web Vuln Scan (All)           {R2}║{E}")
        print(f"  {R2}║{E}  {G2}[0]{E} Back                               {R2}║{E}")
        print(f"  {R2}╚══════════════════════════════════════════╝{E}")
        c = input(f"\n  {R3}DarkPulse/WEB>{E} ").strip()
        if c == "0": break
        elif c == "1": sqli_scan()
        elif c == "2": xss_scan()
        elif c == "3": lfi_scan()
        elif c == "4": cmdi_scan()
        elif c == "5": full_scan()

def _get_url():
    u = input(f"  {GD}Target URL (with params):{E} ").strip()
    if not u: print(f"  {R}[-] No URL{E}"); return None
    if "?" not in u:
        print(f"  {D}[!] No parameters found. Add ?id=1 etc.{E}")
    return u

def sqli_scan():
    url = _get_url()
    if not url: return
    params = extract_params(url)
    if not params:
        print(f"  {R}[-] No parameters to test{E}"); return
    print(f"\n  {G2}[*] Testing {len(params)} params with {len(SQLI_PAYLOADS)} SQLi payloads...{E}")
    vulns = []
    for param in params:
        print(f"\n  {GD}[→] Parameter: {param}{E}")
        for payload in SQLI_PAYLOADS:
            test_url = build_url_with_param(url, param, payload)
            r = http_get(test_url, timeout=6)
            if r["error"] and "timed out" in str(r["error"]).lower():
                if "SLEEP" in payload or "WAITFOR" in payload:
                    print(f"  {R2}  [!!!] VULNERABLE (Time-Based): {payload}{E}")
                    vulns.append(("Time-Based SQLi", param, payload))
                continue
            body_lower = r["body"].lower()
            for sig in SQL_ERRORS:
                if sig.lower() in body_lower:
                    print(f"  {R2}  [!!!] VULNERABLE (Error-Based): {payload}{E}")
                    print(f"  {R}       Signature: {sig}{E}")
                    vulns.append(("Error-Based SQLi", param, payload))
                    break
            else:
                if r["code"] == 200 and len(r["body"]) > 100:
                    clean = http_get(build_url_with_param(url, param, "1"), timeout=5)
                    if clean["code"] == 200 and abs(len(r["body"]) - len(clean["body"])) > 500:
                        if "OR" in payload or "AND" in payload:
                            print(f"  {RD}  [!] Possible Boolean SQLi: {payload}{E}")
                            vulns.append(("Boolean SQLi?", param, payload))
    _report("SQL Injection", vulns)

def xss_scan():
    url = _get_url()
    if not url: return
    params = extract_params(url)
    if not params:
        print(f"  {R}[-] No parameters{E}"); return
    print(f"\n  {G2}[*] Testing {len(params)} params with {len(XSS_PAYLOADS)} XSS payloads...{E}")
    vulns = []
    for param in params:
        print(f"\n  {GD}[→] Parameter: {param}{E}")
        for payload in XSS_PAYLOADS:
            test_url = build_url_with_param(url, param, payload)
            r = http_get(test_url, timeout=6)
            if r["code"] == 0: continue
            if payload in r["body"]:
                print(f"  {R2}  [!!!] REFLECTED XSS: {payload}{E}")
                vulns.append(("Reflected XSS", param, payload))
            else:
                encoded = urllib.parse.quote(payload)
                if encoded in r["body"] and "<" not in r["body"].split(encoded)[0][-5:]:
                    print(f"  {RD}  [!] Possible Stored/Encoded XSS: {payload}{E}")
    _report("XSS", vulns)

def lfi_scan():
    url = _get_url()
    if not url: return
    params = extract_params(url)
    if not params:
        print(f"  {R}[-] No parameters{E}"); return
    print(f"\n  {G2}[*] Testing {len(params)} params with {len(LFI_PAYLOADS)} LFI payloads...{E}")
    vulns = []
    for param in params:
        print(f"\n  {GD}[→] Parameter: {param}{E}")
        for payload in LFI_PAYLOADS:
            test_url = build_url_with_param(url, param, payload)
            r = http_get(test_url, timeout=6)
            if r["code"] == 0: continue
            if "root:x:0:0:" in r["body"] or "root:*:" in r["body"]:
                print(f"  {R2}  [!!!] LFI VULNERABLE: {payload}{E}")
                print(f"  {R}       /etc/passwd content leaked!{E}")
                vulns.append(("LFI /etc/passwd", param, payload))
            elif "Windows" in r["body"] and "hosts" in payload:
                print(f"  {R2}  [!!!] LFI VULNERABLE (Windows): {payload}{E}")
                vulns.append(("LFI Windows", param, payload))
            elif "PD9waHA" in r["body"] and "php://filter" in payload:
                print(f"  {R2}  [!!!] PHP FILTER CHAIN: {payload}{E}")
                vulns.append(("PHP Filter", param, payload))
    _report("LFI/Path Traversal", vulns)

def cmdi_scan():
    url = _get_url()
    if not url: return
    params = extract_params(url)
    if not params:
        print(f"  {R}[-] No parameters{E}"); return
    print(f"\n  {G2}[*] Testing {len(params)} params with {len(CMDI_PAYLOADS)} CMDi payloads...{E}")
    vulns = []
    markers = ["uid=", "gid=", "root:", "nobody", "Linux", "Darwin", "GNU"]
    for param in params:
        print(f"\n  {GD}[→] Parameter: {param}{E}")
        for payload in CMDI_PAYLOADS:
            test_url = build_url_with_param(url, param, payload)
            r = http_get(test_url, timeout=6)
            if r["code"] == 0: continue
            for m in markers:
                if m in r["body"]:
                    print(f"  {R2}  [!!!] CMD INJECTION: {payload}{E}")
                    print(f"  {R}       Marker found: {m}{E}")
                    vulns.append(("Command Injection", param, payload))
                    break
    _report("Command Injection", vulns)

def full_scan():
    url = _get_url()
    if not url: return
    params = extract_params(url)
    if not params:
        print(f"  {R}[-] No parameters{E}"); return
    print(f"\n  {R2}{B}[!] FULL VULNERABILITY SCAN INITIATED{E}")
    all_vulns = []
    print(f"\n  {R3}{'═'*50}{E}")
    print(f"  {GD}[PHASE 1/4] SQL Injection{E}")
    print(f"  {R3}{'═'*50}{E}")
    for param in params:
        for payload in SQLI_PAYLOADS[:10]:
            test_url = build_url_with_param(url, param, payload)
            r = http_get(test_url, timeout=5)
            if r["code"] == 0: continue
            for sig in SQL_ERRORS:
                if sig.lower() in r["body"].lower():
                    print(f"  {R2}  [!!!] SQLi: {param} = {payload}{E}")
                    all_vulns.append(("SQLi", param, payload))
                    break
    print(f"\n  {R3}{'═'*50}{E}")
    print(f"  {GD}[PHASE 2/4] XSS{E}")
    print(f"  {R3}{'═'*50}{E}")
    for param in params:
        for payload in XSS_PAYLOADS[:8]:
            test_url = build_url_with_param(url, param, payload)
            r = http_get(test_url, timeout=5)
            if payload in r.get("body",""):
                print(f"  {R2}  [!!!] XSS: {param} = {payload}{E}")
                all_vulns.append(("XSS", param, payload))
    print(f"\n  {R3}{'═'*50}{E}")
    print(f"  {GD}[PHASE 3/4] LFI{E}")
    print(f"  {R3}{'═'*50}{E}")
    for param in params:
        for payload in LFI_PAYLOADS[:6]:
            test_url = build_url_with_param(url, param, payload)
            r = http_get(test_url, timeout=5)
            if "root:x:0:0:" in r.get("body",""):
                print(f"  {R2}  [!!!] LFI: {param} = {payload}{E}")
                all_vulns.append(("LFI", param, payload))
    print(f"\n  {R3}{'═'*50}{E}")
    print(f"  {GD}[PHASE 4/4] Command Injection{E}")
    print(f"  {R3}{'═'*50}{E}")
    for param in params:
        for payload in CMDI_PAYLOADS[:6]:
            test_url = build_url_with_param(url, param, payload)
            r = http_get(test_url, timeout=5)
            if "uid=" in r.get("body",""):
                print(f"  {R2}  [!!!] CMDi: {param} = {payload}{E}")
                all_vulns.append(("CMDi", param, payload))
    _report("Full Scan", all_vulns)

def _report(scan_type, vulns):
    print(f"\n  {R2}{B}{'═'*50}{E}")
    print(f"  {R2}{B}  {scan_type} RESULTS{E}")
    print(f"  {R2}{B}{'═'*50}{E}")
    if not vulns:
        print(f"  {G}[+] No vulnerabilities detected{E}")
    else:
        print(f"  {R2}[!!!] {len(vulns)} potential vulnerabilities found!{E}")
        for vtype, param, payload in vulns:
            print(f"  {R}  ✗ {vtype} | Param: {param} | Payload: {payload[:40]}{E}")
    print(f"  {R2}{B}{'═'*50}{E}")
