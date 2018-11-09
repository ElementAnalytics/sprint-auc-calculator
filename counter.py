#!/usr/bin/env python

import sys
from PIL import Image, ImageFilter

filearg = sys.argv[1]

im = Image.open(filearg).convert('RGB')
out = Image.new(im.mode, im.size)


def isRed(pixel):
    return pixel[0] > 180 and  pixel[1] < 150 and  pixel[2] < 150

color_counts = {}

for r in range(im.size[0]):
    for c in range(im.size[1]):
        px = im.getpixel((r,c))
        x = color_counts.get(px,0)
        color_counts[px] = x + 1

def nextLargestColor():
  l = max(color_counts, key=color_counts.get)
  color_counts.pop(l,None)
  return l

background = nextLargestColor()
weekend = nextLargestColor()

underRed = 0
ignoreCol = 0
found = False
for x in range(im.size[0]):
    found = False
    canUse = False
    for y in range(im.size[1]):
        ry = (im.size[1] -1) - y
        found = found or isRed(im.getpixel((x,ry)))
        if(not found):
            underRed += 1
            out.putpixel((x,ry),(255,0,0))
        else:
            canUse = True
            out.putpixel((x,ry),(0,0,0))
    if(not canUse):
        underRed -= im.size[1]
        ignoreCol += 1
im.show()
out.show()

auc = float(underRed) / (float((im.size[0] - ignoreCol) * im.size[1]))
print(round(auc,3)) 
