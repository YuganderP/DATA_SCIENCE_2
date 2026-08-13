# Base64 Password Encoder & Decoder

## Overview

This Python project demonstrates how to:
- Encode a password using Base64
- Decode the encoded password back to original text

> Note: Base64 is an encoding technique, not real encryption.

---

# Source Code

```python
import base64

def encrypt_password(password):
    encoded_password = base64.b64encode(password.encode())
    return encoded_password

def decrypt_password(password):
    decoded_password = base64.b64decode(password)
    return decoded_password

user_password = input("enter your password:")

enc_pass = encrypt_password(user_password)

dec_pass = decrypt_password(enc_pass)

print("user password:", user_password)
print("encrypted password:", enc_pass)
print("decrypted password:", dec_pass)
```

---

# Modules Used

| Module | Purpose |
|---|---|
| `base64` | Encode and decode Base64 data |

---

# Workflow

```text
User Input → Encode Password → Decode Password → Display Output
```

---

# Example Output

```text
enter your password: hello123

user password: hello123
encrypted password: b'aGVsbG8xMjM='
decrypted password: b'hello123'
```

---

# Key Concepts

- `encode()` → converts string to bytes
- `b64encode()` → encodes bytes into Base64
- `b64decode()` → decodes Base64 back to original bytes

---

# Limitation

Base64 is **not secure** for real password storage because it can be easily decoded.

For real applications, use:
- `bcrypt`
- `argon2`
- `hashlib`

---

# Conclusion

This project is useful for learning:
- Base64 encoding
- Byte conversion
- Basic data transformation in Python