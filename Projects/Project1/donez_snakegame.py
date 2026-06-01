"""
    Description of program: A snake game in which the player moves around the
    board, eats apples, and grows longer while avoiding walls and itself
    Filename: donez_snakegame.py
    Author: James Donez
    Date: 4/12/26
    Course: COMP 1353
    Assignment: Project 1
    Collaborators: None
    Internet Source: None
"""

# import sys
# from pathlib import Path

# sys.path.append(str(Path(__file__).resolve().parents[2]))

from data_structures.DoublyLinkedList import DoublyLinkedList

#IMPORTS
import dudraw
import random

#Globals
grid = []
snake = DoublyLinkedList()
facing = "left"
alive = True
apple = ()
time = 100

def setup():
    """
    Sets up the drawing canvas, creates the grid, and places the first apple.
    """
    global apple
    dudraw.set_canvas_size(800,800)
    dudraw.clear(dudraw.BLACK)
    dudraw.set_y_scale(0, 20)
    dudraw.set_x_scale(0, 20)
    grid_creation()
    apple = (random.randint(0,19), random.randint(0,19))
    grid[apple[0]][apple[1]] = {"type": "apple"}


def grid_creation():
    """
    Creates the 20 by 20 game grid and fills each square as empty space.
    """
    for i in range(20):
        column = []
        for j in range(20):
            dudraw.set_pen_color_rgb(207,249,158)
            dudraw.filled_square(i+.5, j+.5, .48)
            column.append({"type": "air"})
        grid.append(column)

def create_snake():
    """
    Creates the starting snake at the center of the board and draws it.
    """
    snake.add_first((10,10))
    grid[10][10] = {"type": "head"} 
    draw()

def draw():
    """
    Draws the snake and the apple on the game board.
    """
    item = snake.header.next.data #type: ignore
    x, y = item[0], item[1]
    draw_head(x, y)
    if snake.size >= 2:
        node = snake.header.next.next #type: ignore
        for i in range(snake.size - 1):
            item = node.data #type: ignore
            x, y = item[0] + 0.5, item[1] +0.5
            dudraw.set_pen_color_rgb(62, 145, 65)
            dudraw.filled_square(x, y, .48)

            node = node.next
    apple_x, apple_y = apple #type: ignore

    dudraw.set_pen_color_rgb(199, 55, 47)
    dudraw.filled_square(apple_x+.5, apple_y+.5, .48)

def orientarion(part: str):
    """
    Returns drawing offsets for the snake head based on the direction faced.

    Parameters:
        part (str): The facial feature to position such as eyes, mouth, or triangle

    Returns:
        tuple: Coordinate offsets used to draw that head feature
    """
    global facing
    if part == "eyes":
        if facing == "right":
            return 0.2, 0.2, 0.2, -0.2
        elif facing == "left":
            return -0.2, 0.2, -0.2, -0.2
        elif facing == "down":
            return -0.25, -0.2, 0.2, -0.2
        elif facing == "up":
            return -0.25, 0.2, 0.2, 0.2
    elif part == "mouth":
        if facing == "up":
            return -0.02, 0.7, 0.1, 0.3
        elif facing == "down":
            return -0.02, -0.7, 0.1, 0.3
        elif facing == "right":
            return 0.7, -0.02, 0.3, 0.1
        elif facing == "left":
            return -0.7, -0.02, 0.3, 0.1
    elif part == "triangle":
        if facing == "up":
            return -0.39, 1.4, 0.26, 1.4, -0.01, 0.8
        elif facing == "down":
            return -0.39, -1.4, 0.26, -1.4, -0.01, -0.8
        elif facing == "right":
            return 1.4, -0.32, 1.4, 0.28, 0.8, -0.02
        elif facing == "left":
            return -1.4, -0.32, -1.4, 0.28, -0.8, -0.02


def draw_head(x: int, y:int):
    """
    Draws the snake's head with eyes and tongue at the given grid position.

    Parameters:
        x (int): The x-coordinate of the snake head
        y (int): The y-coordinate of the snake head
    """

    #Centers the vals
    center_x = x + 0.5
    center_y = y + 0.5

    # Main head shape
    dudraw.set_pen_color_rgb(62, 145, 65)
    dudraw.filled_square(center_x, center_y, .48)

    tempx1, tempy1, tempx2, tempy2 = orientarion("eyes") #type: ignore
    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.filled_circle(center_x + tempx1, center_y + tempy1, 0.1)
    dudraw.filled_circle(center_x + tempx2, center_y + tempy2, 0.1)

    dudraw.set_pen_color(dudraw.BLACK)
    dudraw.filled_circle(center_x + tempx1, center_y + tempy1, 0.04)
    dudraw.filled_circle(center_x + tempx2, center_y + tempy2, 0.04)

    temp1, temp2, temp3, temp4= orientarion("mouth") #type: ignore
    dudraw.set_pen_color_rgb(155, 28, 49)
    dudraw.filled_rectangle(center_x + temp1, center_y + temp2, temp3, temp4)
    dudraw.set_pen_color_rgb(207,249,158)
    point1_x, point1_y, point2_x, point2_y, point3_x, point3_y = orientarion("triangle") #type: ignore
    dudraw.filled_triangle(
        center_x + point1_x, center_y + point1_y,
        center_x + point2_x, center_y + point2_y,
        center_x + point3_x, center_y + point3_y
    )

def tounge_fix(direction: str):
    """
    Clears or redraws the square in front of the snake head when turning.

    Parameters:
        direction (str): The direction the snake is currently facing
    """
    x_loc, y_loc = snake.header.next.data #type: ignore
    new_x, new_y = change(facing, x_loc, y_loc) #type: ignore
    if new_x < 0 or new_x > 19 or new_y < 0 or new_y > 19:
        dudraw.set_pen_color_rgb(207,249,158)
        return
    if grid[new_x][new_y] == {"type": "snake"}:
        dudraw.set_pen_color_rgb(62, 145, 65)
        dudraw.filled_square(new_x + 0.5, new_y + 0.5, .48)
    else:
        dudraw.set_pen_color_rgb(207,249,158)
        dudraw.filled_square(new_x +.5, new_y +.5, .48)


def change(move: str, x_loc: int, y_loc: int):
    """
    Calculates the next coordinate based on the current facing direction.

    Parameters:
        move (str): The direction of movement
        x_loc (int): Current x-coordinate
        y_loc (int): Current y-coordinate

    Returns:
        tuple: The next x and y coordinate
    """
    if facing == "up":
        return x_loc, y_loc + 1
    elif facing == "down":
        return x_loc, y_loc - 1
    elif facing == "left":
        return x_loc - 1, y_loc
    elif facing == "right":
        return x_loc + 1, y_loc 

def check_next(x_loc: int, y_loc: int):
    """
    Checks whether the next move causes the snake to hit a wall or itself.

    Parameters:
        x_loc (int): The next x-coordinate to check
        y_loc (int): The next y-coordinate to check
    """
    global alive
    if x_loc < 0 or x_loc > 19 or y_loc < 0 or y_loc > 19:
        alive = False
        return
    if grid[x_loc][y_loc] == {"type": "snake"}:
        alive = False
def move():
    """
    Moves the snake one space forward and handles growth when an apple is eaten.
    """
    global alive
    if alive:
        node = snake.header.next
        last = node
        current_x, current_y = node.data #type: ignore
        while last.next is not snake.tailer: #type: ignore
            last = last.next    #type: ignore
        last_x, last_y = last.data #type: ignore

        new_x, new_y = change(facing, current_x, current_y) #type: ignore
        check_next(new_x,new_y)
        if not alive:
            return
        add_tail = apple_check(new_x,new_y)

        for i in range(snake.size):
            old_x, old_y = node.data #type: ignore
            grid[new_x][new_y] = {"type": "snake"}
            if add_tail and i == snake.size - 1:
                snake.add_last((last_x,last_y))
                grid[last_x][last_y] = {"type": "snake"}
                add_tail = False
            else:
                grid[old_x][old_y] = {"type": "air"}
                dudraw.set_pen_color_rgb(207,249,158)
                dudraw.filled_square(old_x+.5, old_y+.5, .48)

            node.data = new_x,new_y #type: ignore

            node = node.next #type: ignore
            new_x, new_y = old_x, old_y

def apple_check(xloc: int, yloc: int):
    """
    Checks whether the snake has eaten the apple and places a new one if needed.

    Parameters:
        xloc (int): The x-coordinate of the snake's new head position
        yloc (int): The y-coordinate of the snake's new head position

    Returns:
        bool: True if the snake ate the apple, otherwise None
    """
    global apple
    x, y = apple #type: ignore
    if x == xloc and y == yloc:
        grid[x][y] = {"type": "air"}
        apple = (random.randint(0,19), random.randint(0,19))
        x, y = apple
        while grid[x][y] == {"type": "snake"}:
            apple = (random.randint(0,19), random.randint(0,19))
            x, y = apple
        grid[apple[0]][apple[1]] = {"type": "apple"}
        return True
       
def direction(key:str):
    """
    Updates the snake's facing direction based on the key the user pressed.

    Parameters:
        key (str): The keyboard input used to change direction
    """
    global facing

    if key.lower() == "w":
        tounge_fix(facing)
        facing = "up"
    elif key.lower() == "a":
        tounge_fix(facing)
        facing = "left"
    elif key.lower() == "s":
        tounge_fix(facing)
        facing = "down"
    elif key.lower() == "d":
        tounge_fix(facing)
        facing = "right"

def time_update():
    """
    Updates the delay time based on the current snake size.
    """
    time = (snake.size * 20) + 50


def main():
    """
    Runs the main game loop for the snake game.
    """
    global facing

    running = True
    setup()
    create_snake()

    while running:

        

        if dudraw.has_next_key_typed():
            key = dudraw.next_key()
            if key.lower() == "q":
                running = False
            else:
                direction(key)

        if alive:
            move()
            draw()
            time_update()

        dudraw.show(time)

if __name__ == "__main__":
    main()
