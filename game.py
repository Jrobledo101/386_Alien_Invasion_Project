import pygame as pg
from settings import Settings
import game_functions as gf
import time
from os import path

from ship import Ship
from alien import Aliens
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sound import Sound
from barrier import Barriers

HS_FILE = "HighScores.txt"

class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Alien Invasion")
        self.font = pg.font.SysFont(None, 48)
        self.text = self.font.render('500', True, (255,255,255), (0,0,0))
        self.textRect = self.text.get_rect()
        self.textRect.center = (400, 200)
        ship_image = pg.image.load('images/ship.bmp')
        self.ship_height = ship_image.get_rect().height
        self.hs = 0
        self.sound = Sound(bg_music="sounds/music.wav")
        self.sound.play()
        self.sound.pause_bg()
        self.play_button = self.aliens = self.stats = self.sb = self.ship = None
        self.restart()
        self.finished = False
        self.title = True
        self.scorescreendisplay = False
        self.highscorelist = []

    def textset(self, text, posx, posy):
        self.texttodisplay = self.font.render(text, True, (255,255,255), (0,0,0))
        self.screen.blit(self.texttodisplay, (posx, posy))

    def title_screen(self):
        gf.check_events(stats=self.stats, play_button=self.play_button, ship=self.ship, sound=self.sound, game=self)
        while self.title:
            self.screen.fill(self.settings.bg_color)
            self.sound.pause_bg()
            self.screen.blit(pg.image.load('images/alien00.png'),(500,150))
            self.screen.blit(pg.image.load('images/alien10.png'), (500, 250))
            self.screen.blit(pg.image.load('images/alien20.png'), (500, 350))
            self.textset('100', 600, 370)
            self.textset('300', 600, 270)
            self.textset('500', 600, 170)
            self.textset('Press SPACE to begin', 430, 450)
            self.textset('Press \'H\' to view high scores', 380, 550)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.title = False
                        self.play()
                    elif event.key == pg.K_h:
                        self.title = False
                        self.scorescreendisplay = True
                        self.score_screen()

    def score_screen(self):
        while self.scorescreendisplay:
            self.screen.fill(self.settings.bg_color)
            self.textset('High Scores:', 500, 50)
            self.textset('Press esc to exit', 450, 700)
            self.textset(f'{self.hs} ', 600, 100)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.scorescreendisplay = False
                        self.title = True
                        self.title_screen()

    def scores(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.stats.high_score = int(f.read())
                self.hs = self.stats.high_score
            except:
                self.hs = -1000000
        print(f'High score was {self.hs}')

    def restart(self):
        self.play_button = Button(settings=self.settings, screen=self.screen, msg="Play")
        self.hs_button = Button(settings=self.settings, screen=self.screen, msg="High Scores")
        self.stats = GameStats(settings=self.settings)
        self.sb = Scoreboard(game=self, sound=self.sound)
        self.settings.init_dynamic_settings()

        self.barriers = Barriers(game=self)
        self.aliens = Aliens(ship_height=self.ship_height, game=self, barriers=self.barriers)
        self.ship = Ship(aliens=self.aliens, sound=self.sound, game=self, barriers=self.barriers)
        self.aliens.add_ship(ship=self.ship)
        self.stats.high_score = self.hs
        self.sb.prep_high_score()


    def printscores(self):
        f = open('HighScores.txt', 'r')

        for line in f:
            saved_score = line.strip()
            self.highscorelist.append(saved_score)

        for saved_score in self.highscorelist:
            print(saved_score)

    def play(self):
        while not self.finished:
            gf.check_events(stats=self.stats, play_button=self.play_button, ship=self.ship, sound=self.sound, game=self)
            if not self.title:
                self.ship.update()
                self.aliens.update()
                self.barriers.update()

            self.screen.fill(self.settings.bg_color)
            self.ship.draw()
            self.aliens.draw()
            self.barriers.draw()
            self.sb.show_score()
            if not self.sound.playing_bg: self.sound.unpause_bg()
            pg.display.flip()

    def reset(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.aliens.create_fleet()
            self.ship.center_ship()
            time.sleep(0.5)
            self.ship.timer = Ship.timer
        else:
            self.stats.game_active = False
            self.sound.pause_bg()
            self.hs = self.stats.high_score
            self.restart()

    def savescore(self):
        f = open("HighScores.txt", "w")
        f.write(str(self.stats.high_score))
        f.write("\n")

def main():
    g = Game()
    g.scores()
    g.title_screen()
    print(f'High score was {g.stats.high_score}')
    g.savescore()
    g.printscores()
    # Vector.run_tests()
    # Quaternion.run_tests()
    # Matrix.run_tests()
    # Alien.run_tests()


if __name__ == '__main__':
    main()
