import pygame
import math
import random

#Initialisation of pygame
pygame.init()
clock = pygame.time.Clock()

#Random init
random.seed()

#Visual Constants
SCREEN_SIZE = (700, 500)
#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
#Font
FONT = pygame.font.Font(None, 36)

#Game constants
PIPE_SPACE = 200
PIPE_WIDTH = 50
PIPE_HEIGHT = 90
PIPE_SPEED = 1.5
GRAVITY = 0.15

#Execution speed
FPS = 60

class Bird:
	"""
	Class Bird
	Attributs:
		-> x : horizontal position
		-> y : vertical position
		-> mass : mass of the bird
		-> vy : vertical speed
		-> alive : state of the bird (true = alive, false = dead)
		-> rect : visual pygame element of bird
	"""
	
	def __init__(self, x, y, mass):
		"""
		Bird constructor
		Parameters:
			-> x : horizontal initial position
			-> y : vertical initial position
			-> mass : mass of the bird
		"""
		
		self.score = 0
		self.x = x
		self.y = y
		self.mass = mass
		self.vy = 0
		self.alive = True
		self.rect = pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 10)

	def apply_force(self, fy):
		"""
		Apply a vertical force with a magnitude of fy to the bird
		Update self.vy consequently		
		"""
		self.vy += fy / self.mass
		
	def jump(self):
		"""
		Use apply_force to make jump the Bird
		"""
		if self.alive:
			self.vy = 0
			self.apply_force(-40)

	def update(self):
		"""
		Update the position, speed and display of the Bird
		Apply gravity and limit the vertical position (set self.alive to False if the ground or the ceiling is touched
		"""
		self.rect = pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 10)
		self.vy += GRAVITY
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
	"""
	Class Pipe
	Attributs:
		-> x : horizontal position
		-> y : vertical position of the hole
		-> h : vertical dimension of the hole
		-> l : width of the pipe
		-> rect : tuple (r1, r2) where r1 and r2 are the upper and the lower visual parts of the pipe
	"""
	
	def __init__(self, x, y, h, l):
		"""
		Pipe constructor
		Parameters:
			-> x : horizontal position of the pipe
			-> y : vertical position of the hole
			-> h : vertical dimension of the hole
			-> l : width of the pipe
		Init self.rect using those parameters
		"""
		self.x = x
		self.y = y
		self.h = h/2
		self.l = l
		r1 = pygame.draw.rect(screen, GREEN, (self.x, 0, self.l, self.y-self.h))
		r2 = pygame.draw.rect(screen, GREEN, (self.x, self.y+self.h, self.l, SCREEN_SIZE[1]-self.y+self.h))
		self.rect = (r1, r2)
		
	def update(self):
		"""
		Update display of pipe
		"""
		r1 = pygame.draw.rect(screen, GREEN, (self.x, 0, self.l, self.y-self.h))
		r2 = pygame.draw.rect(screen, GREEN, (self.x, self.y+self.h, self.l, SCREEN_SIZE[1]-self.y+self.h))
		self.rect = (r1, r2)
	
	
class PipeGestionnary:
	"""
	Class PipeGestionnary
	Attributs:
		-> nb : number of pipe
		-> pipes : list containing all the pipes
	"""
	
	def __init__(self, x, nb):
		"""
		PipeGestionnary constructor
		Parameters:
			-> x : initial position of the first pipe
			-> nb : number of pipes
		Init self.pipes with random pipes and each one spaced of PIPE_SPACE px
		"""
		self.nb = nb
		self.pipes = pipes = [Pipe(i*PIPE_SPACE + x,
						random.randint(PIPE_HEIGHT, screen.get_size()[1]-PIPE_HEIGHT),
						PIPE_HEIGHT, PIPE_WIDTH)
						for i in range(self.nb)]
	def update(self, move):
		"""
		Update the position of the all pipes using PIPE_SPEED constant
		Sort pipes by increasing horizontal position
		If one pipes disapear in the left side, it is replaced on the right
		"""
		for pipe in self.pipes:
			if move:
				pipe.x -= 1.5
			pipe.update()
		if self.pipes[0].x + self.pipes[0].l < 0:
			self.pipes[0].x = self.pipes[self.nb-1].x + PIPE_SPACE
			
		self.pipes = sorted(self.pipes, key=lambda p: p.x)
	


#Screen initialisation
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('FlappyIA')

while True:
	#Init bird and pipes
	bird = Bird(100, screen.get_size()[1]//2, 10)
	pipes = PipeGestionnary(SCREEN_SIZE[0], 5)
	#Game const to control the game and reset it after a death
	game = True
	while game:
		#Event gestion
		for event in pygame.event.get():
			#If display closed
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				#If spacebar pressed -> jump
				if event.key == pygame.K_SPACE:
					bird.jump()
				#Restart the game after a death
				if event.key == pygame.K_r:
					if not bird.alive and bird.y == SCREEN_SIZE[1]:
						game = False
						break
						
		#Clear screen
		screen.fill(WHITE)
		

		#If bird touch a pipe -> dead
		if bird.rect.colliderect(pipes.pipes[0].rect[0]) or bird.rect.colliderect(pipes.pipes[0].rect[1]):
			bird.alive = False
		
		#Score count -> searching the pipe where the bird is (okay it's not opti but don't juge)
		for pipe in pipes.pipes:
			if pipe.x - 0.5 <= bird.x and bird.x <= pipe.x + 0.5 :
				bird.score += 1
				break
			
		#Update pipes and bird position
		pipes.update(bird.alive)
		bird.update()
		
		#Score display
		text_score = FONT.render("Score : " + str(bird.score), True, (255, 0, 0))
		screen.blit(text_score, (20, 20))
		
		#Gameover gestion
		if not bird.alive and bird.y == SCREEN_SIZE[1]:
			game_over_text = FONT.render("GAME OVER", True, (255, 0, 0))
			game_over_rect = game_over_text.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2))
			restart_text = FONT.render("press r to restart", True, (255, 0, 0))
			restart_rect = restart_text.get_rect(center=(SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2+20))
			screen.blit(game_over_text, game_over_rect)
			screen.blit(restart_text, restart_rect)
			
		
		#Refresh display
		pygame.display.update()
		
		clock.tick(FPS)

