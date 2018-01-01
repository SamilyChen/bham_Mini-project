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

def obsDraw(pygame,screen):
	for o in OBS: 
		pygame.draw.rect(screen,BLUE,o)
		 
def dist(p1,p2):
	return sqrt((p1.x-p2.x)*(p1.x-p2.x)+(p1.y-p2.y)*(p1.y-p2.y))
	
def drawSolutionPath(start,goal,start_num,goal_num,path,map,pygame,screen):
	node=map[goal_num]
	next=map[path[goal_num]]#pre=path[goal_num]
	pre_num=path[goal_num]
	#draw line from goal to goal node of map
	pygame.draw.line(screen,PINK,[goal.x,goal.y],[node.x,node.y],5)
	#draw the path in map
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
	obsDraw(pygame,screen)
	
	path = []
	map=[]
	
	#nodes.append(Node(XDIM/2.0,YDIM/2.0)) # Start in the center
	#nodes.append(Node(0.0,0.0)) # Start in the corner
	start=Node(0.0,0.0)
	goal=Node(630.0,470.0)
	pygame.draw.circle(screen,RED,[int(goal.x),int(goal.y)],5,0)
	#add of goal and start into map
	map.append(start)
	map.append(goal)
	
	time_start=time.time()
	#randomly generate NUMNODES nodes
	#print "gennerate nodes"
	for i in range (NUMNODES):
		rand=Node(random.random()*XDIM, random.random()*YDIM)
		if checkIntersectPoints(rand,OBS):
			i-=1
		map.append(rand)
		#print i
		#print map[i].x
		#print map[i].y
	#print len(map)
	#build the map
	#print "build the map"
	for p in map:
		#print ""
		#print "1:",p.x
		#print "2:",p.y
		#print "3:",p.cost
		p.cost=[]
		#print "4:",p.neighbors
		p.neighbors=[]
		for i in map:
			if i.x!=p.x and i.y!=p.y and checkIntersect(p,i,OBS):
				p.neighbors.append(i)
				p.cost.append(dist(p,i))
				#draw map
				pygame.draw.line(screen,YELLOW,[p.x,p.y],[i.x,i.y])
				pygame.display.update()
			else:
				p.neighbors.append(i)
				p.cost.append(float('inf'))
		#print "2:",p.cost
	#find the path		
	path=dijkstra(map,0)
	#print path
	print "time:",time.time()-time_start
	drawSolutionPath(start,goal,0,1,path,map,pygame,screen)
	pygame.display.update()
	
		
		
if __name__ == '__main__':
    main()
    running = True
    while running:
       for event in pygame.event.get():
	    if event.type == pygame.QUIT:
               running = False