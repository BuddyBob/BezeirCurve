import pygame
import sys
import numpy as np
from math import comb

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bezier Curve Visualization")
clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont("Arial", 18)

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
curves = []
dragging = False
dragging_point = (None, None)

# Current degree
current_n = 3  # Start with cubic

# Slider UI setup
slider_rects = {
    2: pygame.Rect(100, HEIGHT - 40, 80, 30),
    3: pygame.Rect(200, HEIGHT - 40, 80, 30)
}

def draw_slider():
    for n, rect in slider_rects.items():
        color = (0, 200, 0) if n == current_n else (70, 70, 70)
        pygame.draw.rect(screen, color, rect)
        label = font.render(f"n={n}", True, (255, 255, 255))
        screen.blit(label, (rect.x + 15, rect.y + 5))

# Add an initial curve
curves.append(BezierCurve(np.array([[100, 500], [300, 100], [500, 500], [700, 200]], dtype=float)))

running = True
while running:
    clock.tick(FPS)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Check slider clicks
            for n, rect in slider_rects.items():
                if rect.collidepoint(mouse_x, mouse_y):
                    current_n = n

            # Left-click: drag point
            if event.button == 1:
                for ci, curve in enumerate(curves):
                    for pi, point in enumerate(curve.control_points):
                        if np.linalg.norm(point - [mouse_x, mouse_y]) < 10:
                            dragging = True
                            dragging_point = (ci, pi)

            # Right-click: create new curve
            elif event.button == 3:
                offset = 200
                if current_n == 2:
                    # Quadratic
                    new_points = [[mouse_x - offset, mouse_y],[mouse_x, mouse_y - offset],[mouse_x + offset, mouse_y]]
                else:  
                    #cubic
                    new_points = [[mouse_x - offset, mouse_y],[mouse_x - offset//2, mouse_y - offset],[mouse_x + offset//2, mouse_y - offset],[mouse_x + offset, mouse_y]]
                curves.append(BezierCurve(np.array(new_points, dtype=float)))

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

    draw_slider()
    pygame.display.flip()

pygame.quit()
sys.exit()
