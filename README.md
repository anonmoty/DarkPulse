# DarkPulse
only education purpose do not misuse I am not responsible for your suspicious activity 
<img width="720" height="832" alt="Image" src="https://github.com/user-attachments/assets/36267115-27b5-487d-b7ca-f388f6b2938d" />

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!--                        DARKPULSE - README.md                            -->
<!--              Professional Offensive Security Tool                       -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->

<div align="center">

# 💀 DARKPULSE

### `Scan • Exploit • Dominate`

**A Python-based offensive security framework for red teamers and bug bounty hunters.**

[![Version](https://img.shields.io/badge/version-1.0.0-red?style=flat-square)](https://github.com/anonmoty/DarkPulse)
[![Python](https://img.shields.io/badge/python-3.8+-green?style=flat-square)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20win%20%7C%20mac-red?style=flat-square)](https://github.com/anonmoty/DarkPulse)
[![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)](https://github.com/anonmoty/DarkPulse)

</div>

---

```
████████████████████████████████████████████████████████████████████████
█                                                                      █
█   ██████╗  █████╗ ██████╗ ██╗  ██╗██████╗ ██╗   ██╗██╗     ███████╗  █
█   ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██║   ██║██║     ██╔════╝  █
█   ██║  ██║███████║██████╔╝█████╔╝ ██████╔╝██║   ██║██║     ███████╗  █
█   ██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔═══╝ ██║   ██║██║     ╚════██║  █
█   ██████╔╝██║  ██║██║  ██║██║  ██╗██║     ╚██████╔╝███████╗███████║  █
█   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚══════╝  █
█                                                                      █
█                    [ Scan | Exploit | Dominate ]                     █
█                                                                      █
████████████████████████████████████████████████████████████████████████
```

---

## ⚠️ Legal Disclaimer

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   DARKPULSE is an OFFENSIVE security tool built for AUTHORIZED       ║
║   penetration testing, red teaming, and bug bounty programs only.    ║
║                                                                      ║
║   ▸ Use ONLY on systems you own or have written permission to test.  ║
║   ▸ Unauthorized access or exploitation is ILLEGAL.                  ║
║   ▸ Always follow the bug bounty scope and local laws.               ║
║   ▸ The author is NOT responsible for any misuse or damage.          ║
║                                                                      ║
║   Hack responsibly. Exploit ethically. Report professionally.        ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 🎯 What Is DarkPulse?

**DarkPulse** is a Python-based **offensive security framework** designed for **red teamers, penetration testers, and bug bounty hunters**. It combines multiple attack and reconnaissance modules into one streamlined, modular framework — with a clean, hacker-style terminal interface.

Whether you're performing recon, scanning for vulnerabilities, or validating exploits — DarkPulse gives you the **power and precision** you need.

---

## ✨ Core Features

```
┌─────────────────────────────────────────────────────────────────────┐
│  [01] 🔍 Reconnaissance      → Subdomain & endpoint discovery        │
│  [02] 🛡️ Vulnerability Scan  → XSS, SQLi, SSRF, LFI detection        │
│  [03] 🌐 Web Crawler         → Maps internal/external links          │
│  [04] 📡 DNS Enumeration     → Resolves and maps DNS records         │
│  [05] 🧪 Payload Generator   → Custom attack payloads                │
│  [06] 💥 Exploit Validator   → Safe PoC validation                   │
│  [07] ⚡ Multi-Threaded       → Fast parallel scanning                │
│  [08] 📊 Live Progress Bar   → Real-time terminal feedback           │
│  [09] 📝 JSON Reports        → Structured, machine-readable output   │
│  [10] 🎨 Hacker Terminal UI  → Red + Green aesthetic                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

```bash
# Clone the repo
git clone https://github.com/anonmoty/DarkPulse.git
cd DarkPulse

# Install dependencies
pip install -r requirements.txt

# Run
python darkpulse.py --help
```

**One-liner:**

```bash
git clone https://github.com/anonmoty/DarkPulse.git && cd DarkPulse && pip install -r requirements.txt && python darkpulse.py --help
```

---

## 🎯 Usage

```bash
# Basic recon
python darkpulse.py --target https://example.com --recon

# Vulnerability scan
python darkpulse.py --target https://example.com --vuln

# Full offensive scan
python darkpulse.py --target https://example.com --full --threads 20 \
                    --output reports/scan.json --verbose
```

### CLI Flags

```
┌─────────────────────────────────────────────────────────────────────┐
│  --target       →  Target URL                                       │
│  --recon        →  Run reconnaissance                               │
│  --vuln         →  Run vulnerability scan                           │
│  --full         →  Full offensive scan                              │
│  --threads      →  Number of threads (default: 10)                  │
│  --output       →  Report output path                               │
│  --verbose      →  Verbose logging                                  │
│  --help         →  Show help                                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 How It Works

```mermaid
graph LR
    A[Target Input] --> B[Recon Scan]
    B --> C[Endpoint Discovery]
    C --> D[Vulnerability Check]
    D --> E{Vulnerable?}
    E -->|Yes| F[Log Exploit]
    E -->|No| G[Next Endpoint]
    F --> H[Generate Report]
    G --> D
    H --> I[Done]

    style A fill:#1a0000,stroke:#FF0000,color:#00FF00
    style F fill:#1a0000,stroke:#FF0000,color:#00FF00
    style I fill:#1a0000,stroke:#FF0000,color:#00FF00
```

1. **Input** — Takes target URL
2. **Recon** — Gathers information
3. **Discovery** — Finds hidden endpoints
4. **Scan** — Tests for vulnerabilities
5. **Exploit** — Validates findings safely
6. **Report** — Outputs structured findings

---

## 📁 Project Structure

```
DarkPulse/
├── darkpulse.py
├── core/
│   ├── scanner.py
│   ├── crawler.py
│   ├── analyzer.py
│   └── reporter.py
├── payloads/
│   ├── xss.txt
│   ├── sqli.txt
│   └── lfi.txt
├── reports/
├── tests/
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 📸 Demo

```
██████████████████████████████████████████████████████████████████████
█                                                                    █
█   DARKPULSE v1.0.0                                                 █
█   ───────────────────────────────────────────────────────────      █
█                                                                    █
█   [✓] Target: https://example.com                                  █
█   [✓] Mode: Full Offensive Scan                                    █
█   [✓] Threads: 20                                                  █
█   [→] Scanning...                                                  █
█                                                                    █
█   [████████████████████████░░░░░░] 80%                             █
█                                                                    █
█   [!] VULNERABLE: /admin                                           █
█   [!] VULNERABLE: /api/v1/debug                                    █
█   [✓] Scan complete in 4.32s                                       █
█   [✓] Report: reports/scan_2024.json                               █
█                                                                    █
█                     Happy Hunting! 🎯                              █
█                                                                    █
██████████████████████████████████████████████████████████████████████
```

---

## 🛠️ Requirements

```txt
requests>=2.28.0
aiohttp>=3.9.0
beautifulsoup4>=4.11.0
colorama>=0.4.6
tqdm>=4.65.0
rich>=13.0.0
```

```bash
pip install -r requirements.txt
```

---

## 🎨 Terminal Theme

DarkPulse uses a **red + green** hacker palette:

```python
THEME = {
    "primary":   "\033[38;5;196m",  # Bright Red
    "secondary": "\033[38;5;46m",   # Matrix Green
    "accent":    "\033[38;5;214m",  # Amber
    "error":     "\033[38;5;196m",  # Red
    "warning":   "\033[38;5;220m",  # Yellow
    "info":      "\033[38;5;46m",   # Green
    "reset":     "\033[0m",
}
```

---

## 🔥 Power User Tips

```bash
# DarkPulse + subfinder
subfinder -d target.com | httpx | while read url; do
    python darkpulse.py --target "$url" --recon
done

# DarkPulse + nuclei
python darkpulse.py --target https://example.com --full -o scan.json
nuclei -u https://example.com -t ~/nuclei-templates/
```

---

## 🐛 Red Team Workflow

```
██████████████████████████████████████████████████████████████████████
█                                                                    █
█   [01] Subdomain Enumeration  →  amass / subfinder                 █
█   [02] Live Host Detection    →  httpx                             █
█   [03] Recon & Scan           →  DarkPulse  ← you are here         █
█   [04] Endpoint Analysis      →  grep, waybackurls                 █
█   [05] Vulnerability Scanning →  nuclei, XSStrike                  █
█   [06] Manual Testing         →  Burp Suite                        █
█                                                                    █
██████████████████████████████████████████████████████████████████████
```

### Use Cases

- 🔍 **Recon** on any target
- 📜 **Endpoint discovery** for hidden routes
- 🗺️ **Site crawling** for full attack surface
- 🧪 **Vulnerability validation** in safe lab mode
- 📊 **Structured reports** for documentation

---

## 🗺️ Roadmap

```
┌─────────────────────────────────────────────────────────────────────┐
│  [x] Recon scanner                                                  │
│  [x] Vulnerability scan                                             │
│  [x] Site crawler                                                   │
│  [x] JSON reports                                                   │
│  [x] Hacker terminal UI                                             │
│  [ ] XSS detection module                                           │
│  [ ] SQLi detection module                                          │
│  [ ] SSRF detection module                                          │
│  [ ] LFI/RFI detection module                                       │
│  [ ] Docker image                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🤝 Contributing

1. Fork the repo
2. Create branch (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📜 License

MIT License. See [`LICENSE`](LICENSE).

---

## 🙏 Credits

- **Author:** [@anonmoty](https://github.com/anonmoty)
- **Inspired by:** The offensive security community
- **Built with:** Python, caffeine, and curiosity ☕

---

<div align="center">

```
██████████████████████████████████████████████████████████████████████
█                                                                    █
█        💀  SCAN HARD.  EXPLOIT SMART.  DOMINATE ALWAYS.  💀        █
█                                                                    █
█                  ⭐  If this tool helped you, star it!  ⭐           █
█                                                                    █
██████████████████████████████████████████████████████████████████████
```

</div>
