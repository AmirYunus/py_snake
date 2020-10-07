import math
import random
import pygame
import tkinter
from tkinter import messagebox

width = 500
rows = 20

class cube_object(object):
    width = width
    rows = rows

    def __init__(self, start, direction_x = 1, direction_y = 0, colour = (255,0,0)):
        self.position = start
        self.direction_x = 1
        self.direction_y = 0
        self.colour = colour

    def move (self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.position = (self.position[0] + self.direction_x, self.position[1] + self.direction_y)

    def draw(self, window, eyes = False):
        distance = width // rows
        x_coordinate = self.position[0]
        y_coordinate = self.position[1]

        pygame.draw.rect(window, self.colour, (x_coordinate*distance+1, y_coordinate*distance+1, distance-2, distance-2))

        if eyes:
            center = distance // 2
            radius = 3
            right_eye = (x_coordinate*distance+center + radius, y_coordinate*distance + 8)
            left_eye = (x_coordinate*distance+center - radius * 2, y_coordinate*distance + 8)
            pygame.draw.circle(window, (0,0,0), right_eye, radius)
            pygame.draw.circle(window, (0,0,0), left_eye, radius)

class snake_object(object):
    body = []
    turn = {}

    def __init__(self, colour, position):
        self.colour = colour
        self.head = cube_object(position)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for each_key in keys:
                if keys[pygame.K_LEFT]:
                    self.direction_x = -1
                    self.direction_y = 0
                    self.turn[self.head.position[:]] = [self.direction_x, self.direction_y]

                elif keys[pygame.K_RIGHT]:
                    self.direction_x = 1
                    self.direction_y = 0
                    self.turn[self.head.position[:]] = [self.direction_x, self.direction_y]

                elif keys[pygame.K_UP]:
                    self.direction_x = 0
                    self.direction_y = -1
                    self.turn[self.head.position[:]] = [self.direction_x, self.direction_y]

                elif keys[pygame.K_DOWN]:
                    self.direction_x = 0
                    self.direction_y = 1
                    self.turn[self.head.position[:]] = [self.direction_x, self.direction_y]

        for index, cube in enumerate(self.body):
            cube_position = cube.position[:]

            if cube_position in self.turn:
                turn_at = self.turn[cube_position]
                cube.move(turn_at[0], turn_at[1])

                if index == len(self.body)-1:
                    self.turn.pop(cube_position)

            else:
                if cube.direction_x == -1 and cube.position[0] <= 0:
                    cube.position = (cube.rows-1, cube.position[1])

                elif cube.direction_x == 1 and cube.position[0] >= cube.rows-1:
                    cube.position = (0, cube.position[1])

                elif cube.direction_y == 1 and cube.position[1] >= cube.rows-1:
                    cube.position = (cube.position[0], 0)
                
                elif cube.direction_y == -1 and cube.position[1] <= 0:
                    cube.position = (cube.position[0], cube.rows-1)

                else:
                    cube.move(cube.direction_x, cube.direction_y)

    def reset(self, position):
        self.head = cube_object(position)
        self.body = []
        self.body.append(self.head)
        self.turn = {}
        self.direction_x = 0
        self.direction_y = 1

    def add_cube(self):
        tail = self.body[-1]
        direction_x = tail.direction_x
        direction_y = tail.direction_y

        if direction_x == 1 and direction_y == 0:
            self.body.append(cube_object((tail.position[0]-1, tail.position[1])))
        
        elif direction_x == -1 and direction_y == 0:
            self.body.append(cube_object((tail.position[0]+1, tail.position[1])))

        elif direction_x == 0 and direction_y == 1:
            self.body.append(cube_object((tail.position[0], tail.position[1]-1)))
        
        elif direction_x == 0 and direction_y == -1:
            self.body.append(cube_object((tail.position[0], tail.position[1]+1)))

        self.body[-1].direction_x = direction_x
        self.body[-1].direction_y = direction_y

    def draw(self, window):
        for index, cube in enumerate(self.body):
            
            if index == 0:
                cube.draw(window, True)

            else:
                cube.draw(window)

def draw_grid(window):
    size_between = width // rows
    x_coordinate = 0
    y_coordinate = 0

    for _ in range (rows):
        x_coordinate = x_coordinate + size_between
        y_coordinate = y_coordinate + size_between

        pygame.draw.line(window, (255,255,255), (x_coordinate,0), (x_coordinate,width))
        pygame.draw.line(window, (255,255,255), (0,y_coordinate), (width,y_coordinate))

def redraw_window(window, snake, snack):
    window.fill((0,0,0))
    snake.draw(window)
    snack.draw(window)
    draw_grid(window)
    pygame.display.update()


def random_snack(snake):
    positions = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        if len(list(filter(lambda current:current.position == (x,y), positions))) > 0:
            continue

        else:
            break

    return (x,y)

def message_box(subject, content):
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)

    try:
        root.destroy()
    except:
        pass

def main():
    window = pygame.display.set_mode((width, width))
    snake = snake_object((255,0,0),(10,10))
    snack = cube_object(random_snack(snake), colour=(0,255,0))
    flag = True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        
        if snake.body[0].position == snack.position:
            snake.add_cube()
            snack = cube_object(random_snack(snake), colour=(0,255,0))

        for index in range(len(snake.body)):
            if snake.body[index].position in list(map(lambda current: current.position, snake.body[index+1:])):
                print(f"Score: {len(snake.body)}")
                message_box("Game Over", "Try again.")
                snake.reset((10,10))
                break

        redraw_window(window, snake, snack)
    
if __name__ == "__main__":
    main()