# Author Jelly Lin

import numpy as np
import sys
import cv2
from PIL import Image
import Sketcher
import random
import time
import cv
import pygame, sys
import os
from pygame.locals import *

# Load pic by command
if __name__ == "__main__":
    if len(sys.argv) > 1:
        image = sys.argv[1]
    else:
		image = '11.jpg'

piecex = 4
piecey = 4

# Choose Numbers of Piece
pygame.init()
window = pygame.display.set_mode((500,380), 0, 32)
pygame.display.set_caption("Lines of mask")
num = []
for i in range(10):
	num.append(pygame.image.load('tmp/n' + str(i) + '.png'))
back = pygame.image.load("tmp/nx.png")
exit = 0

# Choose pieces
while True:
	if exit == 1 :
		break
	window.blit(back, (0, 0))
	window.blit(num[piecex], (60,90))
	window.blit(num[piecey], (350,90))
	for event in pygame.event.get():
		# Choose
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.pos[0] >= 70 and event.pos[0] <= 120 and event.pos[1] >= 35	 and event.pos[1] <= 70:
				if piecex != 9 :
					piecex = piecex + 1
			if event.pos[0] >= 70 and event.pos[0] <= 120 and event.pos[1] >= 290	 and event.pos[1] <= 330:
				if piecex != 1 :
					piecex = piecex - 1
			if event.pos[0] >= 400 and event.pos[0] <= 450 and event.pos[1] >= 35	 and event.pos[1] <= 70:
				if piecey != 9 :
					piecey = piecey + 1
			if event.pos[0] >= 400 and event.pos[0] <= 450 and event.pos[1] >= 290	 and event.pos[1] <= 330:
				if piecey != 1 :
					piecey = piecey - 1
			if event.pos[0] >= 220 and event.pos[0] <= 300 and event.pos[1] >= 330	 and event.pos[1] <= 370:
				exit = 1
	# Update The Display
	pygame.display.update()
	
# Create Window
cv2.namedWindow("origin", 1)

#get image size
qq = Image.open(image)
sizeX = qq.size[0]
sizeY = qq.size[1]

#mask
mask = cv.CreateImage((sizeX, sizeY), cv.IPL_DEPTH_8U, 1)
cv.Set(mask, cv.Scalar(255,255,255))
cv.SaveImage("tmp/white.jpg", mask)
mask = cv2.imread("tmp/white.jpg")

marker_mask = mask.copy()
marker_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
sketch = Sketcher.Sketcher([marker_mask, mask], lambda : ((0, 0, 0), 255))
#draw mask
random.seed(time.time())
for n in range(piecex):
	points = []
	points.append(0)
	points.append(n*500/piecex)
	for i in range(1*2):
		points.append(random.randint(0, 500))
		points.append(random.randint(n*500/piecex+50,n*500/piecex+150))
	points.append(sizeX*3)
	points.append(n*500/piecex)
	sketch.drawcubicspline(points)
for n in range(piecey):
	points = []
	points.append(n*500/piecey)
	points.append(0)
	for i in range(1*2):
		points.append(random.randint(n*500/piecey+50,n*500/piecey+150))
		points.append(random.randint(0, 500))
	points.append(n*500/piecey)
	points.append(sizeY*3)
	sketch.drawcubicspline(points)
	
im = cv2.imread(image)
cv2.imshow("origin", im)

# Slice pic into pieces
while True:
	c = cv2.waitKey()
	if c == ord('r'):

		ret,thresh = cv2.threshold(marker_mask,127,255,0)
		contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		count = len(contours)
		print count
		
		print "press r to run"
		
		# array for x,y split
		split_x = []
		split_y = []
		split_x1 = []
		split_y1 = []
		c = cv2.waitKey()
		if c == ord('r'):
			for x in range(count):
				pic = cv2.imread(image)
				#mask
				for y in range(count):
					cnt = contours[y]
					if (y != x):
						#draw black
						cv2.drawContours(pic,[contours[y]],0,(1,1,1,255),-1)
					leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
					rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
					topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
					bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
					if (y == x):
						split_x.append(leftmost[0])
						split_y.append(topmost[1])
						split_x1.append(rightmost[0])
						split_y1.append(bottommost[1])
						width = rightmost[0] - leftmost[0]
						height =  bottommost[1] - topmost[1]
						print ("puzzle" + str(y) + ": (" + str(leftmost[0]) + "," + str(topmost[1]) + ")\t" + "width: " + str(width) + "\theight: " + str(height))
						
				img = pic
				#make black into transparent
				
				cv2.imwrite('tmp/pic' + str(x) + '.png', img)
				img = Image.open('tmp/pic' + str(x) + '.png')
				img = img.convert("RGBA") 
				
				box = (split_x[x], split_y[x], split_x1[x], split_y1[x])
				img = img.crop(box)
				pixdata = img.load()

				for y1 in xrange(img.size[1]):
					for x1 in xrange(img.size[0]):
						if pixdata[x1, y1] == (1, 1, 1, 255):
							pixdata[x1, y1] = (255, 255, 255, 0)
				img.save('tmp/pic' + str(x) + '.png', "PNG")
				img = cv2.imread('tmp/pic' + str(x) + '.png')
			
				cv2.namedWindow("image" + str(x), 1)
				cv2.imshow("image" + str(x), img)
				
	if c == ord('q'):
		break
		
# Set Up Pygame Libary
pygame.init()

Screen_X = (int)(sizeX*1.5)
Screen_Y = (int)(sizeY*1.5)

# Set Up Window and Title
window = pygame.display.set_mode((Screen_X,Screen_Y), 0, 32)
pygame.display.set_caption('Jelly')
fitrange = 15
moving = -1

pic = []
DisX = []
DisY = []
X = []
Y = []
fit = []

putdistance = Screen_X / count	
for i in range(count):
	# Load Piece of Image
	pic.append(pygame.image.load('tmp/pic'+str(i)+'.png'))
	# Pieces Fit Distination
	DisX.append(Screen_X/2 - sizeX/2 + ( split_x[i] + split_x1[i] )/2)
	DisY.append(Screen_Y/2 - sizeY/2 + ( split_y[i] + split_y1[i] )/2)
	X.append(0)
	Y.append(0)
	fit.append(0)
	# Define Position Of Puzzles
	X[i-1] = putdistance*i
	
# Load background
background = pygame.image.load('bg.jpg')

print str(sizeX) + "," + str(sizeY)
for i in range(count):
	print str(i) +" : "+ str(DisX[i]) +","+ str(DisY[i])

# Main Loop
while True:
	
	# Search For Events
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
			
		# Moving
		if event.type == pygame.MOUSEBUTTONDOWN:
			if moving != -1:
				moving = -1
				break
			for i in range(count):
				if event.pos[0] >= X[i] and event.pos[0] <= X[i]+pic[i].get_width() and event.pos[1] >= Y[i] and event.pos[1] <= X[i]+pic[i].get_height():
					if fit[i] != 1 : 
						moving = i		
				#fit check
				for i in range(count):
					if event.pos[0] > DisX[i] - fitrange and event.pos[0] < DisX[i] + fitrange and event.pos[1] > DisY[i] - fitrange and event.pos[1] < DisY[i] + fitrange :
						print "fit"
						fit[i] = 1
						X[i] = DisX[i] - pic[i].get_width()/2
						Y[i] = DisY[i] - pic[i].get_height()/2
						
		if moving != -1:
			i = moving	
			X[i] = event.pos[0] - pic[i].get_width()/2
			Y[i] = event.pos[1] - pic[i].get_height()/2
			print str(event.pos[0]) + "," + str(event.pos[1])
			
	# Draw Background
	pygame.draw.rect(background, (0, 255, 0), (Screen_X/2 - sizeX/2, Screen_Y/2 - sizeY/2, sizeX, sizeY))
	window.blit(background, (0,0))
	# Draw pieces To Screen
	for i in range(count):
		window.blit(pic[i], (X[i], Y[i]))
	
	# Update The Display
	pygame.display.update()
    