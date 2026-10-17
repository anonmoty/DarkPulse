import socket, ssl, struct, re, time, urllib.request, urllib.parse, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.config import *

def tcp_scan(host, port, timeout=1.5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        r = s.connect_ex((host, port))
        s.close()
        return r == 0
    except:
        return False

def mass_scan(host, ports, threads=100, timeout=1.5):
    open_ports = []
    def _scan(p):
        if tcp_scan(host, p, timeout):
            return p
        return None
    with ThreadPoolExecutor(max_workers=threads) as ex:
        futs = {ex.submit(_scan, p): p for p in ports}
        for f in as_completed(futs):
            r = f.result()
            if r:
                open_ports.append(r)
    return sorted(open_ports)

def banner_grab(host, port, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        probes = {
            80: b"GET / HTTP/1.0\r\nHost: %b\r\n\r\n" % host.encode(),
            443: b"GET / HTTP/1.0\r\nHost: %b\r\n\r\n" % host.encode(),
            22: b"", 21: b"", 25: b"EHLO test\r\n",
            3306: b"", 5432: b"", 6379: b"INFO\r\n",
            27017: b"", 8080: b"GET / HTTP/1.0\r\n\r\n",
        }
        probe = probes.get(port, b"GET / HTTP/1.0\r\n\r\n")
        if port == 443 or port == 8443:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            s = ctx.wrap_socket(s, server_hostname=host)
        if probe:
            s.send(probe)
        data = s.recv(1024)
        s.close()
        banner = data.decode("utf-8", errors="ignore").strip()
        lines = banner.split("\n")
        for l in lines:
            l = l.strip()
            if l and not l.startswith("HTTP/") and len(l) > 3:
                return l[:80]
        return lines[0][:80] if lines else "N/A"
    except:
        return "N/A"

def http_get(url, timeout=8, follow=True):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0"}
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        code = resp.getcode()
        body = resp.read(500000).decode("utf-8", errors="ignore")
        hdrs = dict(resp.headers)
        final_url = resp.geturl()
        return {"code": code, "body": body, "headers": hdrs, "url": final_url, "error": None}
    except urllib.error.HTTPError as e:
        try:
            body = e.read(500000).decode("utf-8", errors="ignore")
        except:
            body = ""
        return {"code": e.code, "body": body, "headers": dict(e.headers) if e.headers else {}, "url": url, "error": str(e)}
    except Exception as e:
        return {"code": 0, "body": "", "headers": {}, "url": url, "error": str(e)}

def http_post(url, data, timeout=8):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/x-www-form-urlencoded"}
        encoded = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(url, data=encoded, headers=headers)
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        return {"code": resp.getcode(), "body": resp.read(500000).decode("utf-8", errors="ignore"), "error": None}
    except urllib.error.HTTPError as e:
        return {"code": e.code, "body": "", "error": str(e)}
    except Exception as e:
        return {"code": 0, "body": "", "error": str(e)}

def resolve(host):
    try:
        return socket.gethostbyname(host)
    except:
        return None

def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None

def ping_host(ip, timeout=2):
    import subprocess, platform
    param = "-n" if platform.system().lower() == "windows" else "-c"
    t_param = "-w" if platform.system().lower() == "windows" else "-W"
    try:
        r = subprocess.run(["ping", param, "1", t_param, str(timeout), ip],
                          capture_output=True, timeout=timeout+2)
        return r.returncode == 0
    except:
        return False

def extract_params(url):
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    return list(params.keys())

def build_url_with_param(url, param, value):
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    qs[param] = [value]
    new_query = urllib.parse.urlencode(qs, doseq=True)
    return urllib.parse.urlunparse(parsed._replace(query=new_query))

def dns_query(domain, qtype=1, server="8.8.8.8"):
    import random
    tid = random.randint(0, 65535)
    flags = 0x0100
    header = struct.pack(">HHHHHH", tid, flags, 1, 0, 0, 0)
    query = b""
    for part in domain.split("."):
        query += bytes([len(part)]) + part.encode()
    query += b"\x00"
    query += struct.pack(">HH", qtype, 1)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3)
        s.sendto(header + query, (server, 53))
        data = s.recv(4096)
        s.close()
        ancount = struct.unpack(">H", data[6:8])[0]
        return ancount > 0, data
    except:
        return False, b""

def zone_transfer(domain, ns=None):
    if not ns:
        ok, data = dns_query(domain, qtype=2)
        if not ok:
            return None
        ns = domain
    try:
        tid = 1234
        header = struct.pack(">HHHHHH", tid, 0x0000, 1, 0, 0, 0)
        query = b""
        for part in domain.split("."):
            query += bytes([len(part)]) + part.encode()
        query += b"\x00" + struct.pack(">HH", 252, 1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        ip = resolve(ns) or ns
        s.connect((ip, 53))
        msg = header + query
        s.send(struct.pack(">H", len(msg)) + msg)
        rlen = struct.unpack(">H", s.recv(2))[0]
        data = s.recv(rlen)
        s.close()
        ancount = struct.unpack(">H", data[6:8])[0]
        if ancount > 0:
            return data[12:].decode("utf-8", errors="ignore")[:2000]
        return None
    except:
        return None
