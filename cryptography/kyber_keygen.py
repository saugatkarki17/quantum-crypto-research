import time
from pqcrypto.kem import kyber768  # Using Kyber768 for this

def generate_keys():
    start = time.time()
    public_key, secret_key = kyber768.generate_keypair()
    end = time.time()
    keygen_time = (end - start) * 1000  # Convert to milliseconds

    # In a real app, you'd probably save these keys to files
    return public_key, secret_key, keygen_time, len(public_key) + len(secret_key)

if __name__ == "__main__":
    pub_key, sec_key, k_time, k_size = generate_keys()
    print(f"Key generation took {k_time:.4f} ms")
    print(f"Total key size: {k_size} bytes")
    # Don't print full keys in production, keep 'em safe