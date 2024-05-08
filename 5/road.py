import pygame

class Road:
    def __init__(self, game, height) -> None:
        self.game = game
        self.image = pygame.image.load('5/images/road.png')
        

        size = [self.game.screen.get_rect().width, height]
        
        self.image = pygame.transform.rotate(self.image, 90)

        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    
