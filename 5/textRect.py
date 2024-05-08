import pygame

class TextRect:
    init = pygame.font.init()
    basic_font = pygame.font.Font(None, 24)

    def __init__(self, msg, game, size=[100, 100], color=(0, 0, 0), text_color=(255, 255, 255), font=basic_font) -> None:
        self.game = game
        self.size=size
        self.color=color
        self.text_color=text_color
        self.font=font

        self.rect=pygame.Rect(0, 0, *self.size)
        self._prep_msg(msg)


    def _prep_msg(self, msg):
        self.msg_image=self.font.render(msg, True, self.text_color, self.color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.update_pos()

    def draw(self):
        self.game.screen.fill(self.color, self.rect)
        self.game.screen.blit(self.msg_image, self.msg_image_rect)

    def update_pos(self):
        self.msg_image_rect.center=self.rect.center