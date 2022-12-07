from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise

app = Ursina()

grass_texture = load_texture('assets/grass_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
brick_texture = load_texture('assets/brick_block.png')
stone_texture = load_texture('assets/stone_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/punch_sound', loop = False, autoplay = False)

window.exit_button.visible = False
window.fps_counter.enabled = False

block_pick = 1

seedVar = random.randint(1, 3000)
octaveVar = random.randint(1, 5)
noise = PerlinNoise(octaves=octaveVar, seed=seedVar)

player = FirstPersonController()

player.speed = 5
 
def update():
    global block_pick

    if held_keys['left mouse'] or held_keys['right mouse']: 
        hand.active()
    else:
        hand.passive()

    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4

    if held_keys['left shift']: 
        player.speed = 8
    else:
        player.speed = 5




def input(key):
    if key == 'escape':
       sys.quit() 


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm',
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(150, -10, 0),
            position = Vec2(0.4, -0.6)
        )

    def active(self):
        self.position = Vec2(0.3, -0.5)
    
    def passive(self):
        self.position = Vec2(0.4, -0.6)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = sky_texture,
            scale = 150,
            double_sided = True
        )

class Voxel(Button):
    def __init__(self, position, texture = grass_texture):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            origin_y = 0.5,
            texture = texture,
            color = color.color(0, 0, random.uniform(0.9,1)),
            scale = 0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
                if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
                if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
                if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
           
            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)


amp = 6
freq = 24

for z in range(-20, 20):
    for x in range(-20, 20):
        y = floor(noise([x/freq, z/freq])*amp)
        voxel = Voxel(position = (x, y, z))



sky = Sky()
hand = Hand()

app.run()