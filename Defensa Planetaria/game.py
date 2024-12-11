import pygame
import random
import math
import threading
import time

pygame.init()

# Pantalla
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Defensa Planetaria - Computación Paralela")

# Imagenes
background_image = pygame.transform.scale(pygame.image.load('Defensa Planetaria/src/Background.png'), (400, 800)).convert()
cannon_image = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load('Defensa Planetaria/src/cannon.png').convert_alpha(), (100, 100)), 270
)
bullet_image = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load('Defensa Planetaria/src/bullet.png').convert_alpha(), (50, 50)), 270
)
meteor_image = pygame.transform.scale(pygame.image.load('Defensa Planetaria/src/meteor.png').convert_alpha(), (50, 50))

# Colores
WHITE = (255, 255, 255)

# Fuentes
font = pygame.font.Font("Defensa Planetaria/src/dogica.ttf", 20)

FPS = 60
clock = pygame.time.Clock()
score = 0  
level = 1
meteors_reached = 0

class Cannon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 90
        self.original_image = cannon_image
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y - 20))
        screen.blit(self.image, self.rect.topleft)

    def rotate(self, direction):
        self.angle += direction * 5
        self.angle = max(0, min(180, self.angle))

class Bullet(threading.Thread):
    def __init__(self, x, y, angle):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.running = True
        self.image = pygame.transform.rotate(bullet_image, +self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def run(self):
        while self.running:
            self.x += self.speed * math.cos(math.radians(self.angle))
            self.y -= self.speed * math.sin(math.radians(self.angle))
            self.rect.center = (self.x, self.y - 20)
            time.sleep(0.02)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def stop(self):
        self.running = False

class Meteor(threading.Thread):
    def __init__(self, x, y, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.running = True
        self.image = meteor_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def run(self):
        while self.running:
            self.y += self.speed
            self.rect.center = (self.x, self.y)
            time.sleep(0.02)

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def stop(self):
        self.running = False

def check_collision(bullet, meteor):
    distance = math.sqrt((bullet.x - meteor.x) ** 2 + (bullet.y - meteor.y) ** 2)
    return distance < 20  

def show_score_and_level():
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT - 550))
    tittle_text = font.render("DEFENSA PLANETARIA", True, (254, 236, 25))
    screen.blit(tittle_text, (25, 15))
    pygame.draw.rect(screen, (0, 0, 0), (0, 560, WIDTH, HEIGHT))
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    level_text = font.render(f"LEVEL:{level}", True, WHITE)
    meteors_text = font.render(f"MISSED: {meteors_reached}/5", True, (255, 0, 0))
    screen.blit(score_text, (120, 570))
    screen.blit(level_text, (10, 55))
    screen.blit(meteors_text, (180, 55))
    
def increase_difficulty():
    global level
    level += 1

def game_over(bullets, meteors):
    for bullet in bullets:
        bullet.stop()
    for meteor in meteors:
        meteor.stop()
    
    font_big = pygame.font.Font("Defensa Planetaria/src/dogica.ttf", 30)
    over_text = font_big.render("GAME OVER", True, (255, 0, 0))
    pygame.draw.rect(screen, (0, 0, 0), (10, 190, WIDTH - 20, HEIGHT - 400), 0, 15)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 30))
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    exit()
    
def show_menu():
    menu_font = pygame.font.Font("Defensa Planetaria/src/dogica.ttf", 13)
    title_text = font.render("DEFENSA PLANETARIA", True, (254, 236, 25))
    start_text = menu_font.render("Presiona ENTER para Iniciar", True, WHITE)
    exit_text = menu_font.render("Presiona ESC para Salir", True, WHITE)

    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, (0, 0, 0), (10, 190, WIDTH - 20, HEIGHT - 400), 0, 15)
    screen.blit(title_text, (25, 230))
    screen.blit(start_text, (27, 280))
    screen.blit(exit_text, (40, 310))
    draw_borders()
    pygame.display.flip()

def show_instructions():
    font = pygame.font.Font("Defensa Planetaria/src/dogica.ttf", 12)
    instructions = [
        "INSTRUCCIONES",
        "> Usa las flechas izquierda",
        "y derecha para girar el cañón.",
        "> Presiona ESPACIO para",
        "disparar balas.",
        "¡Destruye tantos meteoritos ",
        "como puedas!",
        "Presiona ENTER para comenzar.",
    ]
    pygame.draw.rect(screen, (0, 0, 0), (10, 100, WIDTH - 20, HEIGHT - 200), 0, 15)
    for i, line in enumerate(instructions):
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, 150 + i * 40))
        screen.blit(text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def draw_borders():
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 5)

def main():
    global score, level, meteors_reached
    running = True
    game_started = False

    cannon = Cannon(WIDTH // 2, HEIGHT - 50)
    bullets = []
    meteor_speed = 2
    meteors = [Meteor(random.randint(25, WIDTH - 25), random.randint(-500, -50), meteor_speed) for _ in range(10)]
    for meteor in meteors:
        meteor.start()

    while running:
        screen.blit(background_image, (0, 0))
        draw_borders()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show_instructions()
                    game_started = True
                if event.key == pygame.K_ESCAPE:
                    running = False
                if game_started and event.key == pygame.K_SPACE:
                    bullet = Bullet(cannon.x, cannon.y, cannon.angle)
                    bullets.append(bullet)
                    bullet.start()

        if not game_started:
            show_menu()
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            cannon.rotate(1)
        if keys[pygame.K_RIGHT]:
            cannon.rotate(-1)

        cannon.draw()
        for bullet in bullets[:]:
            if 0 < bullet.x < WIDTH and 0 < bullet.y < HEIGHT:
                bullet.draw()
            else:
                bullet.stop()
                bullets.remove(bullet)

        for meteor in meteors[:]:
            if meteor.y < HEIGHT:
                meteor.draw()
            else:
                meteor.stop()
                meteors.remove(meteor)
                meteors_reached += 1

                if meteors_reached >= 5:
                    game_over(bullets, meteors)

            for bullet in bullets[:]:
                if check_collision(bullet, meteor):
                    bullet.stop()
                    bullets.remove(bullet)
                    meteor.stop()
                    meteors.remove(meteor)
                    score += 10

                    if score % 200 == 0:
                        increase_difficulty()
                        meteor_speed += 1
                        meteors_reached = 0

                    new_meteor = Meteor(random.randint(25, WIDTH - 25), random.randint(-500, -50), meteor_speed)
                    meteors.append(new_meteor)
                    new_meteor.start()
                    break

        show_score_and_level()
        pygame.display.flip()
        clock.tick(FPS)

    for bullet in bullets:
        bullet.stop()
    for meteor in meteors:
        meteor.stop()

    pygame.quit()


if __name__ == "__main__":
    main()