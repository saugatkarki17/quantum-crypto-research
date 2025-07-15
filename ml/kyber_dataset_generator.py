import csv
import os
import time
import random
import pandas as pd
from pqcrypto.kem import kyber768
import sys

# Add crypto scripts path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'crypto')))
from kyber_keygen import generate_keys
from kyber_encrypt import encrypt
from kyber_decrypt import decrypt

def simulate_cpu_load(duration_ms):
    """Mimics CPU work with some random math."""
    start = time.time()
    while time.time() < start + (duration_ms / 1000):
        _ = (random.random() ** 0.5) * random.random()  # Quick dummy calc

def generate_kyber_dataset(num_runs=1000):
    dataset_file = os.path.join("results", "kyber_dataset.csv")
    os.makedirs(os.path.dirname(dataset_file), exist_ok=True)

    data = []
    print(f"Building Kyber dataset with {num_runs} runs...")

    for i in range(num_runs):
        if i % 50 == 0:
            print(f"  At run {i}/{num_runs}...")

        # Random plaintext length for simulation
        plaintext_length = random.randint(50, 500)
        dummy_plaintext = b"A" * plaintext_length

        # Random CPU load
        cpu_load_ms = random.uniform(0, 50)
        simulate_cpu_load(cpu_load_ms)

        # Run Kyber ops
        pub_key, sec_key, _, key_size = generate_keys()
        ciphertext, shared_secret, encrypt_time, ciphertext_size = encrypt(dummy_plaintext, pub_key)
        _, decrypt_time = decrypt(ciphertext, sec_key)

        # Add occasional anomalies (2% chance)
        is_anomaly = 0
        if random.random() < 0.02:
            is_anomaly = 1
            if random.random() < 0.5:
                encrypt_time *= random.uniform(1.5, 3.0)  # Spike encrypt time

        data.append({
            'plaintext_length': plaintext_length,
            'key_size': key_size,
            'ciphertext_size': ciphertext_size,
            'encrypt_time': encrypt_time,
            'decrypt_time': decrypt_time,
            'cpu_load_duration_ms': cpu_load_ms,
            'is_anomaly': is_anomaly
        })

    df = pd.DataFrame(data)
    df.to_csv(dataset_file, index=False)
    print(f"Done! Dataset saved to {dataset_file}")

if __name__ == "__main__":
    generate_kyber_dataset(num_runs=1000)