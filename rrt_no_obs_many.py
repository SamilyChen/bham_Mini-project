#Stratigy:randomly generate n(NUMNODES) nodes in each loop

import sys
import random
import math
import pygame
from pygame.locals import *
from math import sqrt,cos,sin,atan2
import time


##constances
XDIM = 640				#width of the environment
YDIM = 480				#width of the environment
WINSIZE = [XDIM, YDIM]	#Dimension of the visible area
EPSILON = 7.0			#Distance of a newly sampled node from the tree
NUMNODES = 10			#Number of iteration/nodes you want
RADIUS=15				#Radius to look for parent and rewiring
#constances for pygame environment
BLACK = 20, 20, 40
WHITE = 255, 240, 200
PINK = 200, 20, 240
#label
FIND=False

class Node:
	x=0
	y=0
	cost=0
	parent=None
	def __init__(self,xcoord, ycoord):
		self.x = xcoord
		self.y = ycoord

def dist(p1,p2):
	return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))
	
def step_from_to(p1,p2):
	if dist(p1,p2)<EPSILON:
		return p2
	else:
		theta=atan2(p2[1]-p1[1],p2[0]-p1[0])
		return p1[0]+EPSILON*cos(theta),p1[1]+EPSILON*sin(theta)
		
def chooseParent(nn,newnode,nodes):
	for p in nodes:
		if dist([p.x,p.y],[newnode.x,newnode.y]) <RADIUS and p.cost+dist([p.x,p.y],[newnode.x,newnode.y]) < nn.cost+dist([nn.x,nn.y],[newnode.x,newnode.y]):
			nn = p
	newnode.cost=nn.cost+dist([nn.x,nn.y],[newnode.x,newnode.y])
	newnode.parent=nn
	return newnode,nn
	
def reWire(nodes,newnode,pygame,screen):
	for i in xrange(len(nodes)):
		p = nodes[i]
		if p!=newnode.parent and dist([p.x,p.y],[newnode.x,newnode.y]) <RADIUS and newnode.cost+dist([p.x,p.y],[newnode.x,newnode.y]) < p.cost:
			pygame.draw.line(screen,WHITE,[p.x,p.y],[p.parent.x,p.parent.y])
			p.parent = newnode
			p.cost=newnode.cost+dist([p.x,p.y],[newnode.x,newnode.y])
			nodes[i]=p
			pygame.draw.line(screen,BLACK,[p.x,p.y],[newnode.x,newnode.y])
	return nodes
	
def drawSolutionPath(start,goal,nodes,pygame,screen):
	nn = nodes[0]
	for p in nodes:
		if dist([p.x,p.y],[goal.x,goal.y]) < dist([nn.x,nn.y],[goal.x,goal.y]):
			nn = p
	while nn!=start:
		pygame.draw.line(screen,PINK,[nn.x,nn.y],[nn.parent.x,nn.parent.y],5)
		nn=nn.parent
		

def main():
	#initialize and prepare screen
	pygame.init()
	screen = pygame.display.set_mode(WINSIZE)
	pygame.display.set_caption('RRTstar')
	screen.fill(WHITE)

	nodes = []
	i=0
	#nodes.append(Node(XDIM/2.0,YDIM/2.0)) # Start in the center
	nodes.append(Node(0.0,0.0)) # Start in the corner
	start=nodes[0]
	goal=Node(630.0,470.0) #the position of goal node
	time_start=time.time()
	while True:
		rands=[]
		for i in range(NUMNODES):
			rand = Node(random.random()*XDIM, random.random()*YDIM)
			rands.append(rand)
		nn = nodes[0]
		rn=rands[0]
		#finding the node of rands has nearest distance to goal position
		for p in rands:
			if dist([p.x,p.y],[goal.x,goal.y])<dist([rn.x,rn.y],[goal.x,goal.y]):
				rn=p
		#finding the node of rrt has nearest distance to rn
		for p in nodes:
			if dist([p.x,p.y],[rn.x,rn.y])<dist([nn.x,nn.y],[rn.x,rn.y]):
				nn=p
		rand=rn		
		interpolatedNode= step_from_to([nn.x,nn.y],[rand.x,rand.y])
		newnode = Node(interpolatedNode[0],interpolatedNode[1])
		[newnode,nn]=chooseParent(nn,newnode,nodes);
       
		nodes.append(newnode)
		pygame.draw.line(screen,BLACK,[nn.x,nn.y],[newnode.x,newnode.y])
		nodes=reWire(nodes,newnode,pygame,screen)
		pygame.display.update()
		#print i, "    ", nodes
		
		if dist([newnode.x,newnode.y],[goal.x,goal.y])<EPSILON:
			goal.parent=newnode
			nodes.append(goal)
			print "Find the path"
			break
		
		for e in pygame.event.get():
			if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
				sys.exit("Leaving because you requested it.")
				
	print ("iterations:%d"%i)
	print "times:",time.time()-time_start
	drawSolutionPath(start,goal,nodes,pygame,screen)
	pygame.display.update()
	
	# if python says run, then we should run
if __name__ == '__main__':
    main()
    running = True
    while running:
       for event in pygame.event.get():
	    if event.type == pygame.QUIT:
               running = False