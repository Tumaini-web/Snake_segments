import pygame
import math

pygame.init()

clock = pygame.time.Clock()

width, height = 600, 400
screen = pygame.display.set_mode((width, height))

# Constants
NUM_SEGMENTS = 500  # Adjust this to change the number of segments
SEGMENT_LENGTH = 1  # Length of each segment

class Segment:
    def __init__(self, x, y, length):
        self.length = length
        self.angle = 0
        self.b = pygame.math.Vector2(x, y)  # End of the segment
        self.a = pygame.math.Vector2(0, 0)  # Start of the segment
        self.calculate_A()

    def calculate_A(self):
        """Calculate the start point based on the end point and angle"""
        dx = self.length * math.cos(self.angle)
        dy = self.length * math.sin(self.angle)
        self.a = pygame.math.Vector2(self.b.x - dx, self.b.y - dy)

    def show(self, display):
        pygame.draw.line(display, (24, 129, 129), (self.a.x, self.a.y), (self.b.x, self.b.y), 3)

    def follow(self, target_x, target_y):
        """Make this segment follow a target position"""
        target = pygame.math.Vector2(target_x, target_y)
        self.angle = math.atan2(target.y - self.a.y, target.x - self.a.x)

        # Set `b` to the target position
        self.b = target

        # Recalculate `a`
        self.calculate_A()


# Create a list of segments
segments = [Segment(width // 2, height // 2, SEGMENT_LENGTH) for _ in range(NUM_SEGMENTS)]

running = True

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Update segments
    segments[-1].follow(mouse_pos[0], mouse_pos[1])  # The last segment follows the mouse
    for i in range(len(segments) - 2, -1, -1):  # Make each segment follow the next one
        segments[i].follow(segments[i + 1].a.x, segments[i + 1].a.y)

    # Draw segments
    for segment in segments:
        segment.show(screen)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
