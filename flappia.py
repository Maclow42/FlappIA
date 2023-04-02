import pygame
import math
import random

pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

FONT = pygame.font.Font(None, 36)

# Constantes de la simulation
GRAVITY = 0.15
FRICTION = 1

PIPE_SPACE = 200
PIPE_WIDTH = 50
PIPE_HEIGHT = 100

FPS = 60

class Bird:
	def __init__(self, x, y, mass):
		self.x = x
		self.y = y
		self.mass = mass
		self.vx = 0
		self.vy = 0
		self.alive = True
		self.rect = pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 10)

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
		self.rect = pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 10)
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
			
class Pipe:
	def __init__(self, x, y, h, l):
		self.x = x
		self.y = y
		self.h = h/2
		self.l = l
		screen_size = screen.get_size()
		r1 = pygame.draw.rect(screen, GREEN, (self.x, 0, self.l, self.y-self.h))
		r2 = pygame.draw.rect(screen, GREEN, (self.x, self.y+self.h, self.l, screen_size[1]-self.y+self.h))
		self.rect = (r1, r2)
		
	def update(self):
		screen_size = screen.get_size()
		r1 = pygame.draw.rect(screen, GREEN, (self.x, 0, self.l, self.y-self.h))
		r2 = pygame.draw.rect(screen, GREEN, (self.x, self.y+self.h, self.l, screen_size[1]-self.y+self.h))
		self.rect = (r1, r2)
	
	
class PipeGestionnary:
	def __init__(self, x, nb):
		self.nb = nb
		self.pipes = pipes = [Pipe(i*PIPE_SPACE + x,
						random.randint(PIPE_HEIGHT, screen.get_size()[1]-PIPE_HEIGHT),
						PIPE_HEIGHT, PIPE_WIDTH)
						for i in range(self.nb)]
	def update(self, move):
		for pipe in self.pipes:
			if move:
				pipe.x -= 1.5
			pipe.update()
		if self.pipes[0].x + self.pipes[0].l < 0:
			self.pipes[0].x = self.pipes[self.nb-1].x + PIPE_SPACE
			
		self.pipes = sorted(self.pipes, key=lambda p: p.x)
	

random.seed()
bird = Bird(100, screen.get_size()[1]//2, 10)
pipes = PipeGestionnary(screen.get_size()[1], 5)


clock = pygame.time.Clock()

score = 0


while True:
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
	if bird.rect.colliderect(pipes.pipes[0].rect[0]) or bird.rect.colliderect(pipes.pipes[0].rect[1]):
		bird.alive = False
	
	for pipe in pipes.pipes:
		if pipe.x - 0.5 <= bird.x and bird.x <= pipe.x + 0.5 :
			score += 1
			print(bird.x, pipe.x)
			break
		
	pipes.update(bird.alive)
	bird.update()
	
	text_score = FONT.render("Score : " + str(score), True, (255, 0, 0))
	screen.blit(text_score, (20, 20))
	
	# Rafraîchit l'affichage
	pygame.display.update()
	
	clock.tick(FPS)

