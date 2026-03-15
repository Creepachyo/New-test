#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer

mixer.init()
# mixer.music.load('space.ogg')
# mixer.music.play()

firesound = mixer.Sound('fire.ogg')

win_wid = 700
win_hei = 500

score = 0

lost_NPC = 0

max_lost = 4

max_score = 10

health = 5

clip = 5

flag_time = False

font.init()
main_font = font.Font(None, 40)
defeat_font = font.Font(None, 100)
defeat = defeat_font.render('Поражение', True, (255, 0, 0))
win_font = font.Font(None, 80)
win = win_font.render('Победа', True, (0, 255, 0))

FPS = 60

clock = time.Clock()

window = display.set_mode((win_wid, win_hei))
display.set_caption('Space war')
background = transform.scale(image.load('galaxy.jpg'), (win_wid, win_hei))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):

        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_wid - 80:
            self.rect.x += self.speed

    def fire(self):
        
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15, 15)
        bullets.add(bullet)
    
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        global lost_NPC

        if self.rect.y >= win_hei:
            self.rect.x = randint(80, win_wid - 80)
            self.rect.y = randint(-50, 0)
            lost_NPC += 1
        # if lost_NPC == max_lost:
            # print('lose')

class Bullet(GameSprite):

    def update(self):
        self.rect.y -= 15

        if self.rect.y < 0:
            self.kill()

player = Player('rocket.png' , 5, win_hei - 110, 80, 100, 15)
enemies = sprite.Group()
asteroids = sprite.Group()

for i in range(1,5):
    enemy = Enemy('ufo.png', randint(80 , win_wid - 80), -40, 80, 50, randint(1,2))
    enemies.add(enemy)

for i in range(1, 4):
    asteroid = Enemy('asteroid.png', randint(40 , win_wid - 40), randint(40 , win_hei - 40), 40, 40, randint(1 ,2))
    asteroids.add(asteroid)
    
bullets = sprite.Group()

finish = False

run = True 

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if clip > 0 and flag_time == False:
                    player.fire()
                    firesound.play()
                    clip -= 1
                else:
                    last_time = timer()
                    flag_time = True
            
                    
    if finish == False:
        window.blit(background, (0, 0))

        text_score = main_font.render(f'Счёт:{score}', True, (255, 255, 255))
        lost_NPC_score = main_font.render(f'Пропущено:{lost_NPC}', True, (255, 255, 255))
        text_health = main_font.render(f'Здоровье:{health}', True, (255 ,255, 255))
        window.blit(text_score, (5, 20))
        window.blit(lost_NPC_score, (5, 50))
        window.blit(text_health, (5, 80))

        player.update()
        enemies.update()
        bullets.update()
        asteroids.update()

        player.reset()
        enemies.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if flag_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = main_font.render('Перезарядка', True, (255, 255, 255))
                window.blit(reload_text, (5, 110))
            else:
                flag_time = False
                clip = 5

        collides = sprite.groupcollide(enemies, bullets, True, True)

        if sprite.spritecollide(player, asteroids, True):
            health -= 1
        elif sprite.spritecollide(player, enemies, True):
            health -= 5

        for i in collides:
            score += 1
            print(i)
        
        if lost_NPC == max_lost or health <= 0:
            window.blit(defeat, (150, 200))
            finish = True
        elif score == max_score:
            window.blit(win, (250, 200))
            finish = True
        
    display.update()
    clock.tick(FPS)
    