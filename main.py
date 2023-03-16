import pygame
import neat
import time
import os
import random

pygame.init()

pygame.display.set_caption("FlappyBird")

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("Assets", "imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("Assets", "imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("Assets", "imgs", "bird3.png")))]
PIPE_IMG = pygame.image.load('Assets/imgs/pipe.png')
BASE_IMG = pygame.image.load('Assets/imgs/base.png')
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "imgs","bg.png")).convert_alpha(), (500, 800))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.image_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, screen):
        self.image_count += 1

        if self.image_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.image_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.image_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.image_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.image_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.image_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.image_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        screen.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def draw_screen(screen, bird):
    screen.blit(BG_IMG, (0, 0))
    bird.draw(screen)
    pygame.display.update()


def main():
    bird = Bird(200, 200)

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_screen(screen, bird)

    pygame.quit()
    quit()

main()