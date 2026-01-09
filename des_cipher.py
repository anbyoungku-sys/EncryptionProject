# DES : 64비트 블록, 56비트 키

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from oracledb.thin_impl import encrypt_cbc

# 키설정()
key = b'secretky'

# 평문
plaintext = b'hello, world!!'

# 패딩  - 지정한 크기의 블록보다 작은 데이터를 다루는 방법
padded_text = pad(plaintext, 8)

# 암호화 - 블록단위 암호화 지원
des = DES.new(key, DES.MODE_ECB)
encrypted = des.encrypt(padded_text)
print(encrypted)

# 복호화
decrypted = des.decrypt(encrypted)
unpad_decrypted = unpad(decrypted, 8)
print(unpad_decrypted)
