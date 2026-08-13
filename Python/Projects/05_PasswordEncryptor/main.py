import base64

def encrypt_password(password):
    encoded_password=base64.b64encode(password.encode())
    return encoded_password

def decrypt_password(password):
    decoded_password=base64.b64decode(password)
    return(decoded_password)

user_password=input("enter your password:")
enc_pass=encrypt_password(user_password)
dec_pass=decrypt_password(enc_pass)
print("user password:",user_password)
print("encrypted password:", enc_pass )
print("decrypted password:", dec_pass)



