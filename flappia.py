import pygame
import math
import random

pygame.init()
clock = pygame.time.Clock()

random.seed()

SCREEN_SIZE = (700, 500)
screen = pygame.display.set_mode(SCREEN_SIZE)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

FONT = pygame.font.Font(None, 36)

# Constantes de la simulation
GRAVITY = 0.15
FRICTION = 1

PIPE_SPACE = 200
PIPE_WIDTH = 50
PIPE_HEIGHT = 90

FPS = 60

class Bird:
	def __init__(self, x, y, mass):
		self.score = 0
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
		if self.y >= SCREEN_SIZE[1]:
			self.y = SCREEN_SIZE[1]
			self.vy = 0
			self.alive = False
			
class Pipe:
	def __init__(self, x, y, h, l):
		self.x = x
		self.y = y
		self.h = h/2
		self.l = l
		r1 = pygame.draw.rect(screen, GREEN, (self.x, 0, self.l, self.y-self.h))
		r2 = pygame.draw.rect(screen, GREEN, (self.x, self.y+self.h, self.l, SCREEN_SIZE[1]-self.y+self.h))
		self.rect = (r1, r2)
		
	def update(self):
		r1 = pygame.draw.rect(screen, GREEN, (self.x, 0, self.l, self.y-self.h))
		r2 = pygame.draw.rect(screen, GREEN, (self.x, self.y+self.h, self.l, SCREEN_SIZE[1]-self.y+self.h))
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
	




while True:
	bird = Bird(100, screen.get_size()[1]//2, 10)
	pipes = PipeGestionnary(screen.get_size()[1], 5)
	game = True
	while game:
		# Gestion des événements
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					bird.jump()
				if event.key == pygame.K_r:
					if not bird.alive and bird.y == SCREEN_SIZE[1]:
						game = False
						break
						

		# Efface l'écran
		screen.fill(WHITE)
		

		# Met à jour l'objet physique
		if bird.rect.colliderect(pipes.pipes[0].rect[0]) or bird.rect.colliderect(pipes.pipes[0].rect[1]):
			bird.alive = False
		
		for pipe in pipes.pipes:
			if pipe.x - 0.5 <= bird.x and bird.x <= pipe.x + 0.5 :
				bird.score += 1
				break
			
		pipes.update(bird.alive)
		bird.update()
		
		text_score = FONT.render("Score : " + str(bird.score), True, (255, 0, 0))
		screen.blit(text_score, (20, 20))
		
		if not bird.alive and bird.y == SCREEN_SIZE[1]:
			game_over_text = FONT.render("GAME OVER", True, (255, 0, 0))
			game_over_rect = game_over_text.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2))
			restart_text = FONT.render("press r to restart", True, (255, 0, 0))
			restart_rect = restart_text.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2+20))
			screen.blit(game_over_text, game_over_rect)
			screen.blit(restart_text, restart_rect)
			
		
		# Rafraîchit l'affichage
		pygame.display.update()
		
		clock.tick(FPS)

