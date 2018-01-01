#!/usr/bin/env python

import sys, random, math, pygame
from pygame.locals import *
from math import sqrt,cos,sin,atan2
from lineIntersect import *
from dikjstra import *
import time

#constants
XDIM = 640
YDIM = 480
WINSIZE = [XDIM, YDIM]
EPSILON = 7.0
NUMNODES = 20
RADIUS=15
#positions of the obstacles. In this example, I used three rectangles. The format of each rectangle is (left,top,width,height).
OBS=[(500,150,100,50),(300,80,100,50),(150,220,100,50),(190,190,100,100),(500,400,100,40)]

BLACK = 20, 20, 40
WHITE = 255, 240, 200
PINK = 200, 20, 240
YELLOW=255, 215, 0
BLUE=0, 0, 255
RED=255,0,0

class Node:
	x=0
	y=0
	cost=[]
	neighbors=[]
	def __init__(self,xcoord, ycoord):
         self.x = xcoord
         self.y = ycoord

def dist(p1,p2):
	return sqrt((p1.x-p2.x)*(p1.x-p2.x)+(p1.y-p2.y)*(p1.y-p2.y))
	
def drawSolutionPath(start,goal,start_num,goal_num,path,map,pygame,screen):
	#print "goal_num:",goal_num
	#print "strat_num",start_num
	#print path
	node=map[goal_num]
	next=map[path[goal_num]]#pre=path[goal_num]
	pre_num=path[goal_num]
	#draw line from goal to goal node of map
	pygame.draw.line(screen,PINK,[goal.x,goal.y],[node.x,node.y],5)
	#draw the path in map
	#print next
	#print start
	while pre_num!=start_num:
		pygame.draw.line(screen,PINK,[next.x,next.y],[node.x,node.y],5)
		node=next
		pre_num=path[pre_num]
		next=map[pre_num]
	#draw line from start_map to start
	pygame.draw.line(screen,PINK,[start.x,start.y],[node.x,node.y],5)

def main():
	pygame.init()
	screen = pygame.display.set_mode(WINSIZE)
	pygame.display.set_caption('PRM')
	screen.fill(WHITE)

	
	path = []
	map=[]
	
	#nodes.append(Node(XDIM/2.0,YDIM/2.0)) # Start in the center
	#nodes.append(Node(0.0,0.0)) # Start in the corner
	start=Node(0.0,0.0)
	goal=Node(630.0,470.0)
	pygame.draw.circle(screen,RED,[int(goal.x),int(goal.y)],5,0)
	map_goal=None
	map_start=None
	start_num=0
	goal_num=0
	
	time_start=time.time()
	#randomly generate NUMNODES nodes
	for i in range (NUMNODES):
		rand=Node(random.random()*XDIM, random.random()*YDIM)
		map.append(rand)
	#build the map
	for p in map:
		#add goal and start into map
		p.cost=[]
		p.neighbors=[]
		p.neighbors.append(start)
		p.cost.append(dist(p,start))
		goal.neighbors.append(p)
		goal.cost.append(dist(p,goal))
		for i in map:
			if i.x!=p.x and i.y!=p.y:
			
				p.neighbors.append(i)
				p.cost.append(dist(p,i))
				#draw map
				pygame.draw.line(screen,YELLOW,[p.x,p.y],[i.x,i.y])
				pygame.display.update()
	#find the nearest node to start 	
	temp_dist1=float('inf')
	temp_dist2=float('inf')
	temp_i=0
	for s in map:
		if dist(s,start) < temp_dist1:
			map_sart=s
			temp_dist1=dist(s,start)
			start_num=temp_i
		if dist(s,goal) < temp_dist2:
			map_goal=s
			temp_dist2=dist(s,goal)
			goal_num=temp_i
		temp_i=temp_i+1
	#find the path		
	path=dijkstra(map,start_num)
	print "time:",time.time()-time_start
	drawSolutionPath(start,goal,start_num,goal_num,path,map,pygame,screen)
	pygame.display.update()
	
		
		
if __name__ == '__main__':
    main()
    running = True
    while running:
       for event in pygame.event.get():
	    if event.type == pygame.QUIT:
               running = False
		

