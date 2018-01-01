#!/usr/bin/env python
#Stratigy:randomly generate n(NUMNODES) nodes in each loop
import sys, random, math, pygame
from pygame.locals import *
from math import sqrt,cos,sin,atan2
from lineIntersect import *
import time

#constants
XDIM = 640
YDIM = 480
WINSIZE = [XDIM, YDIM]
EPSILON = 7.0
NUMNODES = 100
RADIUS=15
#positions of the obstacles. In this example, I used three rectangles. The format of each rectangle is (left,top,width,height).
OBS=[(500,150,100,50),(300,80,100,50),(150,220,100,50),(190,190,100,100),(500,400,100,40)]

BLACK = 20, 20, 40
WHITE = 255, 240, 200
PINK = 200, 20, 240
BLUE=0,0,255
RED=255,0,0

def obsDraw(pygame,screen):
	for o in OBS: 
		pygame.draw.rect(screen,BLUE,o)

def dist(p1,p2):
	return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def step_from_to(p1,p2):
	if dist(p1,p2) < EPSILON:
		return p2
	else:
		theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
		return p1[0] + EPSILON*cos(theta), p1[1] + EPSILON*sin(theta)

def chooseParent(nn,newnode,nodes):
	for p in nodes:
		if checkIntersect(p,newnode,OBS) and dist([p.x,p.y],[newnode.x,newnode.y]) <RADIUS and p.cost+dist([p.x,p.y],[newnode.x,newnode.y]) < nn.cost+dist([nn.x,nn.y],[newnode.x,newnode.y]):
			nn = p
	newnode.cost=nn.cost+dist([nn.x,nn.y],[newnode.x,newnode.y])
	newnode.parent=nn
	return newnode,nn

def reWire(nodes,newnode,pygame,screen):
	for i in range(len(nodes)):
		p = nodes[i]
		if checkIntersect(p,newnode,OBS) and p!=newnode.parent and dist([p.x,p.y],[newnode.x,newnode.y]) <RADIUS and newnode.cost+dist([p.x,p.y],[newnode.x,newnode.y]) < p.cost:
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
	#i=0
	while nn!=start:
		#i=i+1
		#print ("%d:x=%d;y=%d"%(i,nn.x,nn.y))
		pygame.draw.line(screen,PINK,[nn.x,nn.y],[nn.parent.x,nn.parent.y],5)  
		nn=nn.parent


class Node:
    x = 0
    y = 0
    cost=0  
    parent=None
    def __init__(self,xcoord, ycoord):
         self.x = xcoord
         self.y = ycoord

def main():
	#initialize and prepare screen
	pygame.init()
	screen = pygame.display.set_mode(WINSIZE)
	pygame.display.set_caption('RRTstar')
	screen.fill(WHITE)
	obsDraw(pygame,screen)
	
	nodes = []
	i=0#for counting iteration 
    
	#nodes.append(Node(XDIM/2.0,YDIM/2.0)) # Start in the center
	nodes.append(Node(0.0,0.0)) # Start in the corner
	start=nodes[0]
	goal=Node(630.0,470.0)
	pygame.draw.circle(screen,RED,[int(goal.x),int(goal.y)],5,0)
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
		#finding the node of rrt has nearest distance to goal position==>iteration=99,times=1
		#for p in nodes:
		#	if dist([p.x,p.y],[goal.x,goal.y])<dist([nn.x,nn.y],[goal.x,goal.y]):
		#		nn=p
		#finding the node of rrt has nearest distance to rn
		for p in nodes:
			if dist([p.x,p.y],[rn.x,rn.y])<dist([nn.x,nn.y],[rn.x,rn.y]):
				nn=p
		#compare the distance of random node to goal and nearest node of rrt
		if dist([nn.x,nn.y],[goal.x,goal.y])<dist([rn.x,rand.y],[rn.x,goal.y]):
		#old distance < new distance
			continue
		rand=rn
		interpolatedNode= step_from_to([nn.x,nn.y],[rand.x,rand.y])
		
		newnode = Node(interpolatedNode[0],interpolatedNode[1])
		if checkIntersect(nn,rand,OBS):
			[newnode,nn]=chooseParent(nn,newnode,nodes);
			nodes.append(newnode)
			pygame.draw.line(screen,BLACK,[nn.x,nn.y],[newnode.x,newnode.y])
			nodes=reWire(nodes,newnode,pygame,screen)
			pygame.display.update()
			
			if dist([newnode.x,newnode.y],[goal.x,goal.y])<EPSILON and checkIntersect(newnode,goal,OBS):
				goal.parent=newnode
				nodes.append(newnode)
				print "Find the path"
				break
			for e in pygame.event.get():
				if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
					sys.exit("Leaving because you requested it.")
	print ("iterations:%d"%i)
	print "times:",time.time()-time_start
	#print ("length:%d"%(len(nodes)))
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