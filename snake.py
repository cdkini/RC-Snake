import copy
import pyautogui as pag
import pygame
import random
import sys
import time

from attribute_dicts import colors, dimensions


pygame.init()
display = pygame.display.set_mode((dimensions["WIDTH"], dimensions["HEIGHT"]))
pygame.display.set_caption("PySnake!")

class Snake:
    '''
    Snake object player controls during each game.
    '''
    def __init__(self, x_start, y_start):
        self.x_start = x_start
        self.y_start = y_start
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x_start, self.y_start]]
        self.length = 1

    def reset(self):
        '''
        Sets user controlled Snake obj back at starting
        point and score by refreshing attributes given at __init__.

        Args:
            None
        
        Returns:
            None
        '''
        self.x_start = dimensions["WIDTH"] / 2 
        self.y_start = dimensions["HEIGHT"] / 2 
        self.x_dir = 1
        self.y_dir = 0
        self.history = [[self.x_start, self.y_start]]
        self.length = 1

    def show(self):
        '''
        Displays user controlled Snake obj by drawing rectangles
        based on given Snake length.

        Args:
            None

        Returns:
            None
        '''
        for i in range(self.length):
            if not i % 2:
                pygame.draw.rect(
                    display, 
                    colors["SNAKE_Y"], 
                    (self.history[i][0], self.history[i][1], dimensions["SCALE"], dimensions["SCALE"])
                )
            else:
                pygame.draw.rect(
                    display, 
                    colors["SNAKE_B"], 
                    (self.history[i][0], self.history[i][1], dimensions["SCALE"], dimensions["SCALE"])
                )

    def check_eaten(self):
        '''
        Evaluates whether or not a user controlled Snake obj has collided
        with a randomly generated Food obj.

        Args:
            None

        Returns:
            True (bool): Only returned if collision occurs.
        '''
        if abs(self.history[0][0] - dimensions["FOOD_X"]) < dimensions["SCALE"] and \
            abs(self.history[0][1] - dimensions["FOOD_Y"]) < dimensions["SCALE"]:
                return True

    def grow(self):
        '''
        Increments the length of a user controlled Snake obj.

        Args:
            None

        Returns:
            None
        '''
        self.length += 1
        self.history.append(self.history[self.length - 2])

    def death(self):
        '''
        Determines whether or not the user controlled Snake obj
        has collided with itself.

        Args:
            None
        
        Returns:
            True (bool): Only returned if Snake obj has collided with itself.
        '''
        i = self.length - 1
        while i > 0:
            if abs(self.history[0][0] - self.history[i][0]) < dimensions["SCALE"] and \
            abs(self.history[0][1] - self.history[i][1]) < dimensions["SCALE"] and self.length > 2:
                return True
            i -= 1

    def update(self):
        '''
        Updates user controlled Snake obj's self.history.

        Args:
            None
        
        Returns:
            None
        '''
        i = self.length - 1
        while i > 0:
            self.history[i] = copy.deepcopy(self.history[i-1])
            i -= 1
        self.history[0][0] += self.x_dir * dimensions["SCALE"]
        self.history[0][1] += self.y_dir * dimensions["SCALE"]


class Food:
    '''
    Object the user controlled Snake obj interacts with to obtain points.
    '''
    def new_location(self):
        '''
        Randomly generates Food obj on pygame.display grid.

        Args:
            None

        Returns:
            None
        '''
        dimensions["FOOD_X"] = random.randrange(
            1, dimensions["WIDTH"] / dimensions["SCALE"] - 1) * dimensions["SCALE"]

        dimensions["FOOD_Y"] = random.randrange(
            1, dimensions["HEIGHT"] / dimensions["SCALE"] - 1) * dimensions["SCALE"]

    def show(self):
        '''
        Displays Food obj by drawing a rectangle at 
        the coordinates set by Food.new_location().

        Args:
            None
        
        Returns:
            None
        '''
        pygame.draw.rect(
            display,
            colors["FOOD"],
            (dimensions["FOOD_X"], dimensions["FOOD_Y"], dimensions["SCALE"], dimensions["SCALE"])
        )


def show_score():
    '''
    Displays user's score on top left of screen.

    Args:
        None
    
    Returns:
        None
    '''
    font = pygame.font.SysFont("Garamond", 15)
    text = font.render("Score: " + str(score), True, colors["SNAKE_Y"])
    display.blit(text, (dimensions["SCALE"], dimensions["SCALE"]))

user_scores = []

def main():

    global score
    score = 0

    player = Snake(dimensions["WIDTH"] / 2, dimensions["HEIGHT"] / 2)
    food = Food()
    food.new_location()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pag.prompt(text="Please input your name.", title='User')
                    pygame.quit()
                    sys.exit()

                if player.y_dir == 0:
                    if event.key == pygame.K_UP:
                        player.x_dir = 0
                        player.y_dir = -1
                    if event.key == pygame.K_DOWN:
                        player.x_dir = 0
                        player.y_dir = 1

                if player.x_dir == 0:
                    if event.key == pygame.K_LEFT:
                        player.x_dir = -1
                        player.y_dir = 0
                    if event.key == pygame.K_RIGHT:
                        player.x_dir = 1
                        player.y_dir = 0

        display.fill(colors["BACKGROUND"])

        player.show()
        player.update()
        food.show()
        show_score()

        if player.check_eaten():
            food.new_location()
            score += 1
            player.grow()

        if player.death():
            user_name = input('Please input your name: ')
            user_scores.append((user_name, score))
            score = 0
            font = pygame.font.SysFont("Garamond", 25)
            text = font.render("Game over!", True, colors["MESSAGE"])
            display.blit(text, (int(dimensions["WIDTH"] / 2 - 60), int(dimensions["HEIGHT"] / 2)))
            pygame.display.update()
            time.sleep(3)
            player.reset()

        if player.history[0][0] > dimensions["WIDTH"]:
            player.history[0][0] = 0
        if player.history[0][0] < 0:
            player.history[0][0] = dimensions["WIDTH"]

        if player.history[0][1] > dimensions["HEIGHT"]:
            player.history[0][1] = 0
        if player.history[0][1] < 0:
            player.history[0][1] = dimensions["HEIGHT"]


        pygame.display.update()
        pygame.time.Clock().tick(30) # Speed or difficulty of the game.
    

if __name__=="__main__":
    main()
    print(user_scores)
