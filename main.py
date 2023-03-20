import pygame
import neat
import time
import os
import random

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
FPS = 30

pygame.display.set_caption("FlappyBird")

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("Assets", "imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("Assets", "imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("Assets", "imgs", "bird3.png")))]
PIPE_IMG = pygame.image.load('Assets/imgs/pipe.png')
PIPE_IMG = pygame.transform.scale(PIPE_IMG, (PIPE_IMG.get_width() * 2, PIPE_IMG.get_height() * 2))
BASE_IMG = pygame.image.load('Assets/imgs/base.png')
BASE_IMG = pygame.transform.scale(BASE_IMG, (BASE_IMG.get_width() * 2, BASE_IMG.get_height() * 2))
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "imgs", "bg.png")).convert_alpha(), (500, 800))

STAT_FONT = pygame.font.SysFont("corbel", 50)


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


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.top))
        screen.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        botttom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(botttom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMG, (self.x1, self.y))
        screen.blit(self.IMG, (self.x2, self.y))


def draw_screen(screen, bird, pipes, base, score):
    screen.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(screen)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))

    base.draw(screen)
    bird.draw(screen)
    pygame.display.update()


def main(genomes, config):
    nets = []
    ge = []
    birds = []

    for g in genomes:
        net = neat.nn.FeedForwardNetwork(f, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)


    base = Base(730)
    pipes = [Pipe(600)]

    score = 0

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() > 730:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_screen(screen, bird, pipes, base, score)

    pygame.quit()
    quit()


main()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, congig_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main ,50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    congig_path = os.path.join(local_dir, "config_feedforward.txt")
    run(congig_path)
