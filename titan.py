import Tkinter as tk
import thread, time, threading, sys, math, random
from numpy import *

WIDTH 	= 1200
HEIGHT	= 800
PERIOD	= 2
PLANTAGE = 5
PLANTMATURE = 10

xo	= array([1,0])
yo	= array([0,1])

c	= 10.0


canvas = tk.Canvas(width=WIDTH, height=HEIGHT, bg='gray')
canvas.pack()

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
		print 'node[%d] is hit by node[%d]'%(self.nodeid,node.nodeid)

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
				collio.hitby(self)
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
	
	def grow(self):
		self.age += 1
		self.area = self.r - self.shadow
		if self.age <= PLANTAGE:
			if self.r < PLANTMATURE:
				self.r = self.r + self.area - self.age
			else:
				self.givebirth()
				self.r -= 3
		else:
			self.r -= self.age
			if self.r <= 1:
				self.die()
				
	def givebirth(self):
		rand1 = random.random()
		rand2 = random.random()
		newposition = self.position + array([rand1*100-50,rand2*100-50])
		print self.position
		print newposition
		nq.append(plantC(position=newposition))
		print 'give birth at',newposition
		
	def die(self):
		canvas.delete(self.obj)
		nq.remove(self)
		print 'plant %d died'%self.obj
		
	def request(self):
		nodeC.request(self)
		
	def grant(self):
		nodeC.grant(self)
		self.grow()
		
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
				shadow = self.r+collio.r-distanceof(self.position,collio.position)
				self.shadow = shadow
				if collio.typ==1:
					collio.shadow = shadow
				self.hitby(collio)
				collio.hitby(self)
		self.collio=[]
		

loopcount = 0

timeup= threading.Event()
mutex = threading.Lock()

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
t1 = threading.Thread(target=mytimer)
#t1.setDaemon(True)

def timeisup():
	global loopcount
	global mutex

	while True:
		#timeup.wait()
		#timeup.clear()
		time.sleep(PERIOD)
		time1 = time.time()
		# stage 1
		for node in nq:
			node.request()

		# stage 2
		for i in range(0,len(nq)):
			if nq[i].newp[1]<0:
				nq[i].colliq.append('north')
			if nq[i].newp[1]>HEIGHT:
				nq[i].colliq.append('south')
			if nq[i].newp[0]<0:
				nq[i].colliq.append('west')
			if nq[i].newp[0]>WIDTH:
				nq[i].colliq.append('east')
			for j in range(i+1,len(nq)):
				if distanceof(nq[i].newp,nq[j].newp)<(nq[i].r+nq[j].r):
					nq[i].colliq.append(nq[j])
			nq[i].collision()

		# stage 3
		mutex.acquire()
		for node in nq:
			node.grant()
		mutex.release()
		
		time2=time.time()

t2 = threading.Thread(target=timeisup)
#t2.setDaemon(True)

def test1():
	while True:
		time.sleep(1)
		print time.time()
		
t3 = threading.Thread(target=test1)
t3.setDaemon(True)
t3.start()

nq=[]
nq.append(plantC())

t1.start()
t2.start()

tk.mainloop()


