import Tkinter as tk
import thread, time, threading, sys, math, random, multiprocessing
from numpy import *

WIDTH 	= 1200
HEIGHT	= 800
GRIDSIZE = 100
PERIOD	= 0.1
PLANTAGE = 20
PLANTMATURE = 14
height_m = 10
height_ax = 5
height_px = 10
height_ay = 5
height_py = 15

xo	= array([1,0])
yo	= array([0,1])

c	= 10.0




def lengthof(somevector):
	return sqrt(dot(somevector,somevector))

def distanceof(p1,p2):
	return lengthof(p2-p1)


class nodeC(object):

	nodenum = 0

	def __init__(self,position=None,v=None,typ=None,r=None):
		nodeC.nodenum += 1
		self.nodeid = nodeC.nodenum
		
		rand1 = random.random()
		rand2 = random.random()

		if position!=None:
			self.position=position
		else:
			self.position=array([rand1*WIDTH,rand2*HEIGHT])
			
		self.newp = self.position

		if v!=None:
			self.v=v
		else:
			self.v=array([0,0])
		
		if typ!=None:
			self.typ = typ
		else:
			self.typ=1

		if r!=None:
			self.r = r
		else:
			self.r = 5

		self.f=array([0,0])
		
		self.colliq = []

		if self.typ==1:
			self.shape=canvas.create_oval
			self.color = 'green'
		elif self.tpy==2:
			self.shape=canvas.create_rectangle
			self.color = 'red'
		
		self.obj = self.create_shape()
	def create_shape(self):
		self.obj = self.shape(int(self.position[0]-self.r),int(self.position[1]-self.r),int(self.position[0]+self.r),int(self.position[1]+self.r),fill = self.color)
		return self.obj

	def delete_shape(self):
		canvas.delete(self.obj)

	def request(self):
		self.newp = self.position + self.v

	def hitby(self,node):
		pass
		#print 'node[%d] is hit by node[%d]'%(self.nodeid,node.nodeid)

	def collision(self):
		for collio in self.colliq:
			if collio=='north':
				self.v[1]=-self.v[1]
				self.newp[1]=-self.newp[1]
			elif collio=='south':
				self.v[1] = -self.v[1]
				self.newp[1] = 2.0*HEIGHT-self.newp[1]
			elif collio=='west':
				self.v[0] = -self.v[0]
				self.newp[0] = -self.newp[0]
			elif collio=='east':
				self.v[0]=-self.v[0]
				self.newp[0] = 2.0*WIDTH-self.newp[0]
			else:
				po = (collio.newp-self.newp)/distanceof(collio.newp, self.newp)
				pol = array([-po[1],po[0]])
				vco = (self.r*dot(self.v,po)+collio.m*dot(collio.v,po))/(self.r+collio.m)
				v1o = 2*vco - dot(self.v,po)
				v2o = 2*vco - dot(collio.v,po)
				self.v = v1o*po+dot(self.v,pol)*pol
				collio.v = v2o*po +dot(collio.v,pol)*pol
				self.newp = self.position
				collio.newp = collio.position
				self.hitby(collio)
				#collio.hitby(self)
		self.collio=[]

	def grant(self):
		self.position=self.newp
		self.v=self.v+self.f
		self.delete_shape()
		self.create_shape()
# END of class nodeC

class plantC(nodeC):
	
	def __init__(self,position=None,v=None,typ=1,r=3):
		nodeC.__init__(self,position=position,v=v,typ=1,r=3)
		self.age = 0
		self.area = self.r
		self.m = self.r
		self.shadow = 0
		self.cangrow = 0
	
	def grow(self):
		self.age += 1
		#self.area = self.r - self.shadow
		if self.r <= 1:
			self.die()
		else:
			if self.age <= PLANTAGE:
				if self.r < PLANTMATURE:
					if self.shadow==0: # and self.cangrow==1:
						self.r += height[int(self.position[0])][int(self.position[1])]/height_m #= self.r + self.area/2 - self.age/3
						
				else:
					pass
					self.givebirth()
					#self.r -= 3
			else:
				self.r -= 1 #self.age
				
				
	def givebirth(self):
		rand1 = random.random()
		rand2 = random.random()
		newposition = self.position + array([rand1*100-50,rand2*100-50])
		#print self.position
		#print newposition
		if newposition[0] > 0 and newposition[0]<WIDTH and newposition[1] >0 and newposition[1] < HEIGHT:
			nq.append(plantC(position=newposition))
		#print 'give birth at',newposition
		
	def die(self):

		canvas.delete(self.obj)

		nq.remove(self)

		#print 'plant %d died'%self.obj
		
	def request(self):
		nodeC.request(self)
		
	def grant(self):
		nodeC.grant(self)
		self.grow()
		
	def collision(self):
		#self.shadow = 0
		for collio in self.colliq:
			if collio=='north':
				self.r = 0
				#self.v[1]=-self.v[1]
				#self.newp[1]=-self.newp[1]
				pass
			elif collio=='south':
				self.r = 0
				#self.v[1] = -self.v[1]
				#self.newp[1] = 2.0*HEIGHT-self.newp[1]
				pass
			elif collio=='west':
				self.r = 0
				#self.v[0] = -self.v[0]
				#self.newp[0] = -self.newp[0]
				pass
			elif collio=='east':
				self.r = 0
				#self.v[0]=-self.v[0]
				#self.newp[0] = 2.0*WIDTH-self.newp[0]
				pass
			else:
				#shadow = self.r+collio.r-distanceof(self.position,collio.position)
				#if shadow > self.r:
				#	shadow=self.r
				#elif shadow <0:
				#	shadow=0
				self.shadow = 1
				if collio.typ==1:
					collio.shadow = 1
				#self.hitby(collio)
				#collio.hitby(self)
		self.collio=[]
		



def mytimer():
	global loopcount
	global mutex
	global timeup
	lastcount = -1
	while True:
		time.sleep(PERIOD)
		if loopcount!=lastcount:
			mutex.acquire()
			canvas.update()
			mutex.release()
			lastcount=loopcount
		if timeup.isSet():
			pass
		else:
			timeup.set()

stop = 0

def stop(event):
	global stop
	stop = 1
	print stop

def timeisup(event):
	global loopcount
	global stop
	stop = 0
	gridsize = {}
	grid = {}
	i = 0
	j = 0
	for x in range(0,WIDTH,150):
		gridsize[i] = {}
		for y in range(0,HEIGHT,150):
			gridsize[i][j]=(x-PLANTMATURE,x+150+PLANTMATURE,y-PLANTMATURE,y+150+PLANTMATURE)
			j += 1
		i += 1

	while stop==0:
		#timeup.wait()
		#timeup.clear()
		time.sleep(PERIOD)
		time1 = time.time()
		# stage 1
		for node in nq:
			node.request()
			
		# stage 2
		grid = {}
		for node in nq:
			#xa = []
			#ya = []
			(i,x) = divmod(int(node.newp[0]),GRIDSIZE)
			if x <= PLANTMATURE and i!=0:
				xa = (i-1,i)
				pass
			elif x >= GRIDSIZE- PLANTMATURE and i!=(WIDTH/GRIDSIZE):
				xa = (i,i+1)
				pass
			else:
				xa = (i,)
			(j,y) = divmod(int(node.newp[1]),GRIDSIZE)
			if y <= PLANTMATURE and j!=0:
				ya = (j-1,j)
				pass
			elif y >= GRIDSIZE- PLANTMATURE and j!=(HEIGHT/GRIDSIZE):
				ya = (j,j+1)
				pass
			else:
				ya = (j,)
				
			for xi in xa:
				for yj in ya:
					if xi not in grid:
						grid[xi]={}
					if yj not in grid[xi]:
						grid[xi][yj] = []
					grid[xi][yj].append(node)
		#print grid
		for i in range(0,WIDTH/GRIDSIZE):
			if i in grid:
				for j in range(0,HEIGHT/GRIDSIZE):    
					if j in grid[i]:
						for k in range(0,len(grid[i][j])):
							if grid[i][j][k].newp[1]<0:
								grid[i][j][k].colliq.append('north')
							if grid[i][j][k].newp[1]>HEIGHT:
								grid[i][j][k].colliq.append('south')
							if grid[i][j][k].newp[0]<0:
								grid[i][j][k].colliq.append('west')
							if grid[i][j][k].newp[0]>WIDTH:
								grid[i][j][k].colliq.append('east')
							for l in range(k+1,len(grid[i][j])):
								if distanceof(grid[i][j][k].newp,grid[i][j][l].newp)<(grid[i][j][k].r+grid[i][j][l].r):
									if grid[i][j][l] not in grid[i][j][k].colliq:
										grid[i][j][k].colliq.append(grid[i][j][l])
							grid[i][j][k].collision()
			
		#for i in range(0,len(nq)):
		#	if nq[i].newp[1]<0:
		#	if nq[i].newp[1]>HEIGHT:
		#		nq[i].colliq.append('south')
		#	if nq[i].newp[0]<0:
		#		nq[i].colliq.append('west')
		#	if nq[i].newp[0]>WIDTH:
		#		nq[i].colliq.append('east')
		#	for j in range(i+1,len(nq)):
		#		if distanceof(nq[i].newp,nq[j].newp)<(nq[i].r+nq[j].r):
		#			nq[i].colliq.append(nq[j])
		#	nq[i].collision()

		# stage 3
		mutex.acquire()
		for node in nq:
			node.grant()
		mutex.release()
		
		time2=time.time()
		canvas.update()
		
p1 = threading.Thread(target=mytimer)
p1.setDaemon(True)
p2 = threading.Thread(target=timeisup)
p2.setDaemon(True)

def test1():
	while True:
		time.sleep(1)
		print time.time()
		
#t3 = threading.Thread(target=test1)
#t3.setDaemon(True)
#t3.start()

if __name__=='__main__':
	canvas = tk.Canvas(width=WIDTH, height=HEIGHT, bg='gray')
	canvas.pack()
	
	img = tk.PhotoImage(width=WIDTH,height=HEIGHT)
	canvas.create_image((WIDTH/2,HEIGHT/2),image=img,state="normal")
	height = []
	for xi in range(0,WIDTH):
		print xi
		height.append([])
		x=float(xi)
		for yi in range(0,HEIGHT):
			y=float(yi)
			height[xi].append(height_m+height_ax*math.sin(x/WIDTH*height_px)+height_ay*math.cos(y/HEIGHT*height_py))
			light = (height[xi][yi])/20.0*(16**3)
			img.put('#%03x%03x%03x'%(light,light,light),(xi,yi))
	canvas.update()
	#print height

	canvas.bind('<ButtonPress-1>', timeisup)
	canvas.bind('<Double-1>', stop)
	loopcount = 0

	timeup= threading.Event()
	mutex = threading.Lock()

	#p1 = multiprocessing.Process(target=mytimer)
	#p2 = multiprocessing.Process(target=timeisup)


	nq=[]
	nq.append(plantC())

	#p1.start()
	#p2.start()

	tk.mainloop()


