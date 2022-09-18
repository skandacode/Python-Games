from ursina import *

app = Ursina()
from ursina.shaders import *
from CustomPlayer import CustomPlayer
import pickle, socket, time, sys

Entity.default_shader = basic_lighting_shader
# DirectionalLight(parent=scene, y=10, shadows=True)
# AmbientLight(parent=scene, y=2, z=3, shadows=True)

Sky()


class Block(Button):
    def __init__(self, **kwargs):
        global world_blocks
        super().__init__(
            parent=scene,
            position=(0, 0, 0),
            model='cube',
            origin_y=0,
            texture='stone',
            color=color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color=color.rgb(200, 200, 200)
        )
        # print(dir(super()))
        for key, value in kwargs.items():
            setattr(self, key, value)
        world_blocks[(self.position.x, self.position.y, self.position.z)]=self
    def input(self, key):
        global changing
        if self.hovered:
            if key == 'right mouse down':
                if distance(self, player) < 7:
                    changing=[(self.position.x+mouse.normal.x, self.position.y+mouse.normal.y, self.position.z+mouse.normal.z, 2)]
                    #block = Block(position=self.position + mouse.normal, color=color.white, texture='wood')
            if key == 'left mouse down':
                if distance(self, player) < 7:
                    #destroy(self)
                    changing=[(self.position.x, self.position.y, self.position.z, 0)]


s = socket.socket()
port = 25565
connect_ip = '127.0.0.1'
connect_ip='70.142.206.184'
s.connect((connect_ip, port))
fr = open('world.wld', 'rb')
list_blocks = pickle.load(fr)
world = {}
world_blocks={}
# 1 is for grass, 2 is wood, 3 is stone

for i in list_blocks:
    world[i] = 1
def update_world(already, to):
    global world_blocks
    for i in to:
        if not i in already or already[i] != to[i]:
            if to[i]==1:
                world_blocks[i]=Block(model='cube', color=color.green, texture="grass", position=(i[0], i[1], i[2]), collider='box')
            elif to[i]==2:
                world_blocks[i]=Block(model='cube', color=color.white, texture="wood", position=(i[0], i[1], i[2]), collider='box')
            elif to[i]==3:
                world_blocks[i]=Block(model='cube', color=color.white, texture="stone", position=(i[0], i[1], i[2]), collider='box')
            else:
                try:
                    destroy(world_blocks[i])
                except:
                    pass
update_world({}, world)

#for i in world:
#    Block(model='cube', color=color.green, texture="grass", position=(i[0], i[1], i[2]), collider='box')
changing=None
everybody=[]
def update():
    global world
    s.send(str(((player.position.x, player.position.y, player.position.z), changing)).encode())
    for i in everybody:
        destroy(i)
    adding=None
    subtracting=None
    all_players, world_new = eval(s.recv(1048576).decode())
    #print(world_new)
    #print(world==world_new)
    update_world(world, world_new)
    world=world_new
    for i in all_players:
        everybody.append(Entity(model='cube', position=all_players[i], color=color.white, texture='enimee', scale=(0.6, 2, 0.6)))

window.fullscreen=True
player = CustomPlayer()
app.run()
s.close()
