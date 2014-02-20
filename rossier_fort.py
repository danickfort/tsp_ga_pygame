# -*- coding: utf-8 -*-

import sys
import re
import random
from math import sqrt, pow

class City(object):
	def __init__(self,name,x,y):
		self.name=name
		self.x=x
		self.y=y
	
	def __str__(self):
		return "Name = %s, (%f, %f)"%(self.name,self.x,self.y)

class Individual(object):
	def __init__(self,travel):
		self.travel=travel
		self.distance=0.0
	
	def evaluate(self):
		# distance entre a et b (AB) = sqrt((xb-xa)^2+(yb-ya)^2)
		for i in range(len(cities)-1):
			xa=cities[self.travel[i]].x
			ya=cities[self.travel[i]].y
			xb=cities[self.travel[i+1]].x
			yb=cities[self.travel[i+1]].y
			
			# distance entre deux villes (AB)
			self.distance+=sqrt(pow(xb-xa,2)+pow(yb-ya,2))
		
		# revenir au point de d�part � la fin
		xa=cities[self.travel[-1]].x
		ya=cities[self.travel[-1]].y
		xb=cities[self.travel[0]].x
		yb=cities[self.travel[0]].y
		
		self.distance+=sqrt(pow(xb-xa,2)+pow(yb-ya,2))

# une liste d'objet City
cities=[]

N=1024
population=[]
intermediatePopulation=[]

def initPopulation():
	# 0 � N
	for i in range(N):
		# On g�n�re la liste des index
		l=list(range(len(cities)))
		# on m�lange la liste des index
		random.shuffle(l)
		# on l'ajoute dans la poplulation initiale des individus
		individual=Individual(list(l))
		individual.evaluate()
		population.append(individual)
	
	for individual in population:
		print("%s, %f"%(individual.travel,individual.distance))
		

#def evaluate(individual):
#	pass

def select():
	# Tri de la liste, individus ayant la distance la plus courte en premier.
	sorted_pop = sorted(population, key=lambda individual: individual.distance)
	#for i in sorted_pop:
	#	print(i.distance)
	# On cr�� un tableau avec la meilleure moiti� de la population
	besthalf_pop = sorted_pop[len(sorted_pop)/2:]
	intermediatePopulation = besthalf_pop

def cross():
	for i in range(0,len(intermediatePopulation)-2):
		

def mutate():
	pass

def ga_solve(file=None,gui=True,maxtime=0):
	if file==None:
		# afficher l'interface pour r�cup�rer les points (x, y)
		pass
	else:
		# lecture du fichier
		f=open(file,'r')
		lignes=f.readlines()
		f.close()
		
		for ligne in lignes:
			ligneSplited=ligne.split()
			cities.append(City(ligneSplited[0],float(ligneSplited[1]),float(ligneSplited[2])))
		
		for city in cities:
			print(city)
			
		initPopulation()
		# boucle
		select()

if __name__=="__main__":
	file=None
	gui=True
	maxtime=0
	
	if len(sys.argv)>1:
		if re.search("^[0-9A-Za-z_][0-9A-Za-z_.-][A-Za-z][0-9A-Za-z_.-]+$",sys.argv[-1]):
			file=sys.argv[-1]
		if '--no-gui' in sys.argv:
			gui=False
		if '--max-time' in sys.argv:
			index=sys.argv.index('--max-time')
			maxtime=int(sys.argv[index+1])
	else:
		sys.exit("Error : you must provide a list of cities in the parameter\n \
rossier_fort.py <cities file>\n \
Parameters : \n \
	--no-gui : start without the GUI\n \
	--max-time <time in ms>: how long should the algorithm run \n \
")
	
	ga_solve(file,gui,maxtime)

	
	print("file %s"%file)
	print("gui %d"%gui)
	print("maxtime %d"%maxtime)	