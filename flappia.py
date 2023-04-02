import pygame
import math

pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Constantes de la simulation
GRAVITY = 0.15
FRICTION = 1

FPS = 60

class Bird:
	def __init__(self, x, y, mass):
		self.x = x
		self.y = y
		self.mass = mass
		self.vx = 0
		self.vy = 0
		self.alive = True

	def apply_force(self, fx, fy):
		ax = fx / self.mass
		ay = fy / self.mass
		self.vx += ax
		self.vy += ay
		
	def jump(self):
		if self.alive:
			self.vy = 0
			self.apply_force(0, -45)

	def update(self):
		pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 10)
		self.vx *= FRICTION
		self.vy *= FRICTION
		self.vy += GRAVITY
		self.x += self.vx
		self.y += self.vy
		if self.y <= 0:
			self.y = 0
			self.vy = 0
			self.alive = False
		if self.y >= 500:
			self.y = 500
			self.vy = 0
			self.alive = False
			


bird = Bird(100, 100, 10)
force_x = 0
force_y = 0
bird.apply_force(force_x, force_y)

clock = pygame.time.Clock()


while play:
	# Gestion des événements
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				bird.jump()

	# Efface l'écran
	screen.fill(WHITE)

	# Met à jour l'objet physique
	bird.update()
	
	# Rafraîchit l'affichage
	pygame.display.update()
	
	clock.tick(FPS)

