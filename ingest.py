# =================================================================
# MODULE: JustAirAudit Sovereign Engine (v1.1)
# AUTHOR: Lemarc Wincher
# DATE: April 4, 2026 | San Marcos, TX
# -----------------------------------------------------------------
# DESCRIPTION: Core logic for Local Vector Database (ChromaDB) ingestion 
# of PCI-DSS v4.0.1.
# -----------------------------------------------------------------
# LICENSE: PROPRIETARY & CONFIDENTIAL. All Rights Reserved.
# This code is the sole intellectual property of Lemarc Wincher.
# Unauthorized reproduction or distribution is strictly prohibited.
# =================================================================


import os
import sys
import pypdf
import chromadb
from chromadb.utils import embedding_functions


# --- 1. PATH FIX ---
# This ensures the script finds the PDF whether it's a .py or a .exe
if getattr(sys, 'frozen', False):
    # Running as a compiled .exe
    base_dir = os.path.dirname(sys.executable)
else:
    # Running as a raw .py script
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the PDF and Vault paths relative to the executable
pdf_path = os.path.join(base_dir, "PCI-DSS-v4_0_1.pdf")
vault_path = os.path.join(base_dir, "pci_vault")

# --- 2. SETUP PERMANENT "BRAIN" ---
# PersistentClient ensures the data stays on the disk in ./pci_vault
client = chromadb.PersistentClient(path=vault_path)
emb_fn = embedding_functions.DefaultEmbeddingFunction()
collection = client.get_or_create_collection(name="pci_rules", embedding_function=emb_fn)

def run_ingestion():
    if not os.path.exists(pdf_path):
        print(f"[-] ERROR: PCI-DSS PDF not found at: {pdf_path}")
        print("[!] Please place 'PCI-DSS-v4_0_1.pdf' in the same folder as this tool.")
        return

# --- 3. EXTRACT & INDEX ---
    print(f"[*] INITIATING SOVEREIGN SCAN: {pdf_path}")
    try:
        reader = pypdf.PdfReader(pdf_path)
        total_pages = len(reader.pages)
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                # Add to the local Vector Database
                collection.add(
                    documents=[text], 
                    ids=[f"page_{i}"]
                )
                if i % 50 == 0:
                    print(f" > Processing: {i}/{total_pages} pages indexed...")

        print(f"\n✅ VAULT SUCCESSFULLY BUILT!")
        print(f"[*] Location: {vault_path}")
        print(f"[*] Content: {total_pages} pages stored in Sovereign Brain.")

    except Exception as e:
        print(f"[-] CRITICAL SYSTEMS ERROR: {str(e)}")

if __name__ == "__main__":
    run_ingestion()
