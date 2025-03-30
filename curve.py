import pygame
import sys
import numpy as np
from math import comb

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bezier Curve Visualization")
clock = pygame.time.Clock()
FPS = 60

# BezierCurve class
class BezierCurve:
    def __init__(self, control_points):
        self.control_points = control_points

    def B_t(self, t):
        point = np.zeros(2)
        n = len(self.control_points) - 1
        for i, P in enumerate(self.control_points):
            point += comb(n, i) * ((1 - t) ** (n - i)) * (t ** i) * P
        return point

    def get_curve_points(self, num_points=100):
        t_values = np.linspace(0, 1, num_points)
        return [self.B_t(t) for t in t_values]

    def draw_curve(self, screen, num_points=100):
        curve_points = self.get_curve_points(num_points)
        for i in range(len(curve_points) - 1):
            start_pos = curve_points[i]
            end_pos = curve_points[i + 1]
            pygame.draw.line(screen, (255, 255, 255), start_pos.astype(int), end_pos.astype(int), 2)

    def draw_control_points(self, screen):
        for point in self.control_points:
            pygame.draw.circle(screen, (255, 0, 0), point.astype(int), 6)

# Variables
curves = []  # list of BezierCurve objects
dragging = False
dragging_point = (None, None)  # (curve_index, point_index)

# Add the first curve
curves.append(BezierCurve(np.array([[100, 500], [400, 100], [700, 500]], dtype=float)))

running = True
while running:
    clock.tick(FPS)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Left click: drag a point
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            for ci, curve in enumerate(curves):
                for pi, point in enumerate(curve.control_points):
                    if np.linalg.norm(point - [mouse_x, mouse_y]) < 10:
                        dragging = True
                        dragging_point = (ci, pi)

        # Right click: create new curve
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_x, mouse_y = event.pos
            offset = 200
            new_curve = BezierCurve(np.array([[mouse_x - offset, mouse_y],[mouse_x, mouse_y - offset],[mouse_x + offset, mouse_y]], dtype=float))
            curves.append(new_curve)

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            dragging_point = (None, None)

        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = event.pos
            ci, pi = dragging_point
            curves[ci].control_points[pi] = np.array([mouse_x, mouse_y])

    # Draw everything
    for curve in curves:
        curve.draw_curve(screen)
        curve.draw_control_points(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
