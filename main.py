import pygame
import random
import sys

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1000, 800
BOID_COUNT = 100
PERCEPTION_RADIUS = 100 
DESIRED_SEPARATION = 30
MAX_SPEED = 4
MAX_FORCE = 0.1

PREDATOR_DATA = {
    "prev_pos": pygame.Vector2(0, 0),
    "current_direction": pygame.Vector2(0, -1) 
}

class Boid:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(50, WIDTH-50), random.uniform(50, HEIGHT-50))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity.scale_to_length(random.uniform(2, MAX_SPEED))
        self.acceleration = pygame.Vector2(0, 0)

    def bounce_off_walls(self):
        """Hard bounce: reverse direction when hitting boundaries"""
        # Check Left and Right walls
        if self.position.x <= 0:
            self.position.x = 0
            self.velocity.x *= -1
        elif self.position.x >= WIDTH:
            self.position.x = WIDTH
            self.velocity.x *= -1
            
        # Check Top and Bottom walls
        if self.position.y <= 0:
            self.position.y = 0
            self.velocity.y *= -1
        elif self.position.y >= HEIGHT:
            self.position.y = HEIGHT
            self.velocity.y *= -1

    def apply_rules(self, flock):
        cohesion = self.calculate_cohesion(flock)
        separation = self.calculate_separation(flock)
        alignment = self.calculate_alignment(flock)

        self.acceleration += cohesion * 1.0
        self.acceleration += separation * 1.8 
        self.acceleration += alignment * 1.0

    def calculate_cohesion(self, flock):
        steering = pygame.Vector2(0, 0)
        center_of_mass = pygame.Vector2(0, 0)
        total = 0
        for other in flock:
            if other != self:
                if self.position.distance_to(other.position) < PERCEPTION_RADIUS:
                    center_of_mass += other.position
                    total += 1
        if total > 0:
            center_of_mass /= total
            desired = center_of_mass - self.position
            if desired.length() > 0: desired.scale_to_length(MAX_SPEED)
            steering = desired - self.velocity
            if steering.length() > MAX_FORCE: steering.scale_to_length(MAX_FORCE)
        return steering

    def calculate_separation(self, flock):
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in flock:
            if other != self:
                dist = self.position.distance_to(other.position)
                if 0 < dist < DESIRED_SEPARATION:
                    diff = self.position - other.position
                    diff /= dist
                    steering += diff
                    total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0: steering.scale_to_length(MAX_SPEED)
            steering -= self.velocity
            if steering.length() > MAX_FORCE: steering.scale_to_length(MAX_FORCE)
        return steering

    def calculate_alignment(self, flock):
        steering = pygame.Vector2(0, 0)
        avg_velocity = pygame.Vector2(0, 0)
        total = 0
        for other in flock:
            if other != self:
                if self.position.distance_to(other.position) < PERCEPTION_RADIUS:
                    avg_velocity += other.velocity
                    total += 1
        if total > 0:
            avg_velocity /= total
            if avg_velocity.length() > 0: avg_velocity.scale_to_length(MAX_SPEED)
            steering = avg_velocity - self.velocity
            if steering.length() > MAX_FORCE: steering.scale_to_length(MAX_FORCE)
        return steering

    def avoid_mouse(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        dist = self.position.distance_to(mouse_pos)
        if dist < 80: 
            desired = self.position - mouse_pos
            desired.scale_to_length(MAX_SPEED * 2.0) 
            steering = desired - self.velocity
            self.acceleration += steering * 0.4

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED: self.velocity.scale_to_length(MAX_SPEED)
        self.position += self.velocity
        self.acceleration *= 0

    def draw(self, screen):
        angle = self.velocity.angle_to(pygame.Vector2(0, -1))
        size = 8
        p1 = self.position + pygame.Vector2(0, -size).rotate(-angle)
        p2 = self.position + pygame.Vector2(-size/2, size/2).rotate(-angle)
        p3 = self.position + pygame.Vector2(size/2, size/2).rotate(-angle)
        pygame.draw.polygon(screen, (0, 255, 180), [p1, p2, p3])

def draw_dynamic_predator(screen):
    current_mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    movement_vec = current_mouse_pos - PREDATOR_DATA["prev_pos"]
    if movement_vec.length() > 2:
        PREDATOR_DATA["current_direction"] = movement_vec
    PREDATOR_DATA["prev_pos"] = current_mouse_pos
    angle = PREDATOR_DATA["current_direction"].angle_to(pygame.Vector2(0, -1))
    
    p_size = 22
    p1 = current_mouse_pos + pygame.Vector2(0, -p_size).rotate(-angle)
    p2 = current_mouse_pos + pygame.Vector2(-p_size/2, p_size/2).rotate(-angle)
    p3 = current_mouse_pos + pygame.Vector2(p_size/2, p_size/2).rotate(-angle)
    
    pygame.draw.polygon(screen, (220, 30, 30), [p1, p2, p3])
    pygame.draw.polygon(screen, (255, 255, 255), [p1, p2, p3], 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids: Physical Bounce Walls")
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    
    flock = [Boid() for _ in range(BOID_COUNT)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        screen.fill((10, 10, 25)) 
        
        for boid in flock:
            boid.apply_rules(flock)
            boid.avoid_mouse()
            boid.bounce_off_walls() # <--- Hard bounce logic added here
            boid.update()
            boid.draw(screen)
            
        draw_dynamic_predator(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()