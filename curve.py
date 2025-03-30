import pygame
import sys
import numpy as np
from math import comb

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bezeier Curve Visualization")
clock = pygame.time.Clock()
FPS = 60


"""
Pₙ are control points to guide curve | n -> order of curve
n = 2 gives you a quadratic curve (P0 P1 P2)
"""

#starting control points (inital)
control_points = np.array([
    (100, 500),  # P0
    (300, 100),  # P1
    (500, 500),  # P2
])
n  = 2 # P -> 2

def B_t(t, control_points):
    point = np.zeros(2)
    for i, P in enumerate(control_points):
        # https://en.wikipedia.org/wiki/B%C3%A9zier_curve Quadratic Curve method
        # P is being scaled | (100,500) * .3  -> will return scaled point on the curve 
        point += comb(n, i) * ((1 - t) ** (n - i)) * (t ** i) * P
    return point


def connect_points(bezier_points):
    # Draw the Bezier curve by connecting the points
    for i in range(len(bezier_points) - 1):
        start_pos = bezier_points[i]
        end_pos = bezier_points[i + 1]
        pygame.draw.line(screen, (255, 255, 255), start_pos.astype(int), end_pos.astype(int), 2) 
    

dragging = False
dragging_point_index = None


running = True
while running:
    clock.tick(FPS)
    screen.fill((30, 30, 30))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Check if any control point is clicked in 25 pixels radius
            for i, point in enumerate(control_points):
                if (mouse_x - point[0]) ** 2 + (mouse_y - point[1]) ** 2 < 25:
                    dragging = True
                    dragging_point_index = i
                    break

        #Mouse not dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            dragging_point_index = None

        # If mouse is moving and dragging a point
        elif event.type == pygame.MOUSEMOTION:
            if dragging and dragging_point_index is not None:
                mouse_x, mouse_y = event.pos
                control_points[dragging_point_index] = (mouse_x, mouse_y)
                


    #draw control points
    for point in control_points:
        pygame.draw.circle(screen, (255, 0, 0), point, 5)  # Draw control points in red


    # Draw the Bezier curve
    bezier_points = [B_t(t,control_points) for t in np.linspace(0, 1, 100)] # 100 averaged points on the curve
    connect_points(bezier_points)





    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
