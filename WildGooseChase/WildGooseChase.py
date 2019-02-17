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


class Goose(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def caught(self, coords):
        global count
        global score
        if self.rect.collidepoint(coords):
            score.play()
            count += 1


class Cursor(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('cursor.png')
        self.rect = self.image.get_rect()

    def movement(self, coords):
        self.rect.topleft = coords


class Dialog_Goose(QWidget):
    def __init__(self):
        super().__init__()

    def run(self):
        i, okBtnPressed = QInputDialog.getItem(self, "Выбор гуся",
                                               "Выберите гуся",
                                               ("goose.png", "goose-2.png",
                                                "goose-3.png"), 0, False)
        return i


goose_image = 'goose.png'
if __name__ == '__main__':
    app = QApplication(sys.argv)
    goose_image = Dialog_Goose()
    goose_image = goose_image.run()
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
all_sprites = pygame.sprite.Group()
goose = Goose(all_sprites, goose_image)
cursor = Cursor(all_sprites)
goose_move = 1
new_coords = 2
honking = 3
count = 0
new_x = 0
new_y = 0
FPS = 50
clock = pygame.time.Clock()
honk = pygame.mixer.Sound(os.path.join('data', 'Honk.wav'))
pygame.time.set_timer(goose_move, 10)
pygame.time.set_timer(new_coords, 100)
pygame.time.set_timer(honking, 10000)
pygame.mouse.set_visible(False)
score = pygame.mixer.Sound(os.path.join('data', 'score.wav'))
pygame.mixer.music.load(os.path.join('data', 'Music.mp3'))
pygame.mixer.music.play(-1)
running = True
while running:
    for event in pygame.event.get():
        if event.type == goose_move:
            if new_x > goose.rect.x and new_y > goose.rect.y:
                goose.rect.x += 5
                goose.rect.y += 5
            elif new_x > goose.rect.x and new_y < goose.rect.y:
                goose.rect.x += 5
                goose.rect.y -= 5
            elif new_x < goose.rect.x and new_y > goose.rect.y:
                goose.rect.x -= 5
                goose.rect.y += 5
            elif new_x < goose.rect.x and new_y < goose.rect.y:
                goose.rect.x -= 5
                goose.rect.y -= 5
            else:
                new_x = random.randint(0, 800)
                new_y = random.randint(0, 600)
        elif event.type == new_coords:
            new_x = random.randint(0, 800)
            new_y = random.randint(0, 600)
        elif event.type == pygame.MOUSEMOTION:
            cursor.movement(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            goose.caught(event.pos)
        elif event.type == honking:
            honk.play()
    fon = pygame.transform.scale(load_image('fon.png'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(os.path.join('data', 'PTMono.ttc'), 30)
    text_coord = 10
    string_rendered = font.render('Попаданий: ' + str(count), 1,
                                  pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 10
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    clock.tick(FPS)
    all_sprites.draw(screen)
    pygame.display.flip()
