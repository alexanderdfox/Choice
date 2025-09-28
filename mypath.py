import turtle
from svg.path import parse_path
from xml.dom import minidom
import numpy as np
import math

# Load SVG
svg_file = "trace.svg"  # replace with your SVG file path
doc = minidom.parse(svg_file)
path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
doc.unlink()

# Sample points along path
def sample_path(path_data, samples=100):
	path = parse_path(path_data)
	points = []
	for segment in path:
		for i in range(samples):
			p = segment.point(i / samples)
			points.append((p.real, p.imag))
	return points

# Collect all points
all_points = []
for d in path_strings:
	all_points.extend(sample_path(d, samples=50))

all_points = np.array(all_points)

# Center points
center_x = (all_points[:,0].max() + all_points[:,0].min()) / 2
center_y = (all_points[:,1].max() + all_points[:,1].min()) / 2
all_points[:,0] -= center_x
all_points[:,1] -= center_y
all_points[:,1] = -all_points[:,1]  # invert y for turtle

# Setup turtle
screen = turtle.Screen()
screen.setup(width=800, height=800)
screen.tracer(0)
t = turtle.Turtle()
t.shape("turtle")
t.color("orange")
t.penup()
t.goto(all_points[0])
t.pendown()
t.speed(0)  # maximum speed

# Function to turn the turtle toward the next point
def turn_to(turtle, x, y):
	dx = x - turtle.xcor()
	dy = y - turtle.ycor()
	angle = math.degrees(math.atan2(dy, dx))
	diff = (angle - turtle.heading()) % 360
	if diff > 180:
		turtle.left(360 - diff)
	else:
		turtle.right(diff)

# Infinite loop along path
while True:
	for x, y in all_points[1:]:
		turn_to(t, x, y)
		t.goto(x, y)
