import pygame as pg
import numpy as np
import random
import copy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 125, 0)
BLUE = (0, 0, 128)


class Game:
    def __init__(self, size=[30, 30], size_square=20, len=4, speed=1):
        self.size = np.array(size)  # Size of the grid
        self.size_square = size_square  # Size of each square of the grid
        self.screen = pg.display.set_mode(size=tuple(self.size_square * self.size))
        self.caption = pg.display.set_caption("SNAKE")
        self.speed = speed
        self.directions = {
            "LEFT": np.array([-self.speed, 0]),
            "RIGHT": np.array([self.speed, 0]),
            "UP": np.array([0, -self.speed]),
            "DOWN": np.array([0, self.speed]),
        }
        # Note that the x coordinate corresponds to the columns index and the y coordinate to the rows index
        self.target = [
            random.choice(range(self.size[1])),
            random.choice(range(self.size[0])),
        ]
        # Initialization of snake
        self.len = len
        self.dir = self.directions["RIGHT"]
        self.head = np.array([int(size[0] / 2), int(size[1] / 2)])  # middle poin
        self.body = [self.head - i * self.dir for i in range(len)]
        self.game_over = False

    def new_target(self):
        self.target = [
            random.choice(range(self.size[1])),
            random.choice(range(self.size[0])),
        ]

    def key_input(self):
        # Read key input and convert it into a direction array
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            self.change_dir(self.directions["LEFT"])
        elif key[pg.K_RIGHT]:
            self.change_dir(self.directions["RIGHT"])
        elif key[pg.K_UP]:
            self.change_dir(self.directions["UP"])
        elif key[pg.K_DOWN]:
            self.change_dir(self.directions["DOWN"])

    def change_dir(self, newDir):
        # Control the snake
        if (newDir != -self.dir).all():
            self.dir = newDir

    def is_touching(self):
        for _, body_element in enumerate(self.body[1:]):
            if (self.head == body_element).all():
                self.game_over = True

    def move(self):
        self.key_input()
        self.head = (self.head + self.dir) % self.size
        tail = self.body[-1]
        self.body = [self.head] + self.body[:-1]
        # If the snake eats the target than it grows
        if (self.head == self.target).all():
            self.body = self.body + [tail]
            self.new_target()
        self.len = len(self.body)
        if self.is_touching():
            self.print_score()

    def draw(self):
        # draw snake
        if not self.game_over:
            for _, [x, y] in enumerate(self.body):
                RECT = pg.rect.Rect(
                    (
                        x * self.size_square,
                        y * self.size_square,
                        self.size_square,
                        self.size_square,
                    )
                )
                pg.draw.rect(self.screen, GREEN, RECT)
            # draw target
            TARGET = pg.rect.Rect(
                (
                    self.target[0] * self.size_square,
                    self.target[1] * self.size_square,
                    self.size_square,
                    self.size_square,
                )
            )
            pg.draw.rect(self.screen, RED, TARGET)
        # If game is over print score
        else:
            font = pg.font.Font(None, 50)
            message = "Your score is " + str(self.len)
            img = font.render(message, True, WHITE)
            self.screen.blit(img, (30, 30))


def main():
    # Initialization
    clock = pg.time.Clock()
    pg.init()
    myGame = Game()
    # Game loop
    while True:
        myGame.screen.fill(BLACK)
        for event in pg.event.get():
            if (
                event.type == pg.QUIT
            ):  # The user pressed the close button in the top corner of the window.
                quit()
        myGame.move()
        myGame.draw()
        pg.display.update()
        clock.tick(10)


main()
