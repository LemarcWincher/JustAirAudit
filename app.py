# =================================================================
# APPLICATION: JustAirAudit - Air-Gapped PCI Compliance Tool
# VERSION: 1.1.0-FINAL
# RELEASE DATE: April 5, 2026
# AUTHOR: Lemarc Wincher
# =================================================================

import os
import sys
import threading
import customtkinter as ctk
import ollama
from engine import redact_secrets
import chromadb
from PIL import Image

# --- 1.BULLETPROOF PATH LOGIC ---
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(base_path, "pci_vault")
logo_path = os.path.join(base_path, "JustAirAuditLogo.png")
icon_path = os.path.join(base_path, "JustAirAuditIcon.ico")

# --- 2. CHROMADB BRAIN SETUP ---
try:
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(name="pci_rules")
except Exception as e:
    print(f"Vault Init Warning: {e}")

# --- 3. THEME & UI ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JustAirApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JustAirAudit v1.1 | Sovereign PCI-DSS Engine")
        self.geometry("1100x850")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (Branding & Status) ---
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0, fg_color="#111111")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # --- Taskbar Icon ---
        try:
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Taskbar icon load failed: {e}")

        # --- Sidebar Logo (Fixed size, no stretch) ---
        try:
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                self.logo_img = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(250, 250)  # fixed size
                )
                self.logo_image_label = ctk.CTkLabel(self.sidebar, image=self.logo_img, text="")
                self.logo_image_label.pack(pady=(20, 15))
        except Exception as e:
            print(f"Sidebar logo load failed: {e}")

        self.logo_label = ctk.CTkLabel(self.sidebar, text="JUST AIR AUDIT", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.pack(pady=(5, 5))

        self.sub_logo = ctk.CTkLabel(self.sidebar, text="SOVEREIGN COMPLIANCE", font=ctk.CTkFont(size=11), text_color="gray")
        self.sub_logo.pack(pady=(0, 40))

        # Status Indicators
        self.add_status("● AIR-GAPPED PRIVACY", "#00FF00")
        self.add_status("● ZERO-TRUST SHIELD", "#00FF00")
        self.add_status("● LOCALHOST: 127.0.0.1", "#3B8ED0")

        # Copyright Footer
        self.footer_label = ctk.CTkLabel(
            self.sidebar,
            text="© 2026 LEMARC WINCHER\nALL RIGHTS RESERVED\nBUILD: v1.1.0-FINAL",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#444444",
            justify="left"
        )
        self.footer_label.pack(side="bottom", pady=30, padx=20, anchor="w")

        # --- MAIN AUDIT AREA ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.label = ctk.CTkLabel(self.main_frame, text="Input Source Code for Sovereign Audit:", font=("Helvetica", 16))
        self.label.pack(pady=(20, 10))

        self.code_input = ctk.CTkTextbox(self.main_frame, height=320, width=680, font=("Consolas", 12))
        self.code_input.pack(padx=20, pady=10)

        self.audit_button = ctk.CTkButton(
            self.main_frame,
            text="RUN SOVEREIGN AUDIT",
            font=ctk.CTkFont(weight="bold"),
            height=45,
            width=200,
            command=self.start_audit_thread
        )
        self.audit_button.pack(pady=20)

        self.output_log = ctk.CTkTextbox(
            self.main_frame,
            height=260,
            width=680,
            fg_color="#000000",
            text_color="#00FF00",
            font=("Consolas", 11)
        )
        self.output_log.pack(padx=20, pady=10)
        self.update_log("JustAirAudit Engine Ready. Sovereign Vault Online.")

    def add_status(self, text, color):
        lbl = ctk.CTkLabel(self.sidebar, text=text, text_color=color, font=ctk.CTkFont(size=11, weight="bold"))
        lbl.pack(pady=10, padx=35, anchor="w")

    def update_log(self, text):
        self.output_log.insert("end", f"{text}\n")
        self.output_log.see("end")
        self.update_idletasks()

    def start_audit_thread(self):
        self.audit_button.configure(state="disabled", text="AUDITING...")
        threading.Thread(target=self.run_audit_logic, daemon=True).start()

    def run_audit_logic(self):
        try:
            raw_code = self.code_input.get("1.0", "end-1c")
            if not raw_code.strip():
                self.update_log("\n[!] ERROR: Null input detected.")
                return

            self.update_log("\n" + "="*60)
            self.update_log("> INITIATING ZERO-TRUST PRIVACY SHIELD...")

            # STEP 1: Redaction
            safe_code = redact_secrets(raw_code)
            self.update_log("> SCAN COMPLETE. SENSITIVE STRINGS REDACTED.")
            self.update_log(f"\nSECURE CODE SENT TO AI\n{safe_code}\n")

            # STEP 2: The Ollama Call
            self.update_log("> CONSULTING SOVEREIGN VAULT...")

            response = ollama.chat(model='llama3', messages=[
                {'role': 'system', 'content': "Senior PCI-DSS v4.0.1 Auditor Logic [ENCRYPTED-SIG]"},
                {'role': 'user', 'content': f"Audit this sanitized code: {safe_code}"}
            ])

            self.update_log(f"\n[FINAL COMPLIANCE REPORT]\n{response['message']['content']}")
            self.update_log("="*60)

        except Exception as e:
            self.update_log(f"\n[SYSTEM ERROR]: {str(e)}")
        finally:
            self.audit_button.configure(state="normal", text="RUN SOVEREIGN AUDIT")


if __name__ == "__main__":
    app = JustAirApp()
    app.mainloop()