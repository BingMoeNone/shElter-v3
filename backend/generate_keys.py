#!/usr/bin/env python3
"""
Generate RSA key pair for JWT authentication
"""

import os
import sys
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


def generate_rsa_keys(private_key_path: str, public_key_path: str, key_size: int = 2048):
    """Generate RSA key pair and save to files"""
    print(f"Generating RSA key pair with {key_size} bits...")
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    
    # Generate private key file
    with open(private_key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print(f"Private key saved to: {private_key_path}")
    
    # Generate public key
    public_key = private_key.public_key()
    
    # Generate public key file
    with open(public_key_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print(f"Public key saved to: {public_key_path}")
    
    print("RSA key pair generation completed successfully!")


if __name__ == "__main__":
    # Create keys directory if it doesn't exist
    keys_dir = "keys"
    if not os.path.exists(keys_dir):
        os.makedirs(keys_dir)
        print(f"Created keys directory: {keys_dir}")
    
    # Default key paths
    private_key_path = os.path.join(keys_dir, "private_key.pem")
    public_key_path = os.path.join(keys_dir, "public_key.pem")
    
    # Generate keys
    generate_rsa_keys(private_key_path, public_key_path)
    
    print("\nNext steps:")
    print("1. Update your .env file with the correct key paths")
    print("2. Ensure these keys are not committed to version control")
    print("3. For production, generate new keys and store them securely")
