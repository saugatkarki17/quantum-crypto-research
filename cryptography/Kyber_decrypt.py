import time
from pqcrypto.kem import kyber768

def decrypt(ciphertext, secret_key):
    start = time.time()
    shared_secret = kyber768.decapsulate(ciphertext, secret_key)
    end = time.time()
    decrypt_time = (end - start) * 1000  # Convert to milliseconds

    return shared_secret, decrypt_time

if __name__ == "__main__":
    # Quick test with keys and ciphertext
    from kyber_keygen import generate_keys
    from kyber_encrypt import encrypt

    pub_key, sec_key, _, _ = generate_keys()
    dummy_plaintext = b"Just some random data, not directly encrypted"  # KEM doesn't encrypt this
    cipher, expected_shared_secret, _, _ = encrypt(dummy_plaintext, pub_key)

    decrypted_shared_secret, dec_time = decrypt(cipher, sec_key)
    print(f"Decapsulation took {dec_time:.4f} ms")

    if decrypted_shared_secret == expected_shared_secret:
        print("Nice! Shared secret matches!")
    else:
        print("Uh-oh, shared secrets don't match.")