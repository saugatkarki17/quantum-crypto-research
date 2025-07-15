import time
from pqcrypto.kem import kyber768

def encrypt(plaintext, public_key):
    # Kyber's a KEM, so it doesn't directly encrypt plaintext. It makes a shared secret
    # you can use with something like AES to encrypt your actual data.
    # Here, we just use the plaintext to demo the process, but Kyber doesn't touch it.

    start = time.time()
    # Get ciphertext and shared secret from Kyber
    ciphertext, shared_secret = kyber768.encapsulate(public_key)
    end = time.time()
    encrypt_time = (end - start) * 1000  # Convert to milliseconds

    # We'll use the shared secret later for decryption checks
    return ciphertext, shared_secret, encrypt_time, len(ciphertext)

if __name__ == "__main__":
    # Quick test with keys
    from kyber_keygen import generate_keys
    pub_key, _, _, _ = generate_keys()

    dummy_plaintext = b"Just some dummy text to show encryption."
    cipher, shared_secret, enc_time, c_size = encrypt(dummy_plaintext, pub_key)
    print(f"Encapsulation took {enc_time:.4f} ms")
    print(f"Ciphertext size: {c_size} bytes")
    # Don't print the full secret, keep it hush-hush