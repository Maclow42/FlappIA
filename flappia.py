import pygame
import math
import random
import dnn
import numpy as np
import chainedList

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
NB_INDIVIDUAL = 1000
ELITE_PERCENTAGE = 1
MUTATION_PROB = 0.1

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
	
	def __init__(self, x, y, mass, init_param=True):
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
		self.parameters = dnn.initialisation([2, 10, 10, 1]) if init_param else None
		
	def reset(self):
		self.score = 0
		self.x = 100
		self.y = screen.get_size()[1]//2
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
			
	def makeDecision(self, next_pipe):
		X = np.array([(next_pipe.x+PIPE_WIDTH//2-self.x)/SCREEN_SIZE[0], (next_pipe.y-self.y)/SCREEN_SIZE[1]], ndmin=2).reshape(-1, 1)
		if dnn.predict(X, self.parameters):
			self.jump()

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
		
def buildGeneration(parents=[]):
	if parents == []:
		return [Bird(100, screen.get_size()[1]//2, 10) for _ in range(NB_INDIVIDUAL)]
		
	elite = []
	p = sorted(parents, key=lambda x: -x.score)

	nbElite = 5
	for i in range(nbElite):
		p[i].reset()
		elite.append(p[i])
	for i in range(nbElite):
		bird = Bird(100, screen.get_size()[1]//2, 10, False)
		p1 = random.randint(0, nbElite-1)
		p2 = p1
		bird.parameters = dnn.procreate(elite[p1].parameters, elite[p2].parameters, MUTATION_PROB)
		elite.append(bird)
	for i in range(NB_INDIVIDUAL - 2*nbElite):
		bird = Bird(100, screen.get_size()[1]//2, 10, False)
		p1 = random.randint(0, nbElite-1)
		p2 = random.randint(0, nbElite-1)
		while p1 == p2:
			p2 = random.randint(0, nbElite-1)
		bird.parameters = dnn.procreate(elite[p1].parameters, elite[p2].parameters, MUTATION_PROB)
		elite.append(bird)
	return elite
	


#Screen initialisation
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('FlappyIA')
birds = []
gen = 0
while True:
	gen += 1
	game_score = 0
	#Init bird and pipes
	birds = buildGeneration(birds)
	pipes = PipeGestionnary(300, 5)
	#Game const to control the game and reset it after a death
	game = True
	print(f"########## GENERATION N°{gen} ##########")
	while game:
		#Event gestion
		for event in pygame.event.get():
			#If display closed
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
						
		#Clear screen
		screen.fill(WHITE)
		
		#Search next pipe
		closest_id = 0
		while pipes.pipes[closest_id].x < birds[0].x:
			closest_id += 1
		
		if abs(pipes.pipes[closest_id].x - birds[0].x) <= 1:
			game_score += 1
				
		#If bird touch a pipe -> dead	
		nb_deads = 0
		for bird in birds:
			if bird.alive:
				if bird.rect.colliderect(pipes.pipes[0].rect[0]) or bird.rect.colliderect(pipes.pipes[0].rect[1]):
					bird.alive = False
				else:
					bird.score += 1
					
					#Update pipes and bird position
					bird.makeDecision(pipes.pipes[closest_id])
				
					bird.update()
			else:
				nb_deads += 1
			
		
		if NB_INDIVIDUAL == nb_deads:
			game = False
		else:
			pipes.update(True)
			
			#Score display
			text_score = FONT.render("Score : " + str(game_score), True, (255, 0, 0))
			screen.blit(text_score, (20, 20))
				
			#Refresh display
			pygame.display.update()
			
			clock.tick(FPS)
	
	print(f"score : {game_score}")

