

def dijkstra(map,start_num):
	s=[]
	pre=[]
	dist=[]
	#initialise
	for i in range(len(map)):
		if i!=start_num:
			s.append(False)
			pre.append(start_num)
			dist.append(map[i].cost[i])
		else:
			dist.append(0)
			s.append(True)
			pre.append(start_num)

	for i in range(len(map)-1):
		mindist=float('inf')
		u=start_num
		for j in range(len(map)):
			if  s[j]!=True and dist[j]<mindist:
				u=j
				mindist=dist[j]
		s[u]=True
		#print "u:",u
		for j in range(len(map)):
			#print "j:",j
			#print "s[j]:",s[j]
			#print "pre:",pre
			if s[j]!=True:
				#print "dist+map.cost:",dist[u]+map[u].cost[j]
				#print "dist:",dist[j]
				if (dist[u]+map[u].cost[j]< dist[j]):
					dist[j]=dist[u]+map[u].cost[j]
					pre[j]=u
		#print "dist:",dist
		#print "pre:",pre
		#print "s:",s	
	return pre
	
	