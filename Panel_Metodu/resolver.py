# -*- coding: utf-8 -*-
"""
Created on Thu Jan  16 19:02:52 2020




@author:Umut Atakul


e-mail:atakulumut@gmail.com
"""
import os # 'dat' dosyasını okutmak için kullanacağımız modül
import numpy as np
from scipy import integrate, linalg #İntegral almak ve Lineer Denklem sistemi
                                     #çözümü için SciPy kütüphaneisini
                                     #kullanıcaz
from matplotlib import pyplot







#Class sınıf tanımlamaya yarıyor ardından Panel diye 
#Sınıfın adını veriyoruz : ile blok başlangıcı yaptık.

class Panel:
    
    
    
    def __init__(self, xa, ya, xb, yb):#Panel yapısı ile ilgili
                                                #Sınıfı barındırır

        """
        I Panelin uç noktalarını,merkez noktalarını uzunluğunu ve x ekseni ile
        yaptığı açıyı hesaplatıyoruz.
        Panelin bulunduğu noktanın kanadının alt ya da üst yüzeye tekabül
        ettiği belirlenir.
        Paneli kaynak şiddeti, teğetsel hızı ve başınç katsayısı 0'dan 
        başlatılır
        """
        self.xa, self.ya = xa, ya  #panel başlangıç noktaları
        self.xb, self.yb = xb, yb  #panel bitiş noktaları
        
        self.xc, self.yc = (xa + xb) / 2, (ya + yb) / 2  #panel'in merkez koordinatları
        self.length = np.sqrt((xb - xa)**2 + (yb - ya)**2)  #panel uzunluğu
        
         # x ekseni ile panel normali arasındaki açı 
         #(panel konumunu tanımlalamıza yardımcı olacak)
        if xb - xa <= 0.0:
            self.beta = np.arccos((yb - ya) / self.length)
        elif xb - xa > 0.0:
            self.beta = np.pi + np.arccos(-(yb - ya) / self.length)
        
        # panel location
        if self.beta <= np.pi:
            self.loc = 'upper'  #Kanadın üst yüzeyi
        else:
            self.loc = 'lower'  #Kanadın alt yüzeyi
        
        self.sigma = 0.0  #kaynak gerilimi
        self.vt = 0.0  #Teğetsel hız
        self.cp = 0.0  #basınç katsayısı

class Freestream: #Serbest akım koşulları
    
    def __init__(self, u_inf=1.0, alpha=0.0):#Serbest akım hızını ve açısı
                                            #derece olarak ayarlanır
        """
        Parametreler
        ----------
        u_inf: Serbest akım sürati, reel sayı 
                Varsayım: 1.0
            
        alpha: Derece cinsinden hücum açısı
                Varsayım: 0.0
        """
        self.u_inf = u_inf
        self.alpha = np.radians(alpha)  # Dereceyi radyana çeviriyoruz
        
def define_panels(x, y, N=40):
    """
   Kosinüs yöntemi kullamılarak panel geometrisininin ayrıklaştırılması
    
    
    Parametreler
    ----------
    x: Geometriyi taımlayan x koorinatlarının bir boyutlu reel sayı dizisi
        
    y: Geometriyi taımlayan y koorinatlarının bir boyutlu reel sayı dizisi
    
    N: Panel sayısını bbelirleyen tam sayı 
        Varsayılan panel sayısı: 40.
    """
    
    R = (x.max() - x.min()) / 2.0  # çember çapı
    x_center = (x.max() + x.min()) / 2.0  # Çember merkezinin x koordinatı
    
    theta = np.linspace(0.0, 2.0 * np.pi, N + 1)  # Açı dizisi
    x_circle = x_center + R * np.cos(theta)  # Çemberin x koordinatı
    
    x_ends = np.copy(x_circle)  # Panel uç noktalarının x koordiantı
    y_ends = np.empty_like(x_ends)  # Panel uç noktalarını y koordinatı
    
    # Kapalı yüzey oluşturacak şekilde koordinatları uzatalım
    x, y = np.append(x, x[0]), np.append(y, y[0])
    
    # İz düşümleri ile y noktalarının iz düşümlerini
    I = 0
    for i in range(N):
        while I < len(x) - 1:
            if (x[I] <= x_ends[i] <= x[I + 1]) or (x[I + 1] <= x_ends[i] <= x[I]):
                break
            else:
                I += 1
        a = (y[I + 1] - y[I]) / (x[I + 1] - x[I])
        b = y[I + 1] - a * x[I + 1]
        y_ends[i] = a * x_ends[i] + b
    y_ends[N] = y_ends[0]
    
    # Panel nesnelerini oluşturma
    panels = np.empty(N, dtype=object)
    for i in range(N):
        panels[i] = Panel(x_ends[i], y_ends[i], x_ends[i + 1], y_ends[i + 1])
    
    return panels


def integral(x, y, panel, dxdk, dydk):
    """
    Verilen noktanın panele katkısını belirler
    
    Parametreler
    ----------
    x: Verilen noktanın x koordinatı.
    y: Verilen noktanın y koordinatı
    
    panel: Panel nesnesi
        (Katkısı değerlendirilen panel)
        
    dxdk: Belirli yöndeki x türevinin değeri
    
    dydk: Belirli yöndeki x türevinin değeri
    """
    def integrand(s):
        return (((x - (panel.xa - np.sin(panel.beta) * s)) * dxdk +
                 (y - (panel.ya + np.cos(panel.beta) * s)) * dydk) /
                ((x - (panel.xa - np.sin(panel.beta) * s))**2 +
                 (y - (panel.ya + np.cos(panel.beta) * s))**2) )
    return integrate.quad(integrand, 0.0, panel.length)[0]
    
    
def source_contribution_normal(panels):
    """
    Normal hızlar için kaynak katkısı matrisinin oluşturulması
   
    
    Parametreler
    ----------
    panels: Panel objelerinin listesi
    """
    A = np.empty((panels.size, panels.size), dtype=float)
    # Panele kendisinden olan kaynak katkısı
    np.fill_diagonal(A, 0.5)
    # Panele diğerlerinden olan kaynak katkısı
    for i, panel_i in enumerate(panels):
        for j, panel_j in enumerate(panels):
            if i != j:
                A[i, j] = 0.5 / np.pi * integral(panel_i.xc, panel_i.yc, 
                                                    panel_j,
                                                    np.cos(panel_i.beta),
                                                    np.sin(panel_i.beta))
    return A
    
    
def vortex_contribution_normal(panels):
    """
    Normal hızlar için girddap katkısı matrisinin oluşturulması
    
    Parametreler
    ----------
    panels: Panel objelerinin listesi
    """
    A = np.empty((panels.size, panels.size), dtype=float)
    # Panele kendisinden olan girdap katkısı
    np.fill_diagonal(A, 0.0)
    # Panele diğer panellerden olan kaynak katkısı
    for i, panel_i in enumerate(panels):
        for j, panel_j in enumerate(panels):
            if i != j:
                A[i, j] = -0.5 / np.pi * integral(panel_i.xc, panel_i.yc, 
                                                     panel_j,
                                                     np.sin(panel_i.beta),
                                                     -np.cos(panel_i.beta))
    return A
    


def kutta_condition(A_source, B_vortex):
    """
    Kutta şartları dizisinin oluşturulması.
    
    Parametreler
    ----------
    A_source:2 boyutlu Numpy reel sayı dizisi
    Normal hıza kaynak katkısına etkisi
    B_vortex: -
    A_source:2 boyutlu Numpy reel sayı dizisi
    Normal hıza girdap katkısına etkisi
    """
    b = np.empty(A_source.shape[0] + 1, dtype=float)
    #Teğetsel hızdaki kaynak katkısının matrisi
    #Normal hızın girdap katkısının matrisiyle aynıdır
    b[:-1] = B_vortex[0, :] + B_vortex[-1, :]
    #Teğetsel hızın girdap katkısının matrisi
    #Normal hızınkaynak katkısının matrisinin tersidir
    b[-1] = - np.sum(A_source[0, :] + A_source[-1, :])
    return b
    
def build_singularity_matrix(A_source, B_vortex):
    """
    Kaynak ve girdap katkısından meydana
    gelen sol taraftaki matris sisteminin  oluşturulması
    
    
    
    Parametreler
    ----------
    A_source: Normal hıza kaynak katkısının matrisi
        
    B_vortex: Normal hıza girdap katkısının matrisi
        
    
    
        Lineer sistemin matrisi döndürülür
    """
    A = np.empty((A_source.shape[0] + 1, A_source.shape[1] + 1), dtype=float)
    # Kaynak yapısının etkisinin matrisi
    A[:-1, :-1] = A_source
    # Vortex yapısının oluşturduğu etkilerin matrisi
    A[:-1, -1] = np.sum(B_vortex, axis=1)
    # Kutta şartının tanımlandığı sayı dizisi
    A[-1, :] = kutta_condition(A_source, B_vortex)
    return A

def build_freestream_rhs(panels, freestream):
    """
    Serbest akım katkısından meydana gelen sağ taraftaki 
    matris sisteminin oluşturulması
        
    Parametreler
    ----------
    panels: Panel objelerinin listesi
        
    freestream: Serbest akım şartları nesneleri
    
    Her panele ve Kutta şartına serbest akım katkısı 
    """
    b = np.empty(panels.size + 1, dtype=float)
    # Her panele serbest akımın katkısı
    for i, panel in enumerate(panels):
        b[i] = -freestream.u_inf * np.cos(freestream.alpha - panel.beta)
    # Kutta şartına serbest akıma katkısı
    b[-1] = -freestream.u_inf * (np.sin(freestream.alpha - panels[0].beta) +
                                 np.sin(freestream.alpha - panels[-1].beta) )
    return b
    


def compute_tangential_velocity(panels, freestream, gamma, A_source, B_vortex):
    """
    Yüzeydeki teğetsel hızların hesaplanması
    
    Parametreler
    ----------
    panels: Panel nesnelerin listesi
    freestream: Serbest akım şartının nesneleri
    gamma: Sirkülasyon yoğunluğu
    
    A_source: Normal hıza kaynak katkısının matrisi
    B_vortex: Normal hıza girdap katkısının matrisi..
    """
    A = np.empty((panels.size, panels.size + 1), dtype=float)
    #Teğetsel hıza katkı sağlayan kaynak elemanının matrisi ile
    #normal hıza katkı sağlayan elemanının matrisi aynıdır
    A[:, :-1] = B_vortex
   #Teğetsel hıza etkiyen  girdap elemanının matrisi ile
    #normal hıza etki sağlayan kaynak elemanın matrisi
    #birbirine terstir
    A[:, -1] = -np.sum(A_source, axis=1)
    # Serbest akımın katkısı
    b = freestream.u_inf * np.sin([freestream.alpha - panel.beta 
                                      for panel in panels])
    
    strengths = np.append([panel.sigma for panel in panels], gamma)
    
    tangential_velocities = np.dot(A, strengths) + b
    
    for i, panel in enumerate(panels):
        panel.vt = tangential_velocities[i]



def compute_pressure_coefficient(panels, freestream):
    """
    Yüzey basıncı katsayılarının hesaplanması.
    
    Parametreler
    ----------
    panels: Panel nesneleri listesi
    
    freestream: Serbest akım şartları
    """
    for panel in panels:
        panel.cp = 1.0 - (panel.vt / freestream.u_inf)**2
        

#data dosyasından airfoil geometrisinin yüklenmesi

def calculate(u_inf, alpha, N,secilen):
    naca_filepath = os.path.join('naca_profilleri', secilen+".dat.txt")
    with open(naca_filepath, 'r') as infile:
        x, y = np.loadtxt(infile, dtype=float, unpack=True)
        
    #Airfoil geometrisinin çizimi
        """
    width = 10
    pyplot.figure(figsize=(width, width))
    pyplot.grid()
    pyplot.xlabel('x', fontsize=16)
    pyplot.ylabel('y', fontsize=16)
    pyplot.plot(x, y, color='k', linestyle='-', linewidth=2)
    pyplot.axis('scaled', adjustable='box')
    pyplot.xlim(-0.1, 1.1)
    pyplot.ylim(-0.1, 0.2)"""


    # Geometriyi panellerine ayrıklaştırma
    panels = define_panels(x, y, N=N)

    # plot discretized geometry
    width = 10
    pyplot.figure(figsize=(width, width))
    pyplot.grid()
    pyplot.xlabel('x', fontsize=16)
    pyplot.ylabel('y', fontsize=16)
    pyplot.plot(x, y, color='k', linestyle='-', linewidth=2)
    pyplot.plot(np.append([panel.xa for panel in panels], panels[0].xa),
                np.append([panel.ya for panel in panels], panels[0].ya),
                linestyle='-', linewidth=1, marker='o',
                markersize=6, color='#CD2305')
    pyplot.axis('scaled', adjustable='box')
    pyplot.xlim(-0.1, 1.1)
    pyplot.ylim(-0.1, 0.2)


    # # Serbest akım çizgisi tanımlama
    freestream = Freestream(u_inf=u_inf, alpha=alpha)
    A_source = source_contribution_normal(panels)
    B_vortex = vortex_contribution_normal(panels)
    A = build_singularity_matrix(A_source, B_vortex)
    b = build_freestream_rhs(panels, freestream)

    # Tekillik şiddeti için çözüm
    strengths = linalg.solve (A, b)

    # Her panel için kaynak şiddetinin kaydedilmesi
    for i , panel in enumerate(panels):
        panel.sigma = strengths[i]
        
       
    # Sirkülasyon yoğunluğunun kaydedilmesi
    gamma = strengths[-1]

    # Her bir panel merkezi için teğetsel hızın hesaplaması
    compute_tangential_velocity(panels, freestream, gamma, A_source, B_vortex)
    # Yüzey basıncı katsayısı
    compute_pressure_coefficient(panels, freestream)

    # Yüzey basıncı katsayılarının çizimi
    pyplot.figure(figsize=(10, 6))
    pyplot.grid()
    pyplot.xlabel('$x$', fontsize=16)
    pyplot.ylabel('$C_p$', fontsize=16)
    pyplot.plot([panel.xc for panel in panels if panel.loc == 'upper'],
                [panel.cp for panel in panels if panel.loc == 'upper'],
                label='Üst Yüzey',
                color='r', linestyle='-', linewidth=2, marker='o', markersize=6)
    pyplot.plot([panel.xc for panel in panels if panel.loc == 'lower'],
                [panel.cp for panel in panels if panel.loc == 'lower'],
                label= 'Alt Yüzey',
                color='b', linestyle='-', linewidth=1, marker='o', markersize=6)
    pyplot.legend(loc='best', prop={'size':16})
    pyplot.xlim(-0.1, 1.1)
    pyplot.ylim(1.0, -2.0)
    pyplot.title('Panel Sayısı: {}'.format(panels.size), fontsize=16)

    accuracy = sum([panel.sigma * panel.length for panel in panels])
    print('Tekillik şiddetlerinin toplamı:: {:0.6f}'.format(accuracy))


    # Veterin (c) ve taşıma katsayısının (cl) hesaplanması
    c = abs(max(panel.xa for panel in panels) -
            min(panel.xa for panel in panels))
    cl = (gamma * sum(panel.length for panel in panels) /
        (0.5 * freestream.u_inf * c))
    print('Taşıma katsayısı: CL = {:0.3f}'.format(cl))
    return accuracy, cl