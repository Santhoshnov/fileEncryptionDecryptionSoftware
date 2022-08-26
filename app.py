import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import base64
import streamlit as st 
import os
import io


def file_encryption(filename, password_input):
    Encoded_Password=password_input.encode()
    

    salt = b'\x08\xcfTfw\xd2\x85\x12\xa5D\xa9\xd3:\x86\xda\xa1'

    # derive
    kdf = Scrypt(salt=salt,length=32,n=2**14,r=8,p=1,)
    key = kdf.derive(Encoded_Password)
    key = base64.urlsafe_b64encode(key)
    f=Fernet(key)

    
    Original_Data=filename.read()

    Encrypted_Data=f.encrypt(Original_Data)
     
    with io.BytesIO() as File:
        File.write(Encrypted_Data)
        st.success('file successfully Encrypted!', icon="✅")
        st.download_button(label='Download encrypted file',data=File,file_name=filename.name)


def file_decryption(filename, password_input):
    Encoded_Password=password_input.encode()
    

    salt = b'\x08\xcfTfw\xd2\x85\x12\xa5D\xa9\xd3:\x86\xda\xa1'

    # derive
    kdf = Scrypt(salt=salt,length=32,n=2**14,r=8,p=1,)
    key = kdf.derive(Encoded_Password)
    key = base64.urlsafe_b64encode(key)
    
    f=Fernet(key)

     
    Enc_File=filename.read()

    try:
        Decrypted_Data=f.decrypt(Enc_File)

    except cryptography.fernet.InvalidToken:
        st.warning("Invalid Password",icon="⚠️")
        return

    with io.BytesIO() as File:
        File.write(Decrypted_Data)
        st.success('file successfully Decrypted!', icon="✅")
        st.download_button(label='Download Decrypted file',data=File,file_name=filename.name)






st.title('File Encryption Decryption')
file_upload = st.file_uploader("Upload a file:")
if file_upload is not None:
    loc=file_upload


choice = st.selectbox('Options:',('Encryption','Decryption'))
password =st.text_input("Password:",type="password")
submit = st.button('Submit')
if submit:
    if  not (password =='' or choice =='' or file_upload == None):
        if choice == 'Encryption':
            file_encryption(loc,password)
            
        elif choice == 'Decryption':
            file_decryption(loc,password)
            
    else:
        st.warning('No fields would be empty', icon="⚠️")

st.text('')
st.text('')
st.subheader('Developers')
st.write('| Sirajudeen | Santhosh | Sudhar Aathith |')
