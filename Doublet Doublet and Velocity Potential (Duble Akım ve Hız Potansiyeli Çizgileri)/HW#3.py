# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 15:59:45 2022

@author: umut atakul
"""


import numpy as np

import matplotlib.pyplot as plt

mu = 2 * np.pi

teta = np.linspace (0,2*np.pi,360)

Xf = []
Yf = []
Xfn = []
Yfn = []

Xp = []
Yp = []
Xpn = []
Ypn = []

for fi in range (1,10):
    
    rfi = (mu * np.cos(teta)) / 2 * np.pi * fi
    
    xf = rfi * np.cos(teta)
    
    yf = rfi * np.sin (teta)
    
    xfn = -rfi * np.cos(teta)
    
    yfn = -rfi * np.sin (teta) 
    
    
    Xf.append(xf)
    
    Yf.append(yf)
    
    Xfn.append(xfn)
    
    Yfn.append(yfn)

for psi in range (1,10):
    
    rpsi = (mu * np.sin(teta)) / 2 * np.pi * psi
    
    xp = rpsi * np.cos(teta)
    
    yp = rpsi * np.sin (teta)
    
    xpn = -rpsi * np.cos(teta)
    
    ypn = -rpsi * np.sin (teta) 
    
    
    Xp.append(xp)
    
    Yp.append(yp)
    
    Xpn.append(xpn)
    
    Ypn.append(ypn)
    
plt.figure (figsize=(8,8))

ax = 100

plt.axis (xmin=-ax,xmax=ax,ymin=-ax,ymax=ax)

for a in range (len(Xf)):
    plt.title("Akım ve Hız Potansiyeli Çizgileri")
    plt.xlabel("x ekseni")
    plt.ylabel("y ekseni")
    plt.grid (True)
    plt.plot(Xf[a],Yf[a],'blue',Xp[a],Yp[a],'red',Xfn[a],Yfn[a],'blue',Xpn[a],Ypn[a],'red')
    
plt.show()
    
    
    
