import csv
import os
from kyber_keygen import generate_keys
from kyber_encrypt import encrypt
from kyber_decrypt import decrypt
import time

def run_kyber_benchmark(num_runs=1):
    log_file = os.path.join("results", "log.csv")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    with open(log_file, 'w', newline='') as csvfile:
        fieldnames = ['run_id', 'keygen_time_ms', 'encrypt_time_ms', 'decrypt_time_ms', 'key_size_bytes', 'ciphertext_size_bytes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(num_runs):
            print(f"Running test {i+1} of {num_runs}...")
            # Generate keys
            pub_key, sec_key, keygen_time, key_size = generate_keys()

            # Dummy plaintext for testing
            dummy_plaintext = b"This is a dummy plaintext of variable length " * (i % 5 + 1)

            # Encrypt it
            ciphertext, shared_secret, encrypt_time, ciphertext_size = encrypt(dummy_plaintext, pub_key)

            # Decrypt it
            decrypted_shared_secret, decrypt_time = decrypt(ciphertext, sec_key)

            # Quick check to make sure things match
            if shared_secret != decrypted_shared_secret:
                print(f"Oops, shared secrets don't match in run {i+1}!")

            writer.writerow({
                'run_id': i + 1,
                'keygen_time_ms': f"{keygen_time:.4f}",
                'encrypt_time_ms': f"{encrypt_time:.4f}",
                'decrypt_time_ms': f"{decrypt_time:.4f}",
                'key_size_bytes': key_size,
                'ciphertext_size_bytes': ciphertext_size
            })
    print(f"Done! Results are in {log_file}")

if __name__ == "__main__":
    run_kyber_benchmark(num_runs=100) # 100 runs for solid data