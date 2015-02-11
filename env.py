# what about a local change
import Tkinter as tk
import thread, threading, time
from threading import Timer
import math

from titan_def import *
import random
from numpy import *

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
		#height[xi].append(height_m+height_ax*math.sin(x/xrange_c*height_px)+height_ay*math.cos(y/yrange_c*height_py))
		#light = (height[xi][yi]-6)/8.0*(16**3)
		#img.put('#%03x%03x%03x'%(light,light,light),(xi,yi))
canvas.update()		


class node(object):
	
	def __init__(self):
		rand1 = random.random()
		rand2 = random.random()
		self.x=WIDTH/2.0 + rand1*100.0-50
		self.y=HEIGHT/2.0 + rand2*100.0-50
		self.r=10.0*rand1
		
		self.v=arange(2)
		self.v[0]=rand1*10.0-5.0
		self.v[1]=rand2*10.0-5.0
		
		# create this node
		self.obj=canvas.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill='red')
		
	def nmove(self):
		
		newx=self.x+self.v[0]
		newy=self.y+self.v[1]
		while not((newx>=0 and newx<=WIDTH) and (newy>=0 and newy<=HEIGHT)):
			if newx>WIDTH:
				newx=newx-2.0*(newx-WIDTH)
				self.v[0]=-self.v[0]
				nq.append(node())
			if newx<0:
				newx=-newx
				self.v[0]=-self.v[0]
				nq.append(node())
			if newy>HEIGHT:
				newy=newy-2.0*(newy-HEIGHT)
				self.v[1]=-self.v[1]
				nq.append(node())
			if newy<0:
				newy=-newy
				self.v[1]=-self.v[1]
				nq.append(node())
		deltax=newx-self.x
		deltay=newy-self.y
		self.x=newx
		self.y=newy
		#self.v=self.v*0.999
		canvas.move(self.obj,deltax,deltay)
		
n1 = node()
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
	while True:
		t1=time.time()
		for node1 in nq:
			node1.nmove()
		canvas.update()
		timeup.clear()
		t2=time.time()
		#print t2-t1
		timeup.wait()	
			
thread.start_new_thread(timeisup,(None,))

tk.mainloop()
