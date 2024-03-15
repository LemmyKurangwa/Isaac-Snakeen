from tkinter import *
import random

# Constants for settings of the game, player should not change these. It sets the Width, height of the winodw. Speed of the snake and more!
GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 75
SPACE_SIZE = 50
BODY_PARTS = 6
SNAKE_COLOR = "aqua"
FOOD_COLOR = "lime"
BACKGROUND_COLOR = "magenta"

 
class Snake:
    
    def __init__(self):
        # Setting a body size
        self.body_size = BODY_PARTS
        # List of Coordinates
        self.coordinates = []
        # List of Square Graphics
        self.squares = [] 

        for i in range(0, BODY_PARTS):
            # Coordinates for each body part at the start of the game will be at 0,0 so that snake will appear in top left corner
            self.coordinates.append([0,0])
        # Creating Squares
        # We have lists of lists so thats why we're using x, y
        # In self coordinates, we'll create a square
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            # We have a list of squares, and we can append each square into our list
            self.squares.append(square)   


class Food:
    # Creating init method will construct food object
    def __init__(self):
        # Placing food object randomly, divide 700 by our space size, to give us 14 possible spots on x and y axis, we need to pick one of these spots randomly
        # If we divide game width by our space size, then we'll get a random number between 0 and 14
        # Converting these to pixels
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE)-1) * SPACE_SIZE
         
        # Setting coordinates 
        # A list of x and y 
        self.coordinates = [x, y]

        # Drawing food object on the canvas
        # Picking a starting corner, that will be where x and y are, and an ending coordinate
        # X and Y plus our space size, the size of an object in our game
        # We can also set a fill color, which will be our food color that we declare
        # Adding a tag will make it easy to delete this object
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    # We are unpacking the head of our snake
    # At an index of 0, that's the head of the snake
    # Coordinates will be stored in x and y
    x, y = snake.coordinates[0]

    if direction == "up":
        # If direction is up, then
        # Space size so that we move one space up 
        y -= SPACE_SIZE

    elif direction == "down":
        y += SPACE_SIZE

    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE

    # Let's update the coordinates for the head of the snake, and write that before we move on to the next turn
    # We will insert a new set of coordinates, after updating one of them
    # 0 will be the index/the head of the snake. We will inset x and y coordinates at this new location
    snake.coordinates.insert(0, (x, y))

    #Creating a new graphic for the head of the snake
    #X and Y for the starting corner of our rectangle
    #Ending corner will be x plus SPACE_SIZE etc.
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    #Update snakes list of squares
    # Insert at index, 0 and a new square that we create
    snake.squares.insert(0, square)

    # Eating the apple
    # We unpacked the coordinates for the head of the snake
    # X = Head of the snake
    # That's the x coordinate for our food object
    # This means that the x and y are overlaping 
    if x  == food.coordinates[0] and y == food.coordinates[1]:

        global score
        
        # We're incrementing our score by one
        score += 1

        # Chnaging our label
        # We're going to use the format method and pass in our new score
        label.config(text="Score:{}".format(score))

        # Deleting food object when eaten
        # Using the tag to make deleting the food object quite easier
        canvas.delete("food")

        # Create a new food object after one is eaten
        food = Food()

# We will only delete the last body part of our snake if we did not eat a food object
    else:   
    # Our snake is going to move, but we need to delete the last body part in our snake, within the next turn function
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    # This will check collisons and this will return true or false if we detect a and pass in our snake object
    if check_collisons(snake):
        # If there is a collision, we will call the game over function
        game_over()

    # Else, we will update to the next turn
    else:

        # We need to call the next turn function again, for the next turn
        # Let's say our game speed, we're going to call the next turn function, and we need to pass in our arguments of snake and food
        window.after(SPEED, next_turn, snake, food )   

def change_direction(new_direction):
    
    #Accesing our direction
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down': 
        if direction != 'up':
            direction = new_direction

def check_collisons(snake):
    
    # Let's unpack the head of the next
    x, y = snake .coordinates[0] 

    # Check to see if we cross the left or right border
    if x < 0 or x >= GAME_WIDTH:
       
       # For testing purposes, we're going to print something in the console window
        print("GAME OVER")
        return True
    
    elif y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER")
        return True
    
    # If our snake touches it's tail, or another body part
    # Set inside of the parenthesis to after the head
    for body_part in snake.coordinates[1:]:
        # Checking to see if any of the coordinates are matching
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
        
    #Otherwise
    return False
    


def game_over():
    
    # Deleting everything after a game over
    canvas.delete(ALL)
    # Creating GAME OVER text, and putting it in the middle of the screen
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="white", tag="gameover")

# Using Tkinter to setup the window for the game, and the score widget.
window = Tk()
window.title("Issac Snakeen")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('Helvetica', 40))
label.pack()


canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Using this so that it renders
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# cannot be floats, must be whole integers, so we add a cast, round x and y
# Were doing this, to try and get the window to start in the center of the computer screen
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

# we are setting the geometry, using f string
window.geometry(f"{window_width}x{window_height}+{x}+{y}")


# Adding some controls to the snake
window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))

window.bind('<A>', lambda event: change_direction('left'))
window.bind('<D>', lambda event: change_direction('right'))
window.bind('<W>', lambda event: change_direction('up'))
window.bind('<S>', lambda event: change_direction('down'))

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))



# Creating Snake and Food Object, Fill in Snake and Food class 
snake = Snake()
food = Food()

# After we create Snake and Food object, we should call the next turn function and pass in our snake and food object
next_turn(snake, food)

window.mainloop()