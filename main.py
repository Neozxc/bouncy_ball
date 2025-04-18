import math
import pygame
import pymunk
import pymunk.pygame_util

def create_octagon(space, center, radius):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = center
    space.add(body)

    vertices = []
    for i in range(8):
        angle = math.radians(i * 45)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append((x, y))

    segments = []
    wall_thickness = 2
    for i in range(len(vertices)):
        a = vertices[i]
        b = vertices[(i + 1) % len(vertices)]
        seg = pymunk.Segment(body, a, b, wall_thickness)
        seg.elasticity = 1.0
        seg.friction = 0.5
        segments.append(seg)
        space.add(seg)

    return body, segments

def create_ball(space, position, radius=15):
    mass = 1
    inertia = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, inertia)
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.9
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape

def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Bouncing Ball")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, 500)

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    container_center = (width // 2, height // 2)
    container_radius = 200
    container_body, segments = create_octagon(space, container_center, container_radius)

    ball_start = (width // 2, height // 2 - 50)
    ball_body, ball_shape = create_ball(space, ball_start, radius=15)

    angular_speed = math.radians(60)
    dt = 1 / 60.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        container_body.angle += angular_speed * dt

        space.step(dt)

        screen.fill((0, 0, 0))

        for seg in segments:
            a = container_body.local_to_world(seg.a)
            b = container_body.local_to_world(seg.b)
            pygame.draw.line(screen, (255, 255, 255),
                             (int(a.x), int(a.y)), (int(b.x), int(b.y)), 3)

        ball_pos = ball_body.position
        pygame.draw.circle(screen, (255, 0, 0),
                           (int(ball_pos.x), int(ball_pos.y)),
                           int(ball_shape.radius))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()