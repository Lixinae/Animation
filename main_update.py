# -*- coding: utf-8 -*-
from math import *
from geom import *
from tkGraphPad import *


# ____________________classe Point Fixe____________________#
class PointFixe:
    """initialisatuion d'un point fixe : position, rayon, couleur"""

    def __init__(self, pos, ray, col):
        # paramètres physiques
        self.pos = pos
        self.vit = Vecteur(0, 0)
        self.frc = Vecteur(0, 0)
        # paramètres d'affichage
        self.col = col  # couleur
        self.ray = ray  # rayon

    # --------------------------------
    # méthodes de dessin
    def draw(self):
        fillcircle(self.pos, self.ray, self.col)

    # --------------------------------
    # moteur : rien
    def setup(self):
        pass

    # -------------------------------- (A|B) (vecteur AB)
    def __or__(self, M):
        return Vecteur(self.pos, M.pos)


# ____________________classe Particule____________________#
class Particule(PointFixe):
    """initialisation d'une particule : position, masse, pas, rayon, couleur"""

    def __init__(self, pos, m, pas, ray, col):
        # paramètres physiques
        self.m = m
        self.pas = pas
        # hérite du PointFixe
        PointFixe.__init__(self, pos, ray, col)

    def setup(self):
        self.vit += self.pas / self.m * self.frc
        self.pos += self.pas * self.vit
        self.frc = Vecteur(0, 0)


# --------------------------------
# moteur : LEAPFROG
#    def Leapfrog(self) :
#      self.vit = self.vit + h*(-G-(z/self.m)*self.vit)
#      self.pos = self.pos + h*self.vit
#
#    def EulerExp(self) :
#      self.pos = self.pos + h*self.vit
#      self.vit = self.vit + h*(-G-(z/self.m)*self.vit)
#
#    def EulerImp(self) :
#      self.vit = (self.m/(self.m+h*z))*(self.vit-h*G)
#      self.pos = self.pos + h*self.vit


# ____________________classe Liaison____________________#

class Liaison:

    def __init__(self, M1, M2, col):
        self.M1 = M1
        self.M2 = M2
        self.frc = Vecteur(0., 0.)
        self.col = col

    def setup(self):
        if self.M1:
            self.M1.frc += self.frc
        if self.M2:
            self.M2.frc -= self.frc

    def draw(self):
        if self.M1 and self.M2:
            if self.col == None:
                return
            line(self.M1.pos, self.M2.pos, self.col, 1)


# ____________________classe Gravite -> Liaison____________________#
class Gravite(Liaison):
    def __init__(self, M, vecGrav):
        Liaison.__init__(self, M, None, None)
        self.frc = vecGrav

    def setup(self):
        self.M1.frc += self.frc


# ____________________classe Ressort -> Liaison____________________#
class Ressort(Liaison):
    def __init__(self, M1, M2, k):
        Liaison.__init__(self, M1, M2, "blue")
        self.k = k
        self.l0 = distance(M1.pos, M2.pos)

    def setup(self):
        EPSILON = 0.000000001
        d = max(EPSILON, distance(self.M1.pos, self.M2.pos))  #
        e = (1. - self.l0 / d)  # elongation
        # force de rappel
        self.frc = self.k * e * Vecteur(self.M1.pos, self.M2.pos)
        Liaison.setup(self);


#############################      
m = 1
h = 0.01
k = 100


# ____________________FONCTIONS       ____________________#

# ==========================
# Modeleur : Construction -- "statique"
def Modeleur():
    """ Modeleur """
    points = []
    liaisons = []
    ray = 0.15
    haut = 3
    pointStart = PointFixe(Point(1, haut), ray, "red")
    pointEnd = PointFixe(Point(9, haut), ray, "red")

    for j in range(1, 4):
        ligne = []
        for i in range(2, 9):
            point = Particule(Point(i, j), 1, h, ray, "red")
            ligne.append(point)
        points.append(ligne)

    for j in range(1, 4):
        ressort = Ressort(points[j][0], points[j][1], k)
        liaisons.append(ressort)
        ressort = Ressort(points[j][len(points[0])], points[j][1], k)
        liaisons.append(ressort)
        for i in range(3, 8):
            ressort = Ressort(points[j][i], points[j][i+1], k)
            liaisons.append(ressort)

    point1 = Particule(Point(2, haut), 1, h, ray, "red")
    point2 = Particule(Point(3, haut), 1, h, ray, "red")
    point3 = Particule(Point(4, haut), 1, h, ray, "red")
    point4 = Particule(Point(5, haut), 1, h, ray, "red")
    point5 = Particule(Point(6, haut), 1, h, ray, "red")
    point6 = Particule(Point(7, haut), 1, h, ray, "red")
    point7 = Particule(Point(8, haut), 1, h, ray, "red")

    haut = 2
    pointStart2 = PointFixe(Point(1, haut), ray, "red")
    pointEnd2 = PointFixe(Point(9, haut), ray, "red")
    point12 = Particule(Point(2, haut), 1, h, ray, "red")
    point22 = Particule(Point(3, haut), 1, h, ray, "red")
    point32 = Particule(Point(4, haut), 1, h, ray, "red")
    point42 = Particule(Point(5, haut), 1, h, ray, "red")
    point52 = Particule(Point(6, haut), 1, h, ray, "red")
    point62 = Particule(Point(7, haut), 1, h, ray, "red")
    point72 = Particule(Point(8, haut), 1, h, ray, "red")

    # G = 0
    # grav = Gravite(point1, Vecteur(0, -G))
    # grav1 = Gravite(point2, Vecteur(0, -G))
    # grav2 = Gravite(point3, Vecteur(0, -G))
    # grav3 = Gravite(point4, Vecteur(0, -G))
    # grav4 = Gravite(point5, Vecteur(0, -G))

    ressort = Ressort(pointStart, point1, k)
    ressort1 = Ressort(point1, point2, k)
    ressort2 = Ressort(point2, point3, k)
    ressort3 = Ressort(point3, point4, k)
    ressort4 = Ressort(point4, point5, k)
    ressort5 = Ressort(point5, pointEnd, k)

    points.append(pointStart)
    points.append(point1)
    points.append(point2)
    points.append(point3)
    points.append(point4)
    points.append(point5)
    points.append(pointEnd)

    # liaisons.append(grav)
    # liaisons.append(grav1)
    # liaisons.append(grav2)
    # liaisons.append(grav3)
    # liaisons.append(grav4)

    liaisons.append(ressort)
    liaisons.append(ressort1)
    liaisons.append(ressort2)
    liaisons.append(ressort3)
    liaisons.append(ressort4)
    liaisons.append(ressort5)

    # return balle,balle2,grav,ressort
    return points, liaisons


# ==========================
# fonction animatrice
def anim():
    """fonction animatrice"""
    for p in points:
        p.setup()
    for l in liaisons:
        l.setup()
    points[1].pos.y += 0.01


# balle.setup()
# balle2.setup()
# grav.setup()
# ressort.setup()

# def analytic(P0, V0):
#     dt = dtscale.get()
#     w = m / z
#     t = 0
#     P = P0
#     while (P.y >= 0):
#         e = exp(-t / w)
#         P = Point(P0.x + w * (V0.x) * (1. - e),
#                   P0.y + w * (-g * w + V0.y) * (1. - e) + g * w * t)
#         V = Vecteur(V0.x * e,
#                     (-g * w + V0.y) * e + g * w)
#         circle(P, .02, "black", 1)
#         t += dt


# ==========================
# fonction de dessin
def draw():
    """fonction de dessin"""
    win.clear()  # nettoyage
    # dt=dtscale.get()
    # z= zscale.get()
    # analytic(Point(0,.5),Vecteur(5,9))

    # balle.draw()
    # balle2.draw()
    # ressort.draw()

    for p in points:
        p.draw()
    for l in liaisons:
        l.draw()


# ____________________PRINCIPAL       ____________________#
if __name__ == '__main__':
    # ==========================

    # Démarrage du réceptionnaire d'evenements :
    win = MainWindow("Corde 1D", 900, 450, "lightgrey")
    win.SetDrawZone(-0.1, -0.1, +10.1, +5.1)

    points, liaisons = Modeleur()

    # scrollbars
    # dtscale=win.CreateScalev(label='dt',inf=0.01,sup=0.1,step=0.002)
    # dtscale.set(dt)
    # zscale=win.CreateScalev(label='z',inf=0.01,sup=0.2,step=0.002)
    # zscale.set(z)
    # hscale=win.CreateScalev(label='h',inf=0.01,sup=0.1,step=0.001)
    # hscale.set(h)

    win.anim = anim
    win.draw = draw
    win.startmainloop()
