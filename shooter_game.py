import pygame
from pygame import *
from random import randint
pygame.init()

mixer.init()
font.init()
font1 = font.Font(None, 36)

FPS = 90
clock = time.Clock()


speed_r = 8

lost = 0

kills = 0

hp = 3

boss_Time = False

window = display.set_mode((700, 500))
display.set_caption('Space_Invader')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def move_rocket(self):
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed

    def update(self):
        self.rect.y += self.speed 
        global lost, kills, hp, game
        if self.rect.y > 500:
            self.rect.x = randint(25, 650)
            self.rect.y = 0
            lost += 1

        collides = sprite.groupcollide(bullets, monsters, True, True)

        if sprite.spritecollide(rocket, monsters, True):
            hp -= 1
            ufo = GameSprite('ufo.png', randint(25, 650), 25, 50, 25, randint(1, 2))
            monsters.add(ufo)
            if hp == 0:
                window.blit(lose, (300, 200))
                game = False

        for collide in collides:
            ufo = GameSprite('ufo.png', randint(25, 650), 25, 50, 25, randint(1, 2))
            monsters.add(ufo)
            kills += 1

    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -50:
            self.kill()



background = GameSprite('galaxy.jpg', 0, 0, 700, 500, 0)

rocket = GameSprite('rocket.png', 350, 440, 50, 70, speed_r)

ufo = GameSprite('ufo.png', randint(25, 650), 25, 50, 25, randint(1, 2))
ufo1 = GameSprite('ufo.png', randint(25, 650), 25, 50, 25, 1)
ufo2 = GameSprite('ufo.png', randint(25, 650), 25, 50, 25, 1)
ufo3 = GameSprite('ufo.png', randint(25, 650), 25, 50, 25, randint(1, 2))
ufo4 = GameSprite('ufo.png', randint(25, 650), 25, 50, 25, 1)
monsters = sprite.Group()
monsters.add(ufo, ufo1, ufo2, ufo3, ufo4)

bullets = sprite.Group()

mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')


game = True


win = font1.render('YOY WIN', 1, (110, 220, 30))
lose = font1.render('YOU LOSE', 1, (210, 70, 35))


spisok = []
while game:
    background.reset()

    text_lose = font1.render(
        'Пропущено:' + str(lost), 1, (255,255,255)
    )
    window.blit(text_lose, (10, 10))

    text_kills = font1.render(
        'Убито:' + str(kills), 1, (255,255,255)
    )
    window.blit(text_kills, (10, 47))

    monsters.draw(window)
    monsters.update()

    if lost >= 15:
        window.blit(lose, (300, 200))
        game = False

    if kills == 30:
        window.blit(win, (300, 200))
        game = False

    keys = key.get_pressed()
    rocket.move_rocket()

    bullets.draw(window)
    bullets.update()

    rocket.reset()
        
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

    clock.tick(FPS)
    display.update()

