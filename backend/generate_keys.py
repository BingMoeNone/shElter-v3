#!/usr/bin/env python3
"""
RSA瀵嗛挜瀵圭敓鎴愯剼鏈?鐢ㄤ簬JWT RS256鍔犲瘑

杩愯: python generate_keys.py
"""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import os

def generate_rsa_keypair():
    """鐢熸垚RSA瀵嗛挜瀵?""
    
    # 鐢熸垚绉侀挜
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # 鐢熸垚鍏挜
    public_key = private_key.public_key()
    
    # 绉侀挜搴忓垪鍖?    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # 鍏挜搴忓垪鍖?    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # 鍐欏叆鏂囦欢
    keys_dir = os.path.dirname(os.path.abspath(__file__))
    private_key_path = os.path.join(keys_dir, "keys", "private_key.pem")
    public_key_path = os.path.join(keys_dir, "keys", "public_key.pem")
    
    # 纭繚keys鐩綍瀛樺湪
    os.makedirs(os.path.join(keys_dir, "keys"), exist_ok=True)
    
    # 鍐欏叆绉侀挜
    with open(private_key_path, "wb") as f:
        f.write(private_pem)
    print(f"鉁?绉侀挜宸茬敓鎴? {private_key_path}")
    
    # 鍐欏叆鍏挜
    with open(public_key_path, "wb") as f:
        f.write(public_pem)
    print(f"鉁?鍏挜宸茬敓鎴? {public_key_path}")
    
    # 璁剧疆鏂囦欢鏉冮檺 (Unix/Linux)
    try:
        os.chmod(private_key_path, 0o600)
        os.chmod(public_key_path, 0o644)
        print("鉁?鏂囦欢鏉冮檺宸茶缃?)
    except Exception:
        pass
    
    print("\n瀵嗛挜瀵圭敓鎴愬畬鎴?")
    print("\n鍦?.env 涓厤缃?")
    print(f"  ALGORITHM=RS256")
    print(f"  PRIVATE_KEY_PATH=keys/private_key.pem")
    print(f"  PUBLIC_KEY_PATH=keys/public_key.pem")

if __name__ == "__main__":
    generate_rsa_keypair()
