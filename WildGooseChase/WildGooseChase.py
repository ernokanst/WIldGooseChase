import os, pygame, random
 
 
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
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
all_sprites = pygame.sprite.Group()
sprite_image = load_image("image.png", -1)
sprite = pygame.sprite.Sprite(all_sprites)
sprite.image = sprite_image
sprite.rect = sprite.image.get_rect()
sprite.rect.x = 0
sprite.rect.y = 0
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	all_sprites.draw(screen)
	pygame.display.flip()
