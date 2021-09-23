import socket
import os
import os.path
import base64
import hashlib
import pyperclip
from colorama import init, Fore

def hash_file(filename):

   h = hashlib.sha1()

   with open(filename,'rb') as file:

       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   return h.hexdigest()


init()

print(Fore.YELLOW+'Welcome to the droid`s file teleporter!')

IP = '127.0.0.1' #Свой айпи
PORT = 65432 #Можно не трогать

key = str(IP)+":"+str(PORT)
key = key.encode("ascii")
key = base64.b64encode(key)
key = key.decode("ascii")
print(Fore.GREEN)

task=input('You want to get or send file? g/s:')
print(Fore.RESET)
if task=="g":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        filepath=input('Select downloading folder: ').strip("\"")
        print(Fore.RED)
        key=input("Get the key of the person who sends: ")
        key = key.encode("ascii")
        key = base64.b64decode(key)
        key = key.decode("ascii")
        HOST=key.split(":")[0]
        PORT=int(key.split(":")[1])
        s.connect((HOST, PORT))
        print(Fore.CYAN)
        print('Hello,',HOST,':',PORT,'!')
        hash =s.recv(1024).decode("utf-8")
        name =s.recv(1024).decode("utf-8")
        name =name.split("\\")
        name =name[len(name)-1]
        print("Downloading "+name)
        file = open(filepath+'\\'+name+".part", "ab")
        file.truncate(0)
        while True:
            data = s.recv(1024)
            if not data:
                break
            file.write(data)
        file.close()
        if os.path.isfile(filepath+'\\'+name):
            os.remove(filepath+'\\'+name)
        os.rename(filepath+'\\'+name+".part",filepath+'\\'+name)
        print("Checking hashes...")
        if hash_file(filepath+'\\'+name)==hash:
            print(Fore.GREEN+"File is GOOD (hash verified)")
        else:
            print(Fore.RED+"File is BAD (hash not verified)")
            print(hash_file(filepath+'\\'+name))
            print(hash)

elif task=="s":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        filename=input('Drag\drop to cmd file to send: ').strip("\"")
        file = open(filename, "rb")
        s.bind((IP, PORT))
        print(Fore.CYAN+"Your key copied. Just Ctrl+V it.")
        pyperclip.copy(key)
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(Fore.RED)
            print('Hello,',addr,'!')
            print('Streaming ',filename)
            byte=file.read(1000)
            conn.sendall(bytes(hash_file(filename), 'utf-8'))
            conn.sendall(bytes(filename, 'utf-8'))
            while byte:
                conn.sendall(byte)
                byte=file.read(1000)
        file.close()
print(Fore.YELLOW)
print("Work Сompleted")

