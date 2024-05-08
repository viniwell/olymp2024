
import pygame
import pygame.threads




class CountDown:
    init_thread = pygame.threads.init()
    def __init__(self, start:int) -> None:
        self.current = start
        self.thread = pygame.threads.Thread(target=self.countdown, name='countdown')
        self.thread.start()

    def countdown(self):
        while self.countdown!="stop":
            pygame.time.wait(1000)
            self.current-=1