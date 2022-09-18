import socket, random, json, pickle
from _thread import *

s = socket.socket()
fr = open('world.wld', 'rb')
list_blocks = pickle.load(fr)
world = {}
all_players={}
#1 is for grass, 2 is wood, 3 is stone

for i in list_blocks:
    world[i] = 1

print("Socket successfully created")
port = 25565
s.bind((socket.gethostname(), port))
print("socket binded to %s" % port)


def serve(conn, ip):
    while True:
        try:
            player, data = eval(conn.recv(1024).decode())
            all_players[ip]=player
            if data != None:
                data=data[0]
                data, block = (data[0:3], data[3])
        except Exception as e:
            print('disconnected from ' + str(ip)+ ' because '+e.__repr__())
            print(data, type(data))
            break
        #print(data, type(data))
        if data != None:
            world[tuple(data)] = block
            print(tuple(data))
        conn.send(str((all_players, world)).encode())


s.listen()
print("socket is listening")
while True:
    c, addr = s.accept()
    print(addr)
    start_new_thread(serve, (c, addr[0]))
