
import pygame
import sys
import os

import pygame.threads
from coundown import CountDown
from settings import Settings
from textRect import TextRect
from car import Car
from road import Road

class DragRacing:

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.threads.init()
        
        
        #self.settings = Settings(debug=input("To debug: 'd' >> ")=="d")
        self.settings = Settings()

        if self.settings.debug:
            self.screen = pygame.display.set_mode([700, 700])
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.display.set_caption("Drag Racing")
        pygame.display.set_icon(pygame.image.load('5/images/icon.jpg'))

        self.countdown = None
        self._predicted_winner=None
        
        if os.path.exists("5/score.txt"):
            with open("5/score.txt", 'rb') as file:
                self.score = int.from_bytes(file.read(), 'little')
        else: 
            self.score = 0

        self.frames=-1
        
        
        self.settings.status=Settings.ASK_STATUS
        self._cars=[None, None]

        self.exited = False

        self.thread = pygame.threads.Thread(target=self.game_cycle, name="main")
        self.thread.run()

    def game_cycle(self):
        while not self.exited:
            self._check_events()
            self._update_screen()
        else:
            self.save()
            sys.exit()

    def save(self):
        with open("5/score.txt", 'wb') as file:
            file.write(int.to_bytes(self.score, (self.score//2)+1, 'little'))

    def _check_events(self):
        event:pygame.event.Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save()
                pygame.quit()
                sys.exit()
            elif event.type ==pygame.KEYDOWN:
                self._check_down_events(event)
            elif event.type ==pygame.KEYUP:
                self._check_up_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                self._check_mouse_events(mousepos)

    def _check_down_events(self, event:pygame.event.Event):
        if event.key == pygame.K_ESCAPE:
            self.save()
            try:
                self.countdown.countdown="stop"
            except:
                pass
            self.exited = True


    def _check_up_events(self, event):
        pass

    def _check_mouse_events(self, mousepos):
        clicks = []
        if self.settings.status==Settings.ASK_STATUS:
            for button in self.buttons:
                clicks.append(button.rect.collidepoint(mousepos))
            for click in clicks:
                if click:
                    self._predicted_winner = clicks.index(True)+1
                    self.settings.status=Settings.COUNTDOWN_STATUS
        
        if self.settings.status==Settings.SHOW_WINNER_STATUS:
            click = self.play_again_button.rect.collidepoint(mousepos)
            if click:
                self.settings.status=Settings.ASK_STATUS


    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        if self.settings.status==Settings.COUNTDOWN_STATUS:
            
            if not (isinstance(self.countdown, CountDown)):
                self.countdown=CountDown(5)
            current = self.countdown.current
            if current>0:
                cd = TextRect(str(current), self, color=self.settings.button_color)
                cd.rect.center=self.screen.get_rect().center
                cd.update_pos()
                cd.draw()
            else:
                self.countdown.countdown="stop"
                self.countdown=None
                self.settings.status=Settings.GAME_STATUS
        elif self.settings.status==Settings.ASK_STATUS:
            self.ask_screen()
        
        elif self.settings.status==Settings.GAME_STATUS:
            self.game_screen()

        elif self.settings.status==Settings.SHOW_WINNER_STATUS:
            self.show_winner_screen()
        
        #draw score
        try:
            self.score_rect._prep_msg(str(self.score))
            self.score_rect.update_pos()
            self.score_rect.draw()
            
        except:
            self.score_rect = TextRect(str(self.score), self, size=[100, 50], color=self.settings.button_color)
            self.score_rect.rect.topleft = (10, 10)
            self.score_rect.update_pos()
            self.score_rect.draw()
            
        pygame.display.flip()

    def to_the_start(self):
        for car in self._cars:
            car.rect.left=10

    def game_screen(self):
        self.frames+=1
        if not isinstance(self._cars[0], Car):
            self._cars = [Car(self, '5/images/car1.png', size=[200, 120]), Car(self, '5/images/car2.png', size=[200, 120])]
            car1 = self._cars[0]
            car2 = self._cars[1]

            self.to_the_start()
            car1.rect.centery = 150
            car2.rect.centery = self.screen.get_rect().bottom-300

            self._roads = [Road(self, 250), Road(self, 250)]

            for road in self._roads:
                road.rect.centery = self._cars[self._roads.index(road)].rect.centery

            self.speeds =  [TextRect("Speed: 0", self, [200, 60], color=self.settings.button_color), TextRect("Speed: 0", self, [200, 60], color=self.settings.button_color)]
            for speed in self.speeds:
                speed.rect.centerx = self.screen.get_rect().centerx
                speed.rect.top = self._roads[self.speeds.index(speed)].rect.bottom+10
                speed.update_pos()

        #draw roads
        for road in self._roads:
            road.draw()
        
        #update and draw car
        for car in self._cars:
            if self.frames%30==0:
                car.set_random_speed()
                for i in range(2):
                    self.speeds[i]._prep_msg(f'Speed: {self._cars[i].speed}')
                    self.speeds[i].update_pos()

            if self.frames%3==0:
                car.move()
            finish = self.screen.get_rect().right-50
            if car.rect.collidepoint(finish, car.rect.centery):
                self.win(self._cars.index(car)+1)
            
            car.draw()
        
        #draw speeds of cars
        for speed in self.speeds:
            speed.draw()


    def ask_screen(self):
        screen_rect = self.screen.get_rect()

        question=TextRect("Who will win the race?", self, [500, 100], font = pygame.font.Font(None, 60), color=self.settings.button_color)
        question.rect.centerx=screen_rect.centerx
        question.rect.centery=200
        question.update_pos()
        question.draw()

        button1 = TextRect("1", self, [100, 100], font=pygame.font.Font(None, 40), color=self.settings.button_color)
        button1.rect.right = screen_rect.centerx-100
        button1.rect.top = question.rect.bottom+200
        button1.update_pos()

        button2 = TextRect("2", self, [100, 100], font=pygame.font.Font(None, 40), color=self.settings.button_color)
        button2.rect.left = screen_rect.centerx+100
        button2.rect.top = question.rect.bottom+200
        button2.update_pos()

        self.buttons = [button1, button2]

        button1.draw()
        button2.draw()

    def show_winner_screen(self):
        try:
            self.winner_rect._prep_msg(f'The winner is {self.winner}')
            self.winner_rect.update_pos()
            self.winner_rect.draw()

            self.points_rect._prep_msg(f'You got {self.score_received}')
            self.points_rect.update_pos()
            self.points_rect.draw()
            
            self.play_again_button.draw()
        except:
            self.winner_rect = TextRect(f'The winner is {self.winner}', self, [500, 100], font = pygame.font.Font(None, 60), color=self.settings.button_color)
            self.winner_rect.rect.centerx = self.screen.get_rect().centerx
            self.winner_rect.rect.top = 100
            self.winner_rect.update_pos()
            self.winner_rect.draw()

            self.points_rect = TextRect(f'You got {self.score_received}', self, [150, 60], color=self.settings.button_color)
            self.points_rect.rect.centerx = self.winner_rect.rect.centerx
            self.points_rect.rect.top = self.winner_rect.rect.bottom+40
            self.points_rect.update_pos()
            self.points_rect.draw()

            self.play_again_button = TextRect('Play again', self, [200, 70], font=pygame.font.Font(None, 30), color=self.settings.button_color)
            self.play_again_button.rect.centerx=self.winner_rect.rect.centerx
            self.play_again_button.rect.top=self.points_rect.rect.bottom+350
            self.play_again_button.update_pos()
            self.play_again_button.draw()
        

    def win(self, index):
        print(f'Winner is {index}')
        self.winner=index
        if self._predicted_winner==index:
            self.score_received = 10*(1000-(self._cars[index-1].rect.centerx-self._cars[index%2].rect.centerx))
        else:
            self.score_received= -7*(1000+(self._cars[index-1].rect.centerx-self._cars[index%2].rect.centerx))
        s = self.score
        self.score+=self.score_received
        if self.score<0:
            self.score_received=-s
            self.score = 0


        self.to_the_start()
        self.settings.status=Settings.SHOW_WINNER_STATUS