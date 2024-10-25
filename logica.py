import numpy  as np
from matplotlib import pyplot as plt
from sympy import  symbols, Eq, solve, Eq, sin, cos

class MisilEnemigo:

    def __init__(self, v0, angulo):
        self.v0 = v0
        self.angulo = np.radians(angulo)
        self.g  = 9.8
        self.hMax = 0
        self.dMax = 0
        self.tiempoVuelo = 0
        

    def calcularParametrosEnemigos(self):
        y0 = 0
        x0 = 0

        self.hMax = y0 + (self.v0**2 * (np.sin(self.angulo)**2)) / (2 * self.g)
        self.dMax = (self.v0**2 * sin(2 * self.angulo)) / self.g
        self.tiempoVuelo = (2 * self.v0 * sin(self.angulo)) / self.g

        print('la distancia macima es de: ', self.dMax)
        print('la altura maxima es de: ', self.hMax)
        print('el tiempo de vuelo es de: ', self.tiempoVuelo)

        return self.hMax, self.dMax, self.tiempoVuelo
    
    def calcularCordenadas(self, t):
        x = self.v0 * np.cos(self.angulo) * t
        y = self.v0 * np.sin(self.angulo) * t - 0.5 * self.g * t**2
        print('Coordenadas al tiempo:', t, 's X:', x,  'Y:', y)
        return x, y

testeo = MisilEnemigo(4000, 45)
testeo.calcularParametrosEnemigos()
testeo.calcularCordenadas(200)