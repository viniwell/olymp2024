import pygame
import random

class Car:
    def __init__(self, game, filename, size=[200, 60], ) -> None:
        self.game = game
        self.image = pygame.image.load(filename)
        
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.speed = 0


    def set_random_speed(self):
        self.speed = random.randint(1, 20)

    def move(self):
        self.rect.centerx += self.speed

    def draw(self):
        self.game.screen.blit(self.image, self.rect)


    
