import cv2
from numpy import *

class Sketcher:
	def __init__(self, dests, colors_func):
		self.dests = dests
		self.colors_func = colors_func
		
	def clear(self, x, y):
		for dst, color in zip(self.dests, self.colors_func()):
			cv2.line(dst, (0,250), (500,250), (255,255,255), 255)
	
	def drawline(self, x, y, x1, y1):
		pt = (x, y)
		ptd = (x1, y1)
		for dst, color in zip(self.dests, self.colors_func()):
			cv2.line(dst, pt, ptd, color, 2)
			
	def drawpolyline(self, pts):
		for dst, color in zip(self.dests, self.colors_func()):
			cv2.polylines(dst, pts, 1, color, 2)
	
	def drawcubicspline(self, pts):	
		#lookup table
		s = arange(257)/256.0
		z = s[::-1]
		b = transpose(array((z*z*z,
						   3*z*z*s, 
						   3*z*s*s,
							 s*s*s)))
		#t for accuracy
		def cubicspline(c,t):	return dot(b[t],c)

		points = pts
		arr = array([points])
		cs = reshape((arr),(-1,4,2))
		prev_pt = cs[0][0]
		
		for (x,y) in [cubicspline(c,10*t) for c in cs for t in arange(20)]:
			#print str(x)+","+str(y)
			for dst, color in zip(self.dests, self.colors_func()):
				cv2.line(dst, (int(prev_pt[0]),int(prev_pt[1])), (int(x),int(y)), (1, 1, 1, 255), 2)
			prev_pt[0] = x
			prev_pt[1] = y
		cv2.namedWindow("QQ",1)
		for dst, color in zip(self.dests, self.colors_func()):
			cv2.imshow("QQ", dst)