import turtle
import numpy as np

# screen:
screen = turtle.Screen()
screen.title('Shapes')
screen_width = 800
screen.bgcolor("#100026")
screen.setup(width=screen_width, height=screen_width)
# screen.tracer(0)

# turtle:
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.radians()
pen.pensize(3)
pen.pencolor("#A0A0A0")

# functions:

def draw_polygon(radius, sides, density=1, centre=np.array([0,0]), angle_offset=0):
    if radius <= 0:
        raise ValueError("radius must be > 0")
    if sides < (2 * density) + 1:
        raise ValueError("sides must be > (2 * density) + 1")
    pen.up()
    pen.goto(centre[0] + radius, centre[1])
    pen.down()
    for i in range(1, sides + 1):
        pen.goto(radius * np.cos((2 * i * density * np.pi) / sides), radius * np.sin((2 * i * density * np.pi) / sides))

def draw_circle(radius, centre=np.array([0,0]), precision=0.3):
    """Draws a circle. Parameters:
    - precision: the larger it is, the more precise the circle is but the longer it takes to draw
    """
    if precision <= 0:
        raise ValueError("precision must be > 0")
    draw_polygon(radius, round(radius * precision), centre=centre)

def draw_circscribed_polygon(radius, sides, density=1, centre=np.array([0,0]), angle_offset=0, precision=0.3):
    draw_circle(radius, centre, precision)
    draw_polygon(radius, sides, density, centre, angle_offset)




# drawing:
rad = screen_width // 4
draw_circscribed_polygon(rad, 19, 7)












screen.exitonclick() # keeps screen open until clicked