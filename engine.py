# =================================================================
# MODULE: JustAirAudit Sovereign Engine (v1.1)
# AUTHOR: Lemarc Wincher
# DATE: April 4, 2026 | San Marcos, TX
# -----------------------------------------------------------------
# DESCRIPTION: Core logic for PII/Secret Redaction and 
# Local Vector Database (ChromaDB) PCI-DSS v4.0.1 Querying.
# -----------------------------------------------------------------
# LICENSE: PROPRIETARY & CONFIDENTIAL. All Rights Reserved.
# This code is the sole intellectual property of Lemarc Wincher.
# Unauthorized reproduction or distribution is strictly prohibited.
# =================================================================

import os
from dotenv import load_dotenv

load_dotenv() 

from prompts.secret_prompts import get_prompt

import re
import chromadb
import ollama
from prompts.secret_prompts import get_prompt  # <- fixed import path

# --- The Swapper: Automatically redacts secrets ---
def redact_secrets(code):
    assignment_pattern = r"(?i)(\w+\s*[:=]\s*['\"])(.*?)(['\"])"
    clean_code = re.sub(assignment_pattern, r"\1[REDACTED]\3", code)
    return clean_code

# --- Connect to PCI Vault ---
client = chromadb.PersistentClient(path="./pci_vault")
collection = client.get_collection(name="pci_rules")

def run_audit(user_code):
    """
    Redacts secrets, queries PCI vault, retrieves encrypted prompt, 
    calls local AI, and returns results.
    """
    # Redact sensitive strings
    safe_code = redact_secrets(user_code)
    
    # Print redacted code in terminal with GUI-style formatting
    print("\n" + "="*30 + " SECURE CODE SENT TO AI " + "="*30)
    print(safe_code)
    print("="*74 + "\n")
    
    # Query ChromaDB for relevant PCI rule
    results = collection.query(query_texts=[safe_code], n_results=1)
    relevant_rule = results['documents'][0][0]

    # Get encrypted prompt from prompts folder
    prompt_template = get_prompt("engine_main")  # reads prompts/engine_main.enc
    prompt = prompt_template.format(safe_code=safe_code, relevant_rule=relevant_rule)

    # Call local AI
    response = ollama.generate(model='llama3', prompt=prompt, options={"temperature": 0})
    
    return safe_code, relevant_rule, response['response']

# --- CLI Interface ---
if __name__ == "__main__":
    print("🛡️  JustAirAudit v1.0 | FOUNDED 04/04/2026")
    print("🔒 STATUS: LOCAL / AIR-GAPPED / ZERO-TRUST")
    print("-" * 55)
    
    print("Please paste the code you want to audit for PCI-DSS v4.01:")
    print("(Press Enter, then Ctrl+Z, then Enter again to finish)\n")
    
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
            
    user_input = "\n".join(lines)
    
    if user_input.strip():
        print("\n[PHASE 1 COMMENCED] Scrubbing secrets & querying the vault...")
        safe, rule, report = run_audit(user_input)
        
        print(f"\n[PHASE 2 COMMENCED] Matched PCI Requirement: \n> {rule[:150]}...")
        
        print("\n" + "="*30 + " FINAL AUDIT REPORT " + "="*30)
        print(report)
        print("="*74)
    else:
        print("No code provided. System standing by.")
