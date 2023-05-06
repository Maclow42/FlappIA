import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs, make_circles
from sklearn.metrics import accuracy_score, log_loss
from tqdm import tqdm
import random

def initialisation(dimensions):
	parametres = {}
	C = len(dimensions)
	np.random.seed()
	
	for c in range(1, C):
		parametres['W' + str(c)] = np.random.randn(dimensions[c], dimensions[c - 1])
		parametres['b' + str(c)] = np.random.randn(dimensions[c], 1)

	return parametres
	
	
def proba(x, y):
    """
    Calcule la probabilité z en fonction du quotient x/y.
    Plus x/y est proche de 0, plus z est proche de 1.
    """
    if x > y:
    	return proba(y, x)
    if y == 0:  # Évite la division par zéro
        return 0
    
    quotient = x / y
    z = 1 - abs(quotient)  # Calcule la probabilité en fonction du quotient
    
    return z
    
def procreate(p1, p2, prob):
	C = len(p1) // 2
	
	p = {}

	for c in range(1, C + 1):
		p['W' + str(c)] = np.copy(p1['W' + str(c)])
		p['b' + str(c)] = np.copy(p2['b' + str(c)])
		
		for i in range(p['W' + str(c)].shape[0]):
			for j in range(p['W' + str(c)].shape[1]):
				if(random.random() <= prob):
					p['W' + str(c)][i][j] = random.uniform(-0.5, 0.5)
				elif random.random() >= 0.5:
					p['W' + str(c)][i][j] = p2['W' + str(c)][i][j]
		for i in range(p['b' + str(c)].shape[0]):
			for j in range(p['b' + str(c)].shape[1]):
				if(random.random() <= prob):
					p['b' + str(c)][i][j] = random.uniform(-0.5, 0.5)
				elif random.random() >= 0.5:
					p['b' + str(c)][i][j] = p2['b' + str(c)][i][j]
	return p

def forward_propagation(X, parametres):
	activations = {'A0': X}

	C = len(parametres) // 2

	for c in range(1, C + 1):
		Z = parametres['W' + str(c)].dot(activations['A' + str(c - 1)]) + parametres['b' + str(c)]
		activations['A' + str(c)] = 1 / (1 + np.exp(-Z))

	return activations

def predict(X, parametres):
	activations = forward_propagation(X, parametres)
	C = len(parametres) // 2
	Af = activations['A' + str(C)]
	return Af >= 0.5

