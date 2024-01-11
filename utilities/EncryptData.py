from cryptography.fernet import Fernet

key = b'9QlO5KsStpB24m9fm2wOMLDUZvnEdoIwcKRRycfa0qA='

def Encrypt(message):
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    return encMessage
    
    
def Decrypt(message):
    fernet = Fernet(key)
    decMessage = fernet.decrypt(message).decode()
    return decMessage


    
message = "This is the Best and most wealthy Programmer and Software Engineer on Earth that God Personally Blessed}"

result = Encrypt(message)
print(result)


initial = Decrypt(result)
print(initial)