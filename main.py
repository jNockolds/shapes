import turtle
import numpy as np
import time

"""Todo:
- change how ending_sides is set to ensure it works with density
"""

# default values:

time_decimal_places = 6

d_screen_name = "Shape drawer"
d_screen_width = 800
d_bg_colour = "#100026"

d_pen_colour = "#A0A0A0"
d_pen_size = 2
d_pen_speed = -1 # increasing above 10 has no additional effect

d_density = 1
d_shape_centre = np.array([0,0])
d_shape_angle_offset = np.pi/2
d_precision = 0.1

# decorator definitions:

def measure_time(function):
    """A decorator which measures the time it takes for a function to execute, printing the result. 
    \n It also sums the total execution time of all functions.
    """
    def wrapper(*args, **kwargs): # *args and **kwargs allow the function to take in parameters
        # timing the function:
        start = time.time()
        function(*args, **kwargs)
        end = time.time()

        # gettting results:
        elapsed_time = end - start
        function_name = function.__qualname__ # __qualname__ gives class_name.function_name

        print(f'{function_name} execution time: {round(elapsed_time, time_decimal_places)} seconds') # __name__ needed to give just the name, rather than the object type, name, and ram location
    return wrapper

# class definitions:

class Drawer:
    """Encapsulates the screen and turtle into one class."""
    def __init__(self, screen_width=d_screen_width, bg_colour=d_bg_colour, pen_colour=d_pen_colour, pen_size=d_pen_size, pen_speed=d_pen_speed, screen_name=d_screen_name):
        # screen setup:
        self.screen_width = screen_width
        self.screen = turtle.Screen()
        self.screen.title(screen_name)
        self.screen.bgcolor(bg_colour)
        self.screen.setup(width=screen_width, height=screen_width)
        
        # turtle setup:
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.radians()
        self.pen.pensize(pen_size)
        self.pen.pencolor(pen_colour)

        # pen speed:
        if pen_speed == -1:
            self.screen.tracer(0)
        else:
            self.pen.speed(pen_speed)
    
    def update(self):
        self.screen.update()

    def done(self):
        turtle.done()

class Shape:
    """Superclass for specific shape subclasses."""
    def __init__(self, radius, centre=d_shape_centre):
        # checking attributes:
        if radius <= 0:
            raise ValueError("radius must be > 0.")
        
        # assigning attributes:
        self.radius = radius
        self.centre = centre
    
    @measure_time
    def draw(self, pen):
        raise NotImplementedError("Subclasses must implement this method.")
    
class RegularPolygon(Shape):
    """A regular polygon with its size defined by the smallest radius of circle it can fit within.
    \n Attributes:
    - density - the number of edges "skipped" + 1 (e.g. a pentagon's is 1, but a pentagram's is 2); density <= (sides - 1) / 2 (see Wikipedia for a more in-depth explanation: https://en.wikipedia.org/wiki/Density_(polytope)#Polygons)
    - angle_offset - the amount the polygon is rotated anticlockwise about its centre (in radians)
    """
    def __init__(self, radius, sides : int, density=d_density, centre=d_shape_centre, angle_offset=d_shape_angle_offset):
        # checking attributes:
        if sides < (2 * density) + 1:
            raise ValueError("sides must be >= (2 * density) + 1.")
        if density < 1:
            raise ValueError("density must be >= 1.")
    
        # assigning attributes:
        super().__init__(radius, centre)
        self.sides = sides
        self.density = density
        self.angle_offset = angle_offset
    
    @measure_time
    def draw(self, pen):
        # moving to first vertex:
        pen.up()
        pen.goto(self.centre[0] + self.radius, self.centre[1])
        pen.down()

        # drawing lines between vertices:
        i = 0
        while i < self.sides:
            # moving to home vertex:
            pen.up()
            home_angle = ((2 * i * np.pi) / self.sides) + self.angle_offset
            home_x = self.radius * np.cos(home_angle)
            home_y = self.radius * np.sin(home_angle)
            pen.goto(home_x, home_y) # home vertex

            # moving to destination vertex, skipping a number of vertexes equal to density - 1:
            i += self.density
            destination_angle = ((2 * i * np.pi) / self.sides) + self.angle_offset
            destination_x = self.radius * np.cos(destination_angle)
            destination_y = self.radius * np.sin(destination_angle)
            pen.down()
            pen.goto(destination_x, destination_y) # destination vertex
            
            # set i to new home vertex (1 after the previous home vertex):
            i -= self.density - 1

class Circle(Shape):
    """A circle approximated by a regular polygon.
    \n Attributes:
    - precision - the angular step between vertexes; a smaller value gives a smoother circle
    """
    def __init__(self, radius, centre=d_shape_centre, precision=d_precision):
        # checking attributes:
        if precision <= 0:
            raise ValueError("precision must be > 0.")
    
        # assigning attributes:
        super().__init__(radius, centre)
        self.precision = precision

    @measure_time
    def draw(self, pen):
        sides = round((2 * np.pi) / self.precision) # number of sides for the circle approximation
        poly = RegularPolygon(self.radius, sides, centre=self.centre, angle_offset=0)
        poly.draw(pen)

class CircumscribedRegularPolygon(RegularPolygon, Circle):
    """Draws a circle with a given radius and the largest regular polygon with a given number of sides that fits within it.
    \n Attributes:
    - density - the number of edges "skipped" + 1 (e.g. a pentagon's is 1, but a pentagram's is 2); density <= (sides - 1) / 2 (see Wikipedia for a more in-depth explanation: https://en.wikipedia.org/wiki/Density_(polytope)#Polygons)
    - angle_offset - the amount the polygon is rotated anticlockwise about its centre (in radians)
    - precision - the angular step between vertexes; a smaller value gives a smoother circle
    """
    def __init__(self, radius, sides, density=d_density, centre=d_shape_centre, angle_offset=d_shape_angle_offset, precision=d_precision):
        RegularPolygon.__init__(self, radius, sides, density, centre, angle_offset)
        Circle.__init__(self, radius, centre, precision)

    @measure_time
    def draw(self, pen):
        circle = Circle(self.radius, self.centre, self.precision)
        regular_polygon = RegularPolygon(self.radius, self.sides, self.density, self.centre, self.angle_offset)

        circle.draw(pen)
        regular_polygon.draw(pen)

class NestedCircumscribedRegularPolygons(Shape):
    """Nests circumscribed polygons in each other, decreasing in number of sides until it reaches a minimum.
    \n Attributes:
    - layers - the number of polygons in the nested shape (note that circles aren't polygons)
    - circumscribedRegularPolygons - the list containing all of the polygons
    """
    # constructors:
    
    ## one specific CircumscribedRegularPolygon:
    def __init__(self, circumscribedRegularPolygon, layers=2):
        self.layers = layers
        self.circumscribedRegularPolygons = []
        for i in range(layers):
            self.circumscribedRegularPolygons.append(circumscribedRegularPolygon)

    ## one specific RegularPolygon:
    def __init__(self, regularPolygon, layers=2, precision=d_precision):
        # making the polygon circumscribed:
        radius = regularPolygon.radius
        sides = regularPolygon.sides
        density = regularPolygon.density
        centre = regularPolygon.centre
        angle_offset = regularPolygon.angle_offset
        circumscribedRegularPolygon = CircumscribedRegularPolygon(radius, sides, density, centre, angle_offset, precision)

        # assigning attributes: 
        self.layers = layers
        self.circumscribedRegularPolygons = []
        for i in range(layers):
            self.circumscribedRegularPolygons.append(circumscribedRegularPolygon)
        
    ## a list of CircumscribedRegularPolygons:
    def __init__(self, circumscribedRegularPolygons : list):
        self.layers = len(circumscribedRegularPolygons)
        self.circumscribedRegularPolygons = circumscribedRegularPolygons
    
    ## a list of RegularPolygons:
    def __init__(self, regularPolygons : list, precision=d_precision):
        self.layers = len(regularPolygons)
        self.circumscribedRegularPolygons = []
        for i in range(self.layers):
            # making the polygon circumscribed:
            radius = regularPolygons[i].radius
            sides = regularPolygons[i].sides
            density = regularPolygons[i].density
            centre = regularPolygons[i].centre
            angle_offset = regularPolygons[i].angle_offset
            self.circumscribedRegularPolygons.append(CircumscribedRegularPolygon(radius, sides, density, centre, angle_offset, precision))

    @measure_time
    def draw(self, pen):
        radius_ratio = 1
        for i in range(self.layers):
            # decreasing radius to fit within previous circle (unless radius_ratio == 1):
            self.circumscribedRegularPolygons[i].radius *= radius_ratio

            self.circumscribedRegularPolygons[i].draw(pen)

            # updating raidus ratio for the next iteration:
            radius_ratio *= np.cos((np.pi * self.circumscribedRegularPolygons[i].density) / self.circumscribedRegularPolygons[i].sides)

# variables:

drawer = Drawer()

radius = (drawer.screen_width // 2) - 10
sides = 5

# initiating elapsed time period:
start_time = time.time()

# constructing shapes:

circumscribed_regular_polygon1 = RegularPolygon(radius, 3)
circumscribed_regular_polygon2 = RegularPolygon(radius, 4)
circumscribed_regular_polygon3 = RegularPolygon(radius, 100)


circumscribed_regular_polygons = [circumscribed_regular_polygon1, circumscribed_regular_polygon2, circumscribed_regular_polygon3]

nested_circumscribed_regular_polygons = NestedCircumscribedRegularPolygons(circumscribed_regular_polygons)






## calling draw functions:
nested_circumscribed_regular_polygons.draw(drawer.pen)

# rendering the drawings:
drawer.update()

# calculating and printing total elapsed time: 
end_time = time.time()
total_elapsed_time = end_time - start_time
print(f'\nTotal execution time: {round(total_elapsed_time, time_decimal_places)} seconds')

drawer.done() # keeps screen open after drawing is complete