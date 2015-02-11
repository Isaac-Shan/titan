import Tkinter as tk
import thread, time, threading, sys
import math, random

from numpy import *

WIDTH  = 1200
HEIGHT = 800

xo = array([1,0])
yo = array([0,1])
c= 10.0
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
		
		if self.typ==1:
			self.obj = canvas.create_oval(int(self.position[0]-self.r),int(self.position[1]-self.r),int(self.position[0]+self.r),int(self.position[1]+self.r),fill = 'green')
		elif self.typ==2:
			self.obj = canvas.create_rectangle(int(self.position[0]-self.r),int(self.position[1]-self.r),int(self.position[0]+self.r),int(self.position[1]+self.r),fill = 'red')
			
	def movefrom(self):
		self.newp = self.position + self.v
		# cosume resourse
		#self.m = self.m - 0.01

		return self.newp
	def collision(self):
		
		for collio in self.colliq:
			if len(nq)<20: nq.append(nodeC())
			if collio=='north':
				self.v[1] = -self.v[1]
				self.newp[1] = -self.newp[1]
				pass
			elif collio=='south':
				self.v[1] = -self.v[1]
				self.newp[1] = 2.0*HEIGHT-self.newp[1]
				pass
			elif collio=='west':
				self.v[0] = -self.v[0]
				self.newp[0] = -self.newp[0]
				pass
			elif collio=='east':
				self.v[0] = -self.v[0]
				self.newp[0] = 2.0*WIDTH-self.newp[0]
				pass
			else:
				po = (collio.newp-self.newp)/distanceof(collio.newp, self.newp)
				pol = array([-po[1],po[0]])
				vco = (self.m*dot(self.v,po)+collio.m*dot(collio.v,po))/(self.m+collio.m)
				v1o = 2*vco - dot(self.v,po)
				v2o = 2*vco - dot(collio.v,po)
				self.v = v1o*po+dot(self.v,pol)*pol
				print 'collision,',collio.nodeid,collio.v
				collio.v = v2o*po + dot(collio.v,pol)*pol
				print 'collision,',collio.nodeid,collio.v
				self.newp = self.position
				collio.newp = collio.position
				pass
		self.colliq=[]
		
	def moveto(self):
		oldv = self.v
		canvas.move(self.obj,self.newp[0]-self.position[0],self.newp[1]-self.position[1])
		self.position = self.newp
		for node in nq:
			if node.nodeid==self.nodeid:
				pass
			else:
				f=[0.0,0.0]
				f[0]=f[0]+c*node.m*(node.position[0]-self.position[0])/(((node.position[0]-self.position[0])**2+(node.position[1]-self.position[1])**2))
				f[1]=f[1]+c*node.m*(node.position[1]-self.position[1])/(((node.position[0]-self.position[0])**2+(node.position[1]-self.position[1])**2))
				oldv = self.v
				self.v[0] = self.v[0] + f[0]
				self.v[1] = self.v[1] + f[1]
			#sys.exit(0)
			#time.sleep(1)
		self.r = sqrt(self.m)
		#canvas.setitem(self.obj,r=self.r)
		
		
n1 = nodeC(position=array([100,100]),v=array([5.0,-6.0]),typ=1)
nq = [n1]

timeup = threading.Event()

def mytimer(arg):
	global timeup
	while True:
		time.sleep(0.04)
		timeup.set()
		
thread.start_new_thread(mytimer,(None,))	




	
def timeisup(arg):
	global timeup
	loopcount = 0
	parray = []
	while True: # This is the main body of program
		loopcount = loopcount + 1
		t1=time.time()
		if loopcount%100==0:
			if len(nq) <50:
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
		for node in nq:
			node.moveto()
			
		canvas.update()
		timeup.clear()
		t2=time.time()
		#print t2-t1
		timeup.wait()	
			
thread.start_new_thread(timeisup,(None,))

tk.mainloop()