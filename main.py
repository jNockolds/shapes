import turtle
import numpy as np

# screen:
screen = turtle.Screen()
screen.title('Shapes')
screen_width = 800
screen.bgcolor("lightgrey")
screen.setup(width=screen_width, height=screen_width)
# screen.tracer(0)

# turtle:
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.radians()
pen.pensize(3)

# functions:

def draw_regular_polygon(sides, side_length, start_pos = np.array([0,0]), angle_offset = 0):
    """
    Draws a regular polygon. Parameters:
    - angle_offset: the angle of rotation (anticlockwise) from the default
    """
    internal_angle = (np.pi * (sides - 2)) / sides
    pen.up()
    pen.goto(start_pos[0], start_pos[1])
    pen.down()
    pen.left(np.pi - (internal_angle / 2) + angle_offset)
    for i in range(sides):
        pen.forward(side_length)
        pen.left(np.pi - internal_angle)

def draw_polygon(sides, radius, centre=np.array([0,0]), angle_offset=0):
    if radius <= 0:
        raise ValueError("radius must be > 0")
    pen.up()
    pen.goto(centre[0] + radius, centre[1])
    pen.down()
    for i in range(1, sides + 1):
        pen.goto(radius * np.cos((2 * i * np.pi) / sides), radius * np.sin((2 * i * np.pi) / sides))

def draw_circle(radius, centre=np.array([0,0]), precision=0.3):
    """Draws a circle. Parameters:
    - precision: the larger it is, the more precise the circle is but the longer it takes to draw
    """
    if precision <= 0:
        raise ValueError("precision must be > 0")
    draw_polygon(round(radius * precision), radius, centre)

def draw_circscribed_polygon(sides, radius, centre=np.array([0,0]), angle_offset=0, precision=0.3):
    draw_circle(radius, centre, precision)
    draw_polygon(sides, radius, centre, angle_offset)


# drawing:
rad = screen_width // 4
draw_circscribed_polygon(5, rad)












screen.exitonclick() # keeps screen open until clicked