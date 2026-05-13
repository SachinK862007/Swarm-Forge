import os
import time
from cryptography.fernet import Fernet

# Generate a secret key (simulates TEE‑protected key)
key = Fernet.generate_key()
cipher = Fernet(key)

# Sensitive honeypot data that must be protected
sensitive_data = {
    "honeypot_id": "hp_01",
    "attacker_ip": "192.168.1.100",
    "mitre_technique": "T1595",
    "decoy_credentials": "admin:FakePass2024!",
    "internal_alert": "Isolated attacker session",
    "timestamp": "2026-05-13T12:00:00Z"
}

plaintext = str(sensitive_data).encode('utf-8')
encrypted_data = cipher.encrypt(plaintext)

# ---------- Defender View ----------
print("=" * 60)
print("🛡️  DEFENDER VIEW - SwarmForge TEE Dashboard")
print("=" * 60)
print("Status: Enclave ACTIVE | Memory Encryption: ON")
print("-" * 40)
print("Decrypted Honeypot Data (inside secure enclave):")
for k, v in sensitive_data.items():
    print(f"  {k}: {v}")
print("-" * 40)
print(f"Encryption Key (first 12 chars): {key[:12].decode()}... (hidden)")
print()

# ---------- Attacker View ----------
print("=" * 60)
print("💀 ATTACKER VIEW - Root Terminal (memory dump)")
print("=" * 60)
print("$ sudo cat /proc/swarmforge/mem | head -c 200")
print("-" * 40)
print(encrypted_data[:200].hex())
print("...")
print()
print("WARNING: Data is encrypted and unrecoverable without the enclave key.")
print()

# ---------- Proof of Decryption ----------
print("=" * 60)
print("🔑 PROOF: Decryption with valid key")
print("=" * 60)
decrypted = cipher.decrypt(encrypted_data)
print(f"Decrypted: {decrypted.decode('utf-8')}")
print()

print("Press Ctrl+C to exit the demo...")
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("\nSwarmForge TEE Demo terminated.")