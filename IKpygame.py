import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Root (bahu)
ROOT = pygame.Vector2(400, 300)

# Panjang tulang
L1 = 150
L2 = 120

# Pilih arah siku (+1 atau -1)
POLE = -1   # ganti -1 untuk sisi lain

def clamp(x, a, b):
    return max(a, min(b, x))

def ik_2bone(root, target, l1, l2, pole=1):
    d = target - root
    D = d.length()

    # Cegah jangkauan berlebih
    D = clamp(D, abs(l1 - l2) + 1e-6, l1 + l2 - 1e-6)

    # Arah ke target
    beta = math.atan2(d.y, d.x)

    # ---- Sudut siku (tanpa acos) ----
    c2 = (l1*l1 + l2*l2 - D*D) / (2*l1*l2)
    c2 = clamp(c2, -1, 1)
    s2 = pole * math.sqrt(1 - c2*c2)
    theta2 = math.atan2(s2, c2)

    # ---- Sudut antara L1 dan D ----
    ca = (l1*l1 + D*D - l2*l2) / (2*l1*D)
    ca = clamp(ca, -1, 1)
    sa = math.sqrt(1 - ca*ca)
    alpha = math.atan2(sa, ca)

    # Sudut bahu
    theta1 = beta - alpha

    return theta1, theta2

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    mouse = pygame.Vector2(pygame.mouse.get_pos())

    theta1, theta2 = ik_2bone(ROOT, mouse, L1, L2, POLE)

    # Posisi siku
    elbow = ROOT + pygame.Vector2(
        math.cos(theta1),
        math.sin(theta1)
    ) * L1

    # Posisi tangan
    hand = elbow - pygame.Vector2(
        math.cos(theta1 + theta2),
        math.sin(theta1 + theta2)
    ) * L2

    # Gambar tulang
    pygame.draw.line(screen, (0, 200, 255), ROOT, elbow, 5)
    pygame.draw.line(screen, (0, 255, 100), elbow, hand, 5)

    # Titik
    pygame.draw.circle(screen, (255, 255, 255), ROOT, 6)
    pygame.draw.circle(screen, (255, 100, 100), elbow, 6)
    pygame.draw.circle(screen, (255, 255, 0), hand, 6)
    pygame.draw.circle(screen, (255, 0, 0), mouse, 5, 1)

    pygame.display.flip()

pygame.quit()
