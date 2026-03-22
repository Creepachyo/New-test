
from pygame import *

window = display.set_mode((700, 500))
display.set_caption('Maze')
background = transform.scale(image.load("background.jpg"), (700, 500))

#создай окно игры
game = True

clock = time.Clock()

speed = 4
x1 = 20
y1 = 400
 
x2 = 600
y2 = 300

x3 = 600
y3 = 400

FPS =  60

mixer.init()
# mixer.music.load('jungles.ogg')
mixer.music.play()

font.init()
font = font.Font(None, 70)
defeat = font.render('Поражение', True, (180, 0, 0))

class GameSprtite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.side = 'left'
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprtite):
    def update(self):
        keys_pressed = key.get_pressed()
        
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 695:
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y <= 400:
           self.rect.y += self.speed

class Enemy(GameSprtite):
    def update(self):
        if self.rect.x <= 470:
            self.side = 'right'
        if self.rect.x >= 635:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

player = Player('hero.png', x1, y1, speed)
enemy = Enemy("cyborg.png", x2, y2, speed)
finish = Player("treasure.png", x3, y3, speed)
wall = Wall(100, 100, 100, 150, 0, 10, 350)
wall1 = Wall(100, 100, 100, 250, 100, 10, 500)
wall2 = Wall(100, 100, 100, 250, 100, 150, 10)

end = False

while game:
 
    for e in event.get():
        if e.type == QUIT:
            game = False

    if end != True:
        window.blit(background, (0, 0))

        player.update()
        enemy.update()

        player.reset()
        enemy.reset()
        finish.reset()
        
        wall.draw_wall()
        wall1.draw_wall()
        wall2.draw_wall()

        if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, wall) or sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall2):
            window.blit(defeat, (200, 200))
            end = True

    display.update()
    clock.tick(FPS)

quit()
