import os
import pygame
import random
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QInputDialog


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            сolorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Dialog_Goose(QWidget):
    def __init__(self):
        super().__init__()

    def run(self):
        i, okBtnPressed = QInputDialog.getItem(self, "Выбор гуся",
                                               "Выберите гуся",
                                               ("goose.png", "goose-2.png",
                                                "goose-3.png"), 0, False)
        return i


goose = 'goose.png'
if __name__ == '__main__':
    app = QApplication(sys.argv)
    goose = Dialog_Goose()
    goose = goose.run()
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
all_sprites = pygame.sprite.Group()
sprite_image = load_image(goose)
sprite = pygame.sprite.Sprite(all_sprites)
sprite.image = sprite_image
sprite.rect = sprite.image.get_rect()
sprite.rect.x = 0
sprite.rect.y = 0
goose_move = 15
new_coords = 30
new_x = 0
new_y = 0
FPS = 50
clock = pygame.time.Clock()
pygame.time.set_timer(goose_move, 1)
pygame.time.set_timer(new_coords, 100)
running = True
while running:
    for event in pygame.event.get():
        if event.type == goose_move:
            if new_x > sprite.rect.x and new_y > sprite.rect.y:
                sprite.rect.x += 10
                sprite.rect.y += 10
            elif new_x > sprite.rect.x and new_y < sprite.rect.y:
                sprite.rect.x += 10
                sprite.rect.y -= 10
            elif new_x < sprite.rect.x and new_y > sprite.rect.y:
                sprite.rect.x -= 10
                sprite.rect.y += 10
            elif new_x < sprite.rect.x and new_y < sprite.rect.y:
                sprite.rect.x -= 10
                sprite.rect.y -= 10
        elif event.type == new_coords:
            new_x = random.randint(-250, 600)
            new_y = random.randint(-250, 400)
    screen.fill((255, 255, 255))
    clock.tick(FPS)
    all_sprites.draw(screen)
    pygame.display.flip()
