⚠️ NOTE: This repository is a Source-Available showcase. The core audit logic is encrypted for IP protection. To use the functional tool, please download the compiled GUI from justairaudit.com.

🛡️ JustAirAudit v1.1 — Sovereign PCI Compliance Engine
Version: 1.1.0-FINAL

Author: Lemarc Wincher

Release Date: April 6th, 2026

Website: https://www.justairaudit.com

🔒 Security & Zero-Trust Architecture
JustAirAudit is a sovereign, air-gapped compliance tool designed for high-security environments where data egress is a critical risk.

Local-First AI: All audits are performed locally via Ollama; no data ever leaves the host machine.

Privacy Shield: A Python-based redaction layer utilizing Heuristic Pattern Matching to identify and scrub high-entropy sensitive strings (API keys, secrets, and PII) before they reach the inference engine.

Encrypted Logic: Proprietary audit prompts are stored as encrypted .enc files (AES-128). This ensures the integrity of the PCI-DSS v4.0.1 compliance logic and protects the engine's internal intellectual property.

🚀 Get the Full Application
This repository serves as a technical showcase of the engine's architecture. For the fully compiled, ready-to-use GUI version for Windows, visit the official site:
🔗 justairaudit.com

🛠️ Installation & Setup (For Technical Review)
1. Environment Configuration
For security, the encryption key is managed via a local environment file that is ignored by Git.

Locate .env.example in the root directory and rename it to .env.

Open .env and insert your JAA_PROMPT_KEY.

Note: The provided .enc files are encrypted with a private master key. While the code is transparent for review, the engine will not decrypt these specific files without the author's proprietary key.

2. Dependency Setup
JustAirAudit requires Ollama for local inference:

Download Ollama

Pull the required model:

Bash
ollama pull llama3
3. Application Structure
Ensure the following directory structure is maintained for the engine to function:

pci_vault/ — Local Vector Database (ChromaDB)

prompts/ — Encrypted Compliance Templates (*.enc)

.env — Your private Master Key

JustAirAuditLogo.png — Branding Assets

📜 Proprietary License & Usage
Copyright (c) 2026 Lemarc Wincher. All Rights Reserved.

Personal Use: This software is proprietary. You may review the code for educational and personal purposes free of charge.

Commercial/Corporate Use: Modification, redistribution, or commercial use is strictly prohibited without explicit permission. Businesses or organizations wishing to deploy JustAirAudit must obtain a commercial license from the author prior to use.

DISTRIBUTION: Source-available for architectural review. Execution locked; users directed to justairaudit.com for functional GUI version.

Trademarks: JustAirAudit™ is a trademark of Lemarc Wincher.

For licensing inquiries or professional demonstrations, please contact:

Email: lemwincher@gmail.com

LinkedIn: linkedin.com/in/lemarc-wincher/
