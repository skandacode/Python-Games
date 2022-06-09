from ursina import *
app = Ursina()
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from CustomPlayer import CustomPlayer
import pickle, socket
Entity.default_shader = lit_with_shadows_shader
#DirectionalLight(parent=scene, y=2, z=3, shadows=True)
Sky()
class Block(Button):
    def __init__(self, **kwargs):
        super().__init__(
            parent = scene,
            position = (0, 0, 0),
            model = 'cube',
            origin_y = 0,
            texture = 'stone',
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.rgb(200, 200, 200)
        )
        #print(dir(super()))
        for key, value in kwargs.items():
            setattr(self, key ,value)


    def input(self, key):
        global player, blocks, holding, INVENTORY
        if self.hovered:
            if key == 'right mouse down':
                if not self.position + mouse.normal in blocks and not self.position + mouse.normal==Vec3(round(player.position.x), round(player.position.y+0.5), round(player.position.z)) and not self.position + mouse.normal==Vec3(round(player.position.x), round(player.position.y+1.5), round(player.position.z)):
                    if INVENTORY[holding]>0 and distance(self, player)<7:
                        block = Block(position=self.position + mouse.normal, color=color.white, texture=holding)
                        blocks[block.position]=blocks
                        INVENTORY[holding]-=1
                        print(self.texture)
            if key == 'left mouse down':
                if (self.texture).__repr__().split('.')[0] in INVENTORY and distance(self, player)<7:
                    del blocks[self.position]
                    destroy(self)
                    INVENTORY[(self.texture).__repr__().split('.')[0]]+=1
fr=open('world.wld', 'rb')
loading=True
holding='wood'
INVENTORY={'wood':100000, 'stone':10, 'long_range':{}, 'melee':[]}
hand = Entity(model='cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.red, on_cooldown=False, rotation_x=10)
holdingdisplay = Entity(parent=hand, y=0.5, z=1, world_scale=.4, model='cube', texture=holding, enabled=True)
inventory_dis=Entity(parent=camera.ui, model='quad', texture='inventory', enabled=True, scale=(0.7, 0.07, 0.7), position=(-0.1, -0.4, 1))
list_blocks=pickle.load(fr)
fr.close()
blocks= {}
count=0
deaths=0
kills=0
players=[]
s = socket.socket()
port = 32477
connect_ip='127.0.0.1'
s.connect((connect_ip, port))
if loading:
    for i in list_blocks:
        b=Block(model='cube', color=color.green, texture="grass", position=(i[0], i[1], i[2]), collider='box')
        blocks[b.position]=b
        count+=1
        if count%100==0:
            print(count)
del count
def update():
    try:
        for i in players:
            destroy(i)
    except:
        pass
    players=[]
    print(player.position, camera.rotation, held_keys['left mouse down'], held_keys['right mouse down'])
    s.send(bytes(str((player.position.x, player.position.y, player.position.z)), 'utf-8'))
    if player.position.y<-100:
        player.position=Vec3(0, 2, 0)
        try:
            deaths+=1
        except:
            pass
    
    recieve_data=eval(s.recv(1048576).decode())
    for i in recieve_data:
        p_pos=recieve_data[i]
        players.append(Entity(model='cube', texture='enimee', position=p_pos))
    if held_keys['escape']:
        mouse.visible=True
        
        raise Exception('Keeky', random.choice(['dumb', 'annoying', 'stupid']))
window.fullscreen=True
player = CustomPlayer()
player.speed=10
player.position=(0, 3, 0)
#player.fall_after=0.5

app.run()
