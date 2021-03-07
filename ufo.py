import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from pygame.sprite import Group
from bullet import BulletFromAlien
from random import randint


class Ufo:
    def __init__(self, ship_height, game, barriers):
        self.settings = game.settings
        self.screen = game.screen
        self.ufo_height = ufo_height
        self.game = game

    def create(self):
        settings, screen = self.settings, self.screen
        ufo = Ufo(parent=self, game=self.game)


class Alien(Sprite):   # INHERITS from SPRITE
    images = [[pg.image.load('images/alien' + str(number) + str(i) + '.png') for i in range(2)] for number in range(3)]
    images_boom = [pg.image.load('images/explosion_' + str(i) + '.png') for i in range(9)]

    timers = []
    for i in range(3):
        timers.append(Timer(frames=images[i], wait=700))
    timer_boom = Timer(frames=images_boom, wait=10, looponce=True)

    def __init__(self, game, parent, number=0, x=0, y=0, speed=0):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.game = game
        self.parent = parent
        self.number = number
        self.update_requests = 0
        self.dead, self.reallydead, self.timer_switched = False, False, False

        self.timer = Alien.timers[number]
        self.rect = self.timer.imagerect().get_rect()
        self.rect.x = self.x = x
        self.rect.y = self.y = y
        self.x = float(self.rect.x)
        self.speed = speed
        self.damage = 0

    def check_edges(self):
        r, rscreen = self.rect, self.screen.get_rect()
        return r.right >= rscreen.right or r.left <= 0

    def killed(self):
        if self.dead and not self.timer_switched:
            self.game.stats.score += self.settings.alien_points0 * 3
            self.timer = Timer(frames=Alien.images_boom, wait=50, looponce=True)
            self.timer_switched = True
            self.game.sb.check_high_score(self.game.stats.score)
            self.game.sb.prep_score()



    def update(self):
        if self.dead and self.timer_switched:
            if self.timer.frame_index() == len(Alien.images_boom) - 1:
                self.dead = False
                self.timer_switched = False
                self.reallydead = True
                self.parent.remove(self)
                self.timer.reset()
        delta = self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x += delta
        self.x = self.rect.x

    def draw(self):
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
