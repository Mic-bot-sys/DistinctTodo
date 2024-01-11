from cryptography.fernet import Fernet

key = b'9QlO5KsStpB24m9fm2wOMLDUZvnEdoIwcKRRycfa0qA='

def Decrypt(message):
    fernet = Fernet(key)
    decMessage = fernet.decrypt(message).decode()
    return decMessage