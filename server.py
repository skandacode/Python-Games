import socket, random, json
from _thread import *
s = socket.socket()
data={}
print ("Socket successfully created")
port = 32477
s.bind(('localhost', port))         
print ("socket binded to %s" %(port)) 
def toStr(l):
    s=''
    for i in l: 
        s+=i
    return s
def serve(conn, client_ip):
    global data
    g=random.randint(0, 10000000000)
    while True:
        try:
            x=(conn.recv(1048576)).decode().split(', ')
        except:
            conn.close()
            break
        data[g]=(x)
        pas={}
        for i in data:
            if not i==g:
                pas[i]=data[i]
        #process and store x(data)
        res_bytes=str(pas)
        conn.send(bytes(res_bytes, 'utf-8'))
s.listen()     
print ("socket is listening")            
while True:
    c, addr = s.accept()
    print(addr)
    
    start_new_thread(serve, (c, addr[0]))
