"""Todo:
- implement angle_offset
"""

import turtle
import numpy as np

# initial definitions: 

## screen:

screen = turtle.Screen()
screen.title('Shapes')
screen_width = 800
screen.bgcolor("#100026")
screen.setup(width=screen_width, height=screen_width)

## turtle:

pen = turtle.Turtle()
pen.hideturtle()
pen.radians()
pen.pensize(2)
pen.pencolor("#A0A0A0")

## misc. variables:

default_circle_precision= 0.1

draw_is_instant = True
if draw_is_instant == True:
    screen.tracer(0)
else:
    pen.speed(0)

## functions:

def draw_polygon(radius, sides, density=1, centre=np.array([0,0]), angle_offset=0):
    """Draws the largest regular polygon with a given number of sides that fits within a circle with a given radius. 
    \n Parameters:
    - density - the number of edges "skipped" + 1 (e.g. a pentagon's is 1, but a pentagram's is 2) (see Wikipedia for a more in-depth explanation: https://en.wikipedia.org/wiki/Density_(polytope)#Polygons)
    - angle_offset - the amount the polygon is rotated anticlockwise about its centre (in radians)
    """
    # handling parameters:
    if radius <= 0:
        raise ValueError("radius must be > 0")
    if sides < (2 * density) + 1:
        raise ValueError("sides must be > (2 * density) + 1")
    if density < 1:
        raise ValueError("density must be > 1")
    
    # drawing:
    pen.up()
    pen.goto(centre[0] + radius, centre[1])
    pen.down()
    i = 0
    while i < sides:
        # moving to home vertex
        pen.up()
        pen_x = radius * np.cos((2 * i * np.pi) / sides)
        pen_y = radius * np.sin((2 * i * np.pi) / sides)
        pen.goto(pen_x, pen_y) # home vertex

        # connecting to the vertex forward by an number of vertexs equal to density
        i += density
        pen_x = radius * np.cos((2 * i * np.pi) / sides)
        pen_y = radius * np.sin((2 * i * np.pi) / sides)
        pen.down()
        pen.goto(pen_x, pen_y) # destination vertex
        
        i -= density - 1 # set index of new home vertex (1 after the previous home vertex)
    
def draw_circle(radius, centre=np.array([0,0]), precision=0.1):
    """Draws a circle with a given radius. 
    \n Parameters:
    - precision - the angular step between vertexes; a smaller value gives a smoother circle
    """
    # handling parameter:
    if precision <= 0:
        raise ValueError("precision must be > 0")
    
    # drawing:
    sides = round((2 * np.pi) / precision)
    draw_polygon(radius, sides, centre=centre)

def draw_circscribed_polygon(radius, sides, density=1, centre=np.array([0,0]), angle_offset=0, precision=default_circle_precision):
    """Draws a circle with a given radius and the largest regular polygon with a given number of sides that fits within it. 
    \n Parameters:
    - density - the number of edges "skipped" + 1 (e.g. a pentagon's is 1, but a pentagram's is 2) (see Wikipedia for a more in-depth explanation: https://en.wikipedia.org/wiki/Density_(polytope)#Polygons)
    - angle_offset - the amount the polygon is rotated anticlockwise about its centre (in radians)
    - precision - the angular step between vertexes; a smaller value gives a smoother circle
    """
    draw_circle(radius, centre, precision)
    draw_polygon(radius, sides, density, centre, angle_offset)

def draw_nested_circscribed_polygons(radius, sides, density=1, centre=np.array([0,0]), angle_offset=0, precision=default_circle_precision, ending_sides=3):
    """Draws a circle with a given radius and the largest regular polygon with a given number of sides that fits within it. 
    \n Parameters:
    - density - the number of edges "skipped" + 1 (e.g. a pentagon's is 1, but a pentagram's is 2) (see Wikipedia for a more in-depth explanation: https://en.wikipedia.org/wiki/Density_(polytope)#Polygons)
    - angle_offset - the amount the polygon is rotated anticlockwise about its centre (in radians)
    - precision - the angular step between vertexes; a smaller value gives a smoother circle
    - ending_sides - the number of sides the polygon with the least number of sides has
    """
    radius_ratio = 1
    ending_sides = (2 * density) + 1
    for side_num in range(sides, ending_sides - 1, -1):
        draw_circscribed_polygon(radius * radius_ratio, side_num, density, centre, angle_offset, precision)
        radius_ratio *= np.cos((np.pi * density) / side_num)

# drawing: 

## shape variables:

radius = (screen_width // 2) - 10
density = 2
sides = 9

## calling functions:

draw_nested_circscribed_polygons(radius, sides, density)

screen.update() # renders the drawings

turtle.done() # keeps screen open after drawing is complete