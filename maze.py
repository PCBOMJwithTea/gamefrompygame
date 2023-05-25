#создай игру "Лабиринт"!
#создай тут фоторедактор Easy Editor!
from pygame import *
mixer.init()

window = display.set_mode((700,500))
display.set_caption("Лабиринт")
background = transform.scale(image.load("background.jpg"), (700, 500))
ghost1 = transform.scale(image.load('hero.png'), (100, 100))
ghost2 = transform.scale(image.load('cyborg.png'), (100, 100))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y >= 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y <= 430:
            self.rect.y += self.speed
        if keys_pressed[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x <= 630:
            self.rect.x += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        if self.rect.x <= 525:
            self.direction = 'right'
        if self.rect.x >= 625:
            self.direction = 'left'
            
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

clock = time.Clock()
FPS = 60

mixer.music.load('jungles.ogg')
mixer.music.play()

font.init()
font = font.SysFont('Arial', 70)
win = font.render('YOU WIN', True, (50, 199, 207))
lose = font.render('YOU LOSE', True, (82, 27, 27))

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

hero = Player('hero.png',50, 400, 10)
enemy = Enemy('cyborg.png', 625, 300, 3)
treasure = GameSprite('treasure.png', 430, 220, 0)
wall_1 = Wall(230, 200, 50, 150, 150, 10, 350)
wall_2 = Wall(230, 200, 50, 150, 150, 400, 10)
wall_3 = Wall(230, 200, 50, 530, 70, 10, 350)
wall_4 = Wall(230, 200, 50, 400, 280, 230, 10)
wall_5 = Wall(230, 200, 50, 250, 0, 10, 60)

finish = False

action = True
while action:
    for even in event.get():
        if even.type == QUIT:
            action = False
    
    if finish != True:
        window.blit(background, (0, 0))
        
        hero.reset()
        enemy.reset()
        treasure.reset()
        
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        wall_4.draw_wall()
        wall_5.draw_wall()

        enemy.update()
        hero.update()

        if sprite.collide_rect(hero, enemy) or sprite.collide_rect(hero, wall_1) or sprite.collide_rect(hero, wall_2) or sprite.collide_rect(hero, wall_3) or sprite.collide_rect(hero, wall_4) or sprite.collide_rect(hero, wall_5):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

        if sprite.collide_rect(hero, treasure):
            finish = True
            window.blit(win, (200, 200))
            money.play()

    clock.tick(FPS)
    display.update()