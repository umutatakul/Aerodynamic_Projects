# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 05:46:58 2020

@author:Umut Atakul

e-mail:atakulumut@gmail.com


"""

import tkinter as tk
from tkinter import StringVar
from resolver import calculate
from tkinter import ttk




def calc():
    u_inf = float(kutu3.get())
    alpha = float(kutu4.get())
    N = int(kutu5.get())
    secilen=str(Combo.get())

    acc, coef = calculate(u_inf, alpha, N,secilen)
    accuracy.set(acc)
    cl.set(coef)
    


pencere=tk.Tk ()
pencere.title (" Panel Method Calc. 4 Digit NACA")
pencere.config(bg='white')
pencere.resizable (0,0)

accuracy = StringVar(pencere)
accuracy.set(0)

cl = StringVar(pencere)
cl.set(0)


gtu_resim=tk.PhotoImage (file="logo.ppm")
resim=tk.Label (pencere)
resim.config (image=gtu_resim)
resim.pack()


yazi1=tk.Label (pencere)
yazi1.config (text="Hesaplamak için değerleri giriniz")
yazi1.config (bg='white',
              font=('San Francisco',
                    10,
                    'bold',
                    'underline'))
yazi1.pack ()

yazi2 = tk.Label(pencere, text = "Profil Tipini Seçiniz",
                 bg='white')
yazi2.config (font=('San Francisco',
                    9,
                    ))
yazi2.pack ()

profiller=["naca0006",
           "naca0008",
           "naca0009",
           "naca0012",
           "naca0015",
           "naca0018",
           "naca0021",
           "naca0024",
           "naca1408",
           "naca1410",
           "naca1412",
           "naca2408",
           "naca2410",
           "naca2411",
           "naca2412",
           "naca2414",
           "naca2415",
           "naca2418",
           "naca2421",
           "naca2424",
           "naca4412",
           "naca4415",
           "naca4418",
           "naca4421",
           "naca4424",
           "naca6409",
           "naca6412",]

Combo = ttk.Combobox(pencere, values=profiller)
Combo.pack()



yazi3= tk.Label (pencere)
yazi3.config (text="Serbest akış hızını giriniz",
              bg='white',
              font=('San Francisco',
                    9,
                    )) #u_inf
yazi3.pack ()

kutu3= tk.Entry (pencere)
kutu3.pack ()

yazi4=tk.Label (pencere)
yazi4.config(text="Hücum açısını giriniz",
             bg='white',
              font=('San Francisco',
                    9,
                    )) #alpha
yazi4.pack ()

kutu4=tk.Entry (pencere)
kutu4.pack ()


yazi5=tk.Label (pencere)
yazi5.config (text="Bölünecek panel sayısını giriniz",
              bg='white',
              font=('San Francisco',
                    9,
                    )) #number of N
yazi5.pack ()

kutu5=tk.Entry (pencere)
kutu5.pack ()

buton1=tk.Button (pencere)
buton1.config (text="Hesapla")
buton1.config (command=calc,
               bg='navy',
               activebackground='light blue',
               fg='white')
buton1.configure (cursor= "spider")
buton1.pack ()



acc_l=tk.Label (pencere)
acc_l.config(text="accuracy:",
             bg='orange2')
#acc_l.pack ()

acc=tk.Label (pencere)
acc.config(textvariable=accuracy ,)
#acc.pack ()

coeff_l=tk.Label (pencere)
coeff_l.config(text="Cl:",
                bg='orange2',
                fg='white')
coeff_l.pack ()

coeff=tk.Label (pencere)
coeff.config(textvariable=cl ,
              bg='orange2',
              fg='white')
coeff.pack ()

buton2=tk.Button (pencere)
buton2.config (text="Çıkış")
buton2.config (bg="red3",
               activebackground='salmon')
buton2.config (fg="white")
buton2.config (command=pencere.destroy)
buton2.pack ()



pencere.mainloop ()
