import turtle
#turn show turtle off
wn = turtle.Screen()
wn.title("Naughts and Crosses")
wn.bgcolor("white")

def draw_grid():
    t = turtle.Turtle() #draw walls
    t.penup()
    l = 600
    t.forward(l/6) 
    t.left(90)
    t.forward(l/2)
    t.left(180)
    t.pendown()
    t.forward(l) #line 1
    t.penup()
    t.right(90) 
    t.forward(l/3) 
    t.right(90)
    t.pendown()
    t.forward(l) #line 2
    t.penup()
    t.left(90)
    t.forward(l/3)
    t.left(90)
    t.forward(l/3)
    t.left(90)
    t.pendown()
    t.forward(l) #line 3
    t.penup()
    t.right(90)
    t.forward(l/3)
    t.right(90)
    t.pendown()
    t.forward(l)

def play_move(number, shape):
    l = 600
    t = turtle.Turtle()
    t.penup()
    if number == 2:
        t.left(135)
    if number == 3:
        t.right(90)
    if number == 4:
        t.right(135)
    if number == 6:
        t.left(45)
    if number == 7:
        t.left(90)
    if number == 8:
        t.right(45)
    if number == 9:
        t.left(180)
    if number in [9, 3, 1, 7]:
        t.forward(l/3)
    if number in [2, 6, 4, 8]:
        t.forward(((2/9)**0.5)*l)
    if shape == 'Naught':
        t.setheading(0)
        t.forward(90)
        t.left(90)
        t.pendown()
        t.circle(90)
    if shape == 'Cross':
        t.setheading(0)
        t.left(45)
        t.forward(0.2*l)
        t.left(180)
        t.pendown()
        t.forward(0.4*l)
        t.penup()
        t.left(135)
        t.forward(2*(0.02**0.5)*l)
        t.left(135)
        t.pendown()
        t.forward(0.4*l)

def new_game():
    turtle.clearscreen()

