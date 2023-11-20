from pyglet.window import Window
from pyglet.app import run
from pyglet.text import Label
from pyglet import font
from pyglet import clock
from pyglet.shapes import Line,Rectangle

import random
import math

class Renderer(Window):
    def __init__(self, game):
        self.game = game
        super().__init__()
        font.add_file('/Users/karandeepsinghnanda/Documents/VSCode/Backdrop-Repo/joystix monospace.otf')
        font.load('Joystix', 16)
        self.laser_x = self.width /5
        self.laser = Line(
            self.laser_x,
            0,
            self.laser_x,
            self.height,
            color =(214,93,177,255)
        )
        self.shake_animation_time = 0
        self.stars = []
        for n in range(20):
            self.stars.append(Rectangle(
                random.randint(0, self.width),
                random.randint(0, self.height),
                4,4,
                color =(132,94,194,255))
            )
        
    def start(self):
            
        """define the start position of the word on the screen"""
        self.game.new_round()
        self.characters = []
        self.confetti = []
        x = self.width
        y = random.randint(self.height / 4 , self.height / 4 * 3) #Randomize the height of the words to appear
        for t in self.game.word:
            self.characters.append(Label(
                t,font_size=24,
                x=x,
                y=y,
                font_name='Joystix',
                anchor_x='center',
                color=(255,199,95,255)))
            x = x + 32
            
    def on_draw(self):
        """ as seen on the screen"""
        self.clear() #blank window
        self.laser.draw()
        for c in self.characters:
            c.draw()
        for c in self.confetti:
            c.draw()
        for s in self.stars:
            s.draw()
            
    
    def on_update(self, dt):
        """
        updating the screen with moving words and confetti
        """
        
        for c in self.characters:
            c.x -= 100 * dt
        if self.characters[0].x < self.laser_x + 12: #+12 for the left alignment of the characters
            self.start()
        for c in self.confetti:
            c.update(dt)
        if self.shake_animation_time > 0:
            self.shake_animation_time -= dt
            self.characters[0].rotation = math.sin(self.shake_animation_time * 50) * 20
        else:
            self.characters[0].rotation = 0
        for s in self.stars:
            s.x += dt * 20
            if s.x > self.width:
                s.x = 0
                
                
    def on_key_press(self, symbol, modifiers):
        """
        update the characters after a correct key press
        """
        
        key = chr(symbol).upper()
        if self.game.check_key(key):
            character = self.characters[0]
            if self.game.word:
                self.characters  = self.characters[1:]
        
            else:
                self.start()
            self.confetti.append(Confetti(character.x, character.y))
        
        else:
            self.shake_animation_time = .3 #300 ms
            

class Game:
    def __init__(self):
        self.words = ["SUN", "FLOWER", "SWIMMING", "POOL", "FISH", "BATHING SUIT", "TOWEL"]
    
    def new_round(self):
        self.word = random.choice(self.words)
        
    def check_key(self,character):
        if character == self.word[0]:
            self.word = self.word[1:]
            return True
        
        return False
    
    
class Confetti:
    def __init__(self,x,y):
        self.confetti = [
            Rectangle(x, y, 10, 10, color=(132, 94, 194, 255)),
            Rectangle(x, y, 10, 10, color=(214, 93, 177, 255)),
            Rectangle(x, y, 10, 10, color=(255, 150, 113, 255)),
            Rectangle(x, y, 10, 10, color=(249, 248, 113, 255)),
        ]
        self.y = y + 50 
        self.animation_time = -2
        self.directions_x = [random.random() * -10 for c in self.confetti]
        self.speeds = [random.random() * 2 + 2 for c in self.confetti]
    
    
    def draw(self):
        for c in self.confetti:
            c.draw()
            
            
    def update(self,dt):
        self.animation_time += dt *20
        for c,d,s in zip(self.confetti, self.directions_x, self.speeds):
            c.y = self.y - self.animation_time ** 2 * s # to start with: c.y = self.y - self.animation_time ** 2
            c.x += d * dt * 10


game = Game()
renderer = Renderer(game)
renderer.start()
clock.schedule(renderer.on_update)
run()

    
            
            