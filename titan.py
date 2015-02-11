import Tkinter as tk
import thread, time, threading, sys
import math, random

from numpy import *

WIDTH  = 1200
HEIGHT = 800

c = 10.0
xo = array([1,0])
yo = array([0,1])

canvas = tk.Canvas(width=WIDTH, height=HEIGHT, bg='gray')
canvas.pack()

	
def lengthof(a1):
	return sqrt(dot(a1,a1))
	
def distanceof(p1,p2):
	return lengthof(p2-p1)
	
class nodeC(object):
	
	nodenum = 0
	
	def __init__(self,position=None,v=None,typ=None,m=None):
		nodeC.nodenum = nodeC.nodenum+1
		self.nodeid = nodeC.nodenum
		rand1 = random.random()
		rand2 = random.random()
		
		if position!=None:
			self.position = position
		else:
			self.position = array([rand1*WIDTH,rand2*HEIGHT])
			
		self.newp = self.position
		
		if v!=None:
			self.v = v
		else:
			self.v = array([rand2*10-5,rand1*10-5])
		
		self.f = array([0,0])
		
		if typ!=None:
			self.typ = typ
		else:
			self.typ = 1
			
		if m!=None:
			self.m = m
		else:
			self.m = 20.0
			
		self.r = sqrt(self.m)
		
		self.colliq = []
		
		if self.typ==1: # 1 for vegetation
			self.obj = canvas.create_oval(int(self.position[0]-self.r),int(self.position[1]-self.r),int(self.position[0]+self.r),int(self.position[1]+self.r),fill = 'green')
		elif self.typ==2:
			self.obj = canvas.create_rectangle(int(self.position[0]-self.r),int(self.position[1]-self.r),int(self.position[0]+self.r),int(self.position[1]+self.r),fill = 'red')
			
	def movefrom(self):
		self.newp = self.position + self.v
		return self.newp
		
	def collision(self):
		
		for collio in self.colliq:
			if len(nq)<2: nq.append(nodeC())
			if collio=='north':
				self.v[1] = -0.5*self.v[1]
				self.newp[1] = -self.newp[1]
				pass
			elif collio=='south':
				self.v[1] = -0.5*self.v[1]
				self.newp[1] = 2.0*HEIGHT-self.newp[1]
				pass
			elif collio=='west':
				self.v[0] = -0.5*self.v[0]
				self.newp[0] = -self.newp[0]
				pass
			elif collio=='east':
				self.v[0] = -0.5*self.v[0]
				self.newp[0] = 2.0*WIDTH-self.newp[0]
				pass
			else:
				po = (collio.newp-self.newp)/distanceof(collio.newp, self.newp)
				pol = array([-po[1],po[0]])
				vco = (self.m*dot(self.v,po)+collio.m*dot(collio.v,po))/(self.m+collio.m)
				v1o = 2*vco - dot(self.v,po)
				v2o = 2*vco - dot(collio.v,po)
				self.v = v1o*po+dot(self.v,pol)*pol				
				collio.v = v2o*po + dot(collio.v,pol)*pol
				self.newp = self.position
				collio.newp = collio.position
				pass
		self.colliq=[]
		
	def moveto(self):
		canvas.move(self.obj,self.newp[0]-self.position[0],self.newp[1]-self.position[1])
		self.position = self.newp
		for node in nq:
			if node.nodeid==self.nodeid:
				pass
			elif node.typ==1:
				pass
			else:
				f=[0.0,0.0]
				f[0]=f[0]+c*node.m*(node.position[0]-self.position[0])/(((node.position[0]-self.position[0])**2+(node.position[1]-self.position[1])**2))
				f[1]=f[1]+c*node.m*(node.position[1]-self.position[1])/(((node.position[0]-self.position[0])**2+(node.position[1]-self.position[1])**2))
				self.v[0] = self.v[0] + f[0]
				self.v[1] = self.v[1] + f[1]

		self.r = sqrt(self.m)
		#canvas.setitem(self.obj,r=self.r)
		
class plantC(nodeC):
	def __init__(self,position=None,v=None,typ=None,m=None):
		if v==None:
			self.v = array([0,0])
		else:
			self.v = v
		self.typ = 1
		if position==None:
			self.position == array([500,500])
		else:
			self.position = position
		nodeC.__init__(self,position=self.position,v=self.v,typ=1,m=None)
		self.age = 0
		
	def movefrom(self):
		global loopcount
		self.age += 1
		nodeC.movefrom(self)
		if self.age%100==0:
			r1 = random.random()*60-30
			r2 = random.random()*60-30
			r=array([r1,r2])
			nq.append(plantC(position=self.position+r))

		
n1 = plantC(position=array([600,200]),v=array([0,0]),typ=1)
#n2 = nodeC(position=array([600,600]),v=array([0.0,0.0]),typ=1)
#n3 = nodeC(position=array([400,400]),v=array([0.0,-10.0]),typ=1)
#n4 = nodeC(position=array([800,400]),v=array([0.0,10.0]),typ=1)
nq = [n1]#,n3,n4]

loopcount = 0

mutex0 = threading.Lock()

timeup = threading.Event()

def mytimer(arg):
	global timeup
	global loopcount
	global mutex0
	lastcount = -1
	i = 0
	while True:
		#i = i + 1
		time.sleep(0.04)
		#timeup.set()
		#print 'in mytimer',i 
		if loopcount!= lastcount:
			mutex0.acquire()
			canvas.update()
			mutex0.release()
			lastcount = loopcount
		
#thread.start_new_thread(mytimer,(None,))	
t1 = threading.Thread(target=mytimer,args=(None,))
t1.setDaemon(True)
t1.start()


	
def timeisup(arg):
	global timeup
	global loopcount
	global mutex0
	parray = []
	while True: # This is the main body of program
		loopcount = loopcount + 1

		t1=time.time()
		if loopcount%100==0:
			if len(nq) <4:
				#nq.append(nodeC())
				pass
				
		# stage 1, get new position

		for node in nq:
			parray.append(node.movefrom())

		# stage 2, extract collision
		# suppose r<=10
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

		# stage 3,
		mutex0.acquire()
		for node in nq:
			node.moveto()
		mutex0.release()
		#canvas.update()
		#timeup.clear()
		t2=time.time()
		#print t2-t1,loopcount
		time.sleep(0.025)
		#timeup.wait()	
			
#thread.start_new_thread(timeisup,(None,))
t2 = threading.Thread(target=timeisup,args=(None,))
t2.setDaemon(True)
t2.start()

tk.mainloop()