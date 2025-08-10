import tkinter as tk
import random
from PIL import Image, ImageTK

# Game constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
FRUIT_SIZE = 50
BASKET_WIDTH = 100
FALL_SPEED = 10
NEW_FRUIT_INTERVAL = 2000  # milliseconds

# Initialize window
root = tk.Tk()
root.title("🍓 Catch the Falling Fruits 🍍")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="#e0f7fa")
canvas.pack()

# Load images
fruit_images = [
    ImageTk.PhotoImage(Image.open("images/apple.png").resize((FRUIT_SIZE, FRUIT_SIZE))),
    ImageTk.PhotoImage(Image.open("images/banana.png").resize((FRUIT_SIZE, FRUIT_SIZE))),
    ImageTk.PhotoImage(Image.open("images/grape.png").resize((FRUIT_SIZE, FRUIT_SIZE)))
]
basket_image = ImageTk.PhotoImage(Image.open("images/basket.png").resize((BASKET_WIDTH, 70)))

# Basket setup
basket_x = WINDOW_WIDTH // 2
basket = canvas.create_image(basket_x, WINDOW_HEIGHT - 50, image=basket_image)

# Game variables
score = 0
missed = 0
fruits = []

score_text = canvas.create_text(10, 10, anchor="nw", font=("Arial", 16, "bold"), text="Score: 0 | Missed: 0", fill="black")

# Move basket
def move_left(event):
    global basket_x
    if basket_x > BASKET_WIDTH // 2:
        basket_x -= 20
        canvas.coords(basket, basket_x, WINDOW_HEIGHT - 50)

def move_right(event):
    global basket_x
    if basket_x < WINDOW_WIDTH - BASKET_WIDTH // 2:
        basket_x += 20
        canvas.coords(basket, basket_x, WINDOW_HEIGHT - 50)

root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

# Drop new fruit
def drop_fruit():
    x = random.randint(50, WINDOW_WIDTH - 50)
    fruit_type = random.choice(fruit_images)
    fruit = canvas.create_image(x, 0, image=fruit_type)
    fruits.append((fruit, fruit_type))
    root.after(NEW_FRUIT_INTERVAL, drop_fruit)

# Update game loop
def update_game():
    global score, missed
    for fruit, image in fruits[:]:
        canvas.move(fruit, 0, FALL_SPEED)
        fx, fy = canvas.coords(fruit)
        if fy >= WINDOW_HEIGHT - 80:
            if abs(fx - basket_x) < 50:
                score += 1
                canvas.delete(fruit)
                fruits.remove((fruit, image))
            else:
                missed += 1
                canvas.delete(fruit)
                fruits.remove((fruit, image))
    
    canvas.itemconfig(score_text, text=f"Score: {score} | Missed: {missed}")

    if missed >= 5:
        canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, text="Game Over!", font=("Arial", 40, "bold"), fill="red")
    else:
        root.after(50, update_game)

# Start the game
drop_fruit()
update_game()
root.mainloop()

