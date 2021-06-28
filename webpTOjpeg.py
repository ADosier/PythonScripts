# Created by Alec Dosier

# This script converts every .webp image in the current directory into .jpeg
# It keeps the initial images in the directory and renames all of the files to p1, p2, p3 ... pn

# to get this to run, you need to add the packages numpy, and webptools

import numpy as np
from webptools import webplib as webp
import os

print(' ')
# get names of files in directory
allfiles = os.listdir('.')

# filter out files with extension .webp
files = []
for f in allfiles:
    if f.endswith(".webp"):
        files.append(f)

print("Files found to convert:")
print(files)
print(' ')
size = len(files)
print("Number of files found:", size)

# creates file names ranging from p1.jpeg...pN.jpeg
newfile = []
for i in range(1, size+1):
    newfile.append('p'+str(i)+'.jpg')

print("newfile = %s" % newfile)

# call webp conversion for files in dir
    #print("TEST VALUE: ")
    #print (files[0], 'to ->', newfile[0])
    #print(webp.dwebp(files[0], newfile[0], "-o"))
print(type(files[0]), "and", type(newfile[0]))
for z in range(0, size):
    print("converting", files[z], "to", newfile[z])
    print(type(files[z]), "and", type(newfile[z]))
    webp.dwebp(files[z], newfile[z], '-o')






