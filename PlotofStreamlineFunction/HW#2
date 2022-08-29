# -*- coding: utf-8 -*-
""""
Created on Wed Oct 30 01:41:41 2019

@author: umut atakul
"""

import numpy as np

import matplotlib.pyplot as plt

X = []
Y = []

k = 2

psi=[]

for psi in range (1,10):
    teta = np.linspace (0,2*np.pi,360)
    
    x = psi**(1/k) * np.cos(teta)
    y = psi**(1/k) * np.sin(teta)
    
    X.append(x)
    Y.append(y)
plt.axis (xmin=-5,xmax=5,ymin=-5,ymax=5)
plt.figure(figsize=(10,10))
plt.xlabel ("X ekseni")
plt.ylabel ("Y ekseni")
plt.grid(True)
for a in range (len(X)):
    plt.plot(X[a],Y[a])
plt.show()
    
    
