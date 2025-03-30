import pygame
import sys
import numpy as np
from math import comb
import random 

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1400, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bezier Curve Visualization")
clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont("Arial", 18)

# BezierCurve class
class BezierCurve:
    def __init__(self, control_points, color=None):
        self.control_points = control_points
        self.color = color if color else self.random_color()

    def random_color(self):
        return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    # Calculate the point on the Bezier curve at parameter t
    # B(t) = sum(i=0 to n) [C(n, i) * (1-t)^(n-i) * t^i * P[i]]
    # where C(n, i) is the binomial coefficient, P[i] are the control points
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
            pygame.draw.circle(screen, self.color, point.astype(int), 6)

    """
    Calculate the derivative of the Bezier curve at parameter t.
    Issue was how do I find deriv when I dont know curves equation?
    The derivative of a Bezier curve can be calculated using the control points.

    The parametric derivative gives you the tangent
    """
    def derivative(self, t):
        n = len(self.control_points) - 1
        derivative = np.zeros(2)
        for i in range(n):
            diff = self.control_points[i + 1] - self.control_points[i]  # Vector between adjacent control points
            derivative += comb(n - 1, i) * ((1 - t) ** (n - 1 - i)) * (t ** i) * n * diff
        return derivative
    
    def get_point(self, t):
        return self.B_t(t)


# Variables
curves = []
dragging = False
dragging_point = (None, None)
current_n = 3
tangent_button_active = False
mouse_held = False
t = 0
speed = 0.01

# Slider UI setup
slider_rects = {
    2: pygame.Rect(100, HEIGHT - 40, 80, 30),
    3: pygame.Rect(200, HEIGHT - 40, 80, 30),
    4: pygame.Rect(300, HEIGHT - 40, 80, 30),
    5: pygame.Rect(400, HEIGHT - 40, 80, 30),
    6: pygame.Rect(500, HEIGHT - 40, 80, 30),
    7: pygame.Rect(600, HEIGHT - 40, 80, 30),
    8: pygame.Rect(700, HEIGHT - 40, 80, 30),
}
# Tangent button UI setup
tangent_button_rect = pygame.Rect(800, HEIGHT - 40, 80, 30)

def draw_slider():
    for n, rect in slider_rects.items():
        color = (0, 200, 0) if n == current_n else (70, 70, 70)
        pygame.draw.rect(screen, color, rect)
        label = font.render(f"n={n}", True, (255, 255, 255))
        screen.blit(label, (rect.x + 15, rect.y + 5))

def draw_tangent_button(active):
    color = (0, 200, 0) if active else (70, 70, 70)
    pygame.draw.rect(screen, color, tangent_button_rect)
    label = font.render("Tangent", True, (255, 255, 255))
    screen.blit(label, (tangent_button_rect.x + 5, tangent_button_rect.y + 5))


# Find the closest point on any curve to the mouse position and return the tangent vector at that point
def find_tangent(mouse_x, mouse_y):
    if not curves:
        return None, None

    closest_curve = None
    closest_distance = float('inf')
    closest_point = None
    closest_index = -1

    for curve in curves:
        curve_points = curve.get_curve_points(num_points=100)
        for i, point in enumerate(curve_points):
            distance = np.linalg.norm(point - np.array([mouse_x, mouse_y]))
            if distance < closest_distance:
                closest_distance = distance
                closest_point = point
                closest_curve = curve
                closest_index = i

    if closest_distance > 10:
        return None, None

    t = closest_index / 99
    tangent_vector = closest_curve.derivative(t)
    return closest_point, tangent_vector

# Add initial curve
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
            mouse_held = True

            # Slider select
            for n, rect in slider_rects.items():
                if rect.collidepoint(mouse_x, mouse_y):
                    current_n = n

            # Toggle tangent mode
            if tangent_button_rect.collidepoint(mouse_x, mouse_y):
                tangent_button_active = not tangent_button_active

            # Start dragging point
            for ci, curve in enumerate(curves):
                for pi, point in enumerate(curve.control_points):
                    if np.linalg.norm(point - [mouse_x, mouse_y]) < 10:
                        dragging = True
                        dragging_point = (ci, pi)

            #Right click create new curve dynamic 
            if event.button == 3:
                offset = 200
                new_points = []
                for i in range(current_n):
                    angle = (2 * np.pi / current_n) * i
                    x_offset = int(offset * np.cos(angle))
                    y_offset = int(offset * np.sin(angle))
                    new_points.append([mouse_x + x_offset, mouse_y + y_offset])
                curves.append(BezierCurve(np.array(new_points, dtype=float)))


        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            dragging_point = (None, None)
            mouse_held = False

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if dragging:
                ci, pi = dragging_point
                curves[ci].control_points[pi] = np.array([mouse_x, mouse_y])

    # Draw all curves
    for curve in curves:
        curve.draw_curve(screen)
        curve.draw_control_points(screen)

        point = curve.get_point(t)
        pygame.draw.circle(screen, (237, 36, 76), (int(point[0]), int(point[1])), 5)

    t += speed
    if t > 1:
        t = 0  # Restart dot at beginning



    # Draw tangent line if active and mouse is held
    if tangent_button_active and mouse_held:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        point, tangent = find_tangent(mouse_x, mouse_y)
        if point is not None:
            scale = 100
            unit_tangent = tangent / np.linalg.norm(tangent)
            p1 = point + unit_tangent * scale
            p2 = point - unit_tangent * scale
            pygame.draw.line(screen, (255, 0, 255), p1.astype(int), p2.astype(int), 4)

    # UI
    draw_slider()
    draw_tangent_button(tangent_button_active)

    pygame.display.flip()

pygame.quit()
sys.exit()
