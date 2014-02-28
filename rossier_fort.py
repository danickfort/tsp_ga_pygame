# -*- coding: utf-8 -*-

# D�veloppeurs:
# -> Matthieu Rossier, INF3B-DLM
# -> Danick Fort, INF3B-DLM
# ALGORITHME GENETIQUE - Intelligence Artificielle - He-Arc

# version de python utilis�: python 3.3.0

import sys
import copy
import re
import random
import pygame
import time
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
from datetime import datetime
from math import hypot

# Repr�sente une ville, une ville est cract�ris� par
# -> un nom de ville
# -> une position (x, y)
class City(object):
	# Constructeur
	def __init__(self,name,x,y):
		self.name=name
		self.x=x
		self.y=y
	# Permet d'afficher � l'�cran une ville
	def __str__(self):
		return "Name = %s, (%f, %f)"%(self.name,self.x,self.y)

# Repr�sente un individu dans une popupalation, un individu est caract�ris� par
# -> un "voyage": une liste d'index d'object "City". Les objets "City" sont stock� dans la variable globale "cities"
# -> la distance du voyage
class Individual(object):
	# Constructeur
	def __init__(self,travel):
		self.travel=travel
		self.distance=0.0
		self.evaluate()
	# m�thodue qui calcul la distance du "voyage"
	def evaluate(self):
		# distance entre a et b (AB) = sqrt((xb-xa)^2+(yb-ya)^2)
		for i in range(len(cities)-1):
			xa=cities[self.travel[i]].x
			ya=cities[self.travel[i]].y
			xb=cities[self.travel[i+1]].x
			yb=cities[self.travel[i+1]].y
			
			# distance entre deux villes (AB)
			self.distance+=hypot(xb-xa,yb-ya)
		
		# revenir au point de d�part � la fin
		xa=cities[self.travel[-1]].x
		ya=cities[self.travel[-1]].y
		xb=cities[self.travel[0]].x
		yb=cities[self.travel[0]].y
		
		self.distance+=hypot(xb-xa,yb-ya)
	# permet d'afficher un "voyage"
	def __str__(self):
		return str(self.travel)
	# permet d'afficher un "voyage"
	def __repr__(self):
		return "Parcours : " + str(self.travel) + "\nDistance : " + str(self.distance)
	# retourne la longueur du "voyage"
	def __len__(self):
		return len(self.travel)

# Test si deux individus (en terme de distance) sont identiques
def equals(individualA,individualB):
	individualDistanceA=individualA.distance
	individualDistanceB=individualB.distance
	return int(individualDistanceA)==int(individualDistanceB)

# une liste d'objet City
cities=[]
# repr�sente la nombre d'individu dans la population
N=2000
# repr�sente la population total
population=[]
# repr�sente la population interm�diaire (apr�s la phase de s�lection)
intermediatePopulation=[]

# initialisation de la GUI (pygame)
pygame.init()
# repr�sente la fen�tre (pygame)
window=None
# repr�senta la zone � dessiner (pygame)
screen=None
# initialiser la possibilit� de pouvoir dessiner du texte
font=pygame.font.Font(None,30)

# m�thode qui permet de dessiner du texte par rapport � des positions
def drawText(screen,text,x,y,textColor):
	t=font.render(text,True,textColor)
	textRect=t.get_rect()
	textRect.left=x
	textRect.top=y
	screen.blit(t,textRect)

# m�thode qui permet de dessiner un voyage d'un individu
# un cercle repr�sente une ville
def drawSolution(screen,citiesIndex):
	colorCircle=(10,10,200)
	radiusCircle=3
	
	screen.fill(0)
	for cityIndex in citiesIndex:
		pygame.draw.circle(screen,colorCircle,(int(cities[cityIndex].x),int(cities[cityIndex].y)),radiusCircle)
		pygame.display.flip()

# m�thode qui dessine les villes d'une solution
def drawCities(screen):
	colorCircle=(10,10,200)
	radiusCircle=3
	
	screen.fill(0)
	for city in cities:
		pygame.draw.circle(screen,colorCircle,(city.x,city.y),radiusCircle)
		pygame.display.flip()

# d�marre une interface GUI qui demande � l'utilisateur de choisir les positions des villes
def requestCities():
	width=500
	height=500
	window=pygame.display.set_mode((width,height))
	screen=pygame.display.get_surface()
	
	# tant que l'utilisateur ne quitte pas l'interface GUI
	flag=True
	while flag:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN and event.key == K_RETURN:
				flag=False
			elif event.type == MOUSEBUTTONDOWN:
				# r�cup�re les positions de la souris
				x,y=pygame.mouse.get_pos()
				# ajoute une ville � la liste globale
				cities.append(City("v%d"%(len(cities)),x,y))
				# on dessine les villes � l'�cran
				drawCities(screen)

# premi�re phase de l'AG
# -> on initialise une population al�atoire d'individu
def initPopulation():
	# 0 � N
	# N => nombre d'individus
	for i in range(N):
		# On g�n�re la liste des index
		l=list(range(len(cities)))
		# on m�lange la liste des index
		random.shuffle(l)
		# on l'ajoute dans la poplulation initiale des individus
		individual=Individual(list(l))
		population.append(individual)

# deuxi�me phase de l'AG
def select():
	# tri de la liste, individus ayant la distance la plus courte en premier.
	sorted_pop = sorted(population, key=lambda individual: individual.distance)

	# la position du milieu de la liste
	half_point = len(sorted_pop)/2
	# repr�sente un index
	curr = 0
	selected_pop = []
	
	# �a s�lectionne un individu par rapport � l'index "curr"
	while (len(selected_pop) < half_point):
		selected_pop.append(sorted_pop[curr])
		# on fait varier l'index curr "al�atoirement"
		# ceci est utile pour laisser une chance aux individus "moins bon" ne faisant pas partie de la premi�re partie des meilleurs
		curr = curr + random.randint(1,2)

	# on cr�� un tableau avec la meilleure moiti� de la population
	# selected_pop = sorted_pop[:int(len(sorted_pop)/2)]
	for i in selected_pop:
		intermediatePopulation.append(i)

# troisi�me phase de l'AG
# l'�tape du croisement permet depuis deux parent de donner deux enfants
# nous avois choisi comme algorithme: croisement par des deux points
def cross():
	for individual_index in range(0,len(intermediatePopulation),2):
		crossover(intermediatePopulation[individual_index].travel,intermediatePopulation[individual_index+1].travel)

def crossover(parent1,parent2):
	"""
	croisement par deux points
	"""
	crossover_point1 = random.randint(0, len(parent1) - 1)
	crossover_point2 = random.randint(crossover_point1, len(parent1))
	"""
	Get a list of items in parent2, starting from crossover_point2, which
	are not in the middle segment of parent1.
	"""
	unused = [x for x in parent2[crossover_point2:] +
	          parent2[:crossover_point2]
	          if x not in parent1[crossover_point1:crossover_point2]]
	"""
	Copy the middle segment from parent1 to child1, and fill in the empty
	slots from the unused list, beginning with crossover_point2 and
	wrapping around to the beginning.
	"""
	child1 = (unused[len(parent1) - crossover_point2:] +
	          parent1[crossover_point1:crossover_point2] +
	          unused[:len(parent1) - crossover_point2])

	"""
	Get a list of items in parent1, starting from crossover_point2, which
	are not in the middle segment of parent2.
	"""
	unused = [x for x in parent1[crossover_point2:] +
	          parent1[:crossover_point2]
	          if x not in parent2[crossover_point1:crossover_point2]]
	"""
	Copy the middle segment from parent1 to child1, and fill in the empty
	slots from the unused list, beginning with crossover_point2 and
	wrapping around to the beginning.
	"""
	child2 = (unused[len(parent1) - crossover_point2:] +
	          parent2[crossover_point1:crossover_point2] +
	          unused[:len(parent1) - crossover_point2])

	intermediatePopulation.append(Individual(child1))
	intermediatePopulation.append(Individual(child2))

# on choisi deux index al�atoires et croise dans la liste les deux villes repr�sent� par les index
def mutate():
	# m�lange des index des individus
	indices = list(range(0,len(intermediatePopulation)))
	random.shuffle(indices)

	# mutation dans 1% des cas
	for i in indices[:int(len(intermediatePopulation)/100)]:
		individual = intermediatePopulation[i]
		# r�cup�ration du voyage
		travel=individual.travel
		# index al�atoire 1 (firstIndex)
		firstIndex=random.randint(0,len(travel)-1)
		# index al�atoire 2 (secondIndex)
		secondIndex=random.randint(0,len(travel)-1)
		
		# �change des valeurs par rapport au deux index
		temp=travel[firstIndex]
		travel[firstIndex]=travel[secondIndex]
		travel[secondIndex]=temp
		
		# comme l'individu a �t� mut�, il faut recalculer la distance
		individual.evaluate()
		
# fonction principale du l'algorithme
def ga_solve(file=None,gui=True,maxtime=0):
	# si pas de fichier en entr�e
	if file==None:
		# afficher l'interface pour r�cup�rer les points (x, y)
		# fonction bloquante
		requestCities()
	# si on a un fichier text en entr�e
	else:
		# lecture du fichier
		f=open(file,'r')
		lignes=f.readlines()
		f.close()
		
		# synthaxe des lignes du fichier
		
		# ville1 x1 y1
		# ville2 x2 y2
		# ...
		for ligne in lignes:
			ligneSplited=ligne.split()
			cities.append(City(ligneSplited[0],float(ligneSplited[1]),float(ligneSplited[2])))
	
	# initialisation de la population initiale
	initPopulation()
	startTime=datetime.now()
	
	# m�morise le meilleur individu pr�c�dent
	previousElite=None
	elite = None
	# compteur incr�ment� si l'�lite revient plusieurs fois de suite
	previousEliteCounter=0
	
	counter=0
	flag=True
	# commence la boucle principale
	# deux conditions de terminaison
	# 1) le temps d�fini par --maxtime
	# 2) si l'�lite revient n fois
	while True:
		# s�lection de la population
		select()
		# coisement de la population
		# algorithme croisement sur deux points
		cross()
		# mutation de la population
		# 1% de la population
		mutate()
		
		# timespan repr�sente le dur�e du temps d�j� pass�
		timespan=datetime.now()-startTime
		if timespan.total_seconds()>maxtime:
			flag=False
		
		# copie de l population intermi�diare dans la population total
		for idx,el in enumerate(intermediatePopulation):
			population[idx] = el
		del intermediatePopulation[:]

		# recherche du meilleur
		sorted_pop = sorted(population, key=lambda individual: individual.distance)
		elite = sorted_pop[0]
		
		# Test si l'�lite revient 20x de suite
		numberOfApparition=100
		if previousElite is not None:
			# si le elite courant est identique � l'�lite pr�c�dent
			if equals(elite,previousElite):
				previousEliteCounter+=1
				if previousEliteCounter>numberOfApparition:
					flag=False
			else:
				previousEliteCounter=0
		# m�morisation de l'�lite pr�c�dent
		previousElite=elite
		
		# afficher le r�sultat
		if gui:
			path=[]
			for cityIndex in elite.travel:
				path.append((cities[cityIndex].x,cities[cityIndex].y))
				
			if file!=None:
				window=pygame.display.set_mode((500,500))
			
			screen=pygame.display.get_surface()
			screen.fill(0)
			drawSolution(screen,elite.travel)
			pygame.draw.lines(screen,(10,10,200),True,path)
			drawText(screen,str(counter)+" iterations",0,0,(255,255,255))
			drawText(screen,str(timespan),0,30,(255,255,255))
			pygame.display.flip()
		
		counter+=1
	
		if not flag:
			break
	
	# la fonction retourne la liste des noms des ville et "meilleur" distance
	return elite.distance, [cities[i].name for i in elite.travel]

if __name__=="__main__":
	import os
	
	file=None
	gui=True
	maxtime=0
	
	# il au moins > 1 param�tres
	if len(sys.argv)>1:
		# si le dernier param�tre est un nom de fichier valide, alors on le prend comme fichier d'entr�e
		if os.path.exists(sys.argv[-1]):
			file=sys.argv[-1]
		# est-ce que l'utilisateur veut une interface GUI qui affiche les r�sultats
		if '--nogui' in sys.argv:
			gui=False
		# d�finit le temps maximal que l'algorithme a pour s'ex�cuter
		if '--maxtime' in sys.argv:
			index=sys.argv.index('--maxtime')
			if isinstance(int(sys.argv[index+1]),int):
				maxtime=int(sys.argv[index+1])
	else:
		sys.exit("Error : you must provide a list of cities in the parameter\n \
rossier_fort.py <cities file>\n \
Parameters : \n \
	--nogui : start without the GUI\n \
	--maxtime <time in ms>: how long should the algorithm run \n \
")
	try:
		ga_solve(file,gui,maxtime)
	except KeyboardInterrupt:
		try:
			population[0]
			sys.exit("Elite at stop time : ", population[0])
		except:
			sys.exit("Exited")
