import numpy as np
from matplotlib import pyplot as plt
from sympy import symbols, solve, Eq, sin, cos


class MisilEnemigo:
    def __init__(self, v0, anguloDisparo):
        self.v0 = v0
        self.angulo = np.radians(anguloDisparo)
        self.g = 9.8

        self.hMax = 0
        self.dMax = 0
        self.tiempoVuelo = 0

    def localizarMisilEnemigo(self):
        y0 = 0
        x0 = 0

        self.hMax = y0 + (self.v0**2 * (np.sin(self.angulo)**2)) * 0.5 / 9.8  
        self.dMax = (self.v0**2 * np.sin(2 * self.angulo)) / self.g 
        self.tiempoVuelo = 2 * (self.v0 * np.sin(self.angulo)) / self.g  
        print('la distancia macima es de: ', self.dMax)
        print('la altura maxima es de: ', self.hMax)
        print('el tiempo de vuelo es de: ', self.tiempoVuelo)

        return self.hMax, self.dMax, self.tiempoVuelo

    def obtenerCoordenadas(self, t):
        x = self.v0 * np.cos(self.angulo) * t
        y = self.v0 * np.sin(self.angulo) * t - 0.5 * self.g * t**2
        return x, y

    def interceptarEnemigo(self, hIntercepcion):
        if hIntercepcion > self.hMax:
            print('No se puede interceptar el misil enemigo')
            return False
        else:
            t = symbols('t')
            EcuacionAltura = Eq(self.v0 * sin(self.angulo) * t - 0.5 * self.g * t**2, hIntercepcion)
            tiempos = solve(EcuacionAltura, t)

            tiemposValidos = [float(sol.evalf()) for sol in tiempos if sol.is_real and 0 <= sol.evalf() <= self.tiempoVuelo]

            if len(tiemposValidos) == 0:
                print('No hay soluciones reales para la intercepción')
                return None

            return tiemposValidos


class MisilInterceptador:
    def __init__(self, Xintercepcion, hIntercepcion, tiempoIntercepcion, posicion_inicial):
        self.Xintercepcion = Xintercepcion
        self.hIntercepcion = hIntercepcion
        self.v0 = 0
        self.angulo = 0
        self.g = 9.8

        self.tiempoIntercepcion = tiempoIntercepcion
        self.posicion_inicial = posicion_inicial  # Nueva variable para la posición inicial

    def calcularParametros(self):
        t = self.tiempoIntercepcion

        # Ecuaciones para resolver el ángulo y velocidad inicial
        v0, angulo = symbols('v0 angulo')

        # Ecuación de altura
        EcuacionAltura = Eq(v0 * sin(angulo) * t - 0.5 * self.g * t**2, self.hIntercepcion)

        # Ecuación de distancia horizontal
        EcuacionDistancia = Eq(v0 * cos(angulo) * t, self.Xintercepcion - self.posicion_inicial)

        # Resolver el sistema de ecuaciones
        soluciones = solve((EcuacionAltura, EcuacionDistancia), (v0, angulo))

        # Filtrar soluciones reales
        for sol in soluciones:
            self.v0 = sol[0]
            self.angulo = sol[1]
            if self.v0.is_real and self.v0 > 0 and self.angulo.is_real:
                self.v0 = float(self.v0)
                self.angulo = float(self.angulo.evalf())
                print(f"Velocidad inicial necesaria: {self.v0:.2f} m/s")
                print(f"Ángulo de disparo necesario: {np.degrees(self.angulo):.2f}°")
                return self.v0, self.angulo

        print("No se encontraron soluciones reales para el ángulo y la velocidad inicial.")
        return None, None

    def obtenerCoordenadas(self, t):
        # Ajustar las coordenadas para considerar la posición inicial
        x = self.posicion_inicial + self.v0 * np.cos(self.angulo) * t
        y = self.v0 * np.sin(self.angulo) * t - 0.5 * self.g * t**2
        return x, y

    def graficarTrayectorias(self, misil_enemigo):
        # Gráficos
        t_total = np.linspace(0, misil_enemigo.tiempoVuelo, num=500)
        x_misil_enemigo = [misil_enemigo.obtenerCoordenadas(t)[0] for t in t_total]
        y_misil_enemigo = [misil_enemigo.obtenerCoordenadas(t)[1] for t in t_total]

        # Obtener coordenadas del misil interceptador
        t_interceptador = np.linspace(0, self.tiempoIntercepcion, num=500)
        x_interceptador = [self.posicion_inicial + self.v0 * np.cos(self.angulo) * t for t in t_interceptador]
        y_interceptador = [self.v0 * np.sin(self.angulo) * t - 0.5 * self.g * t**2 for t in t_interceptador]

        # Graficar
        plt.figure(figsize=(12, 6))
        plt.plot(x_misil_enemigo, y_misil_enemigo, label='Misil Enemigo', color='black')
        plt.plot(x_interceptador, y_interceptador, label='Misil Interceptador', color='blue', linestyle='--')

        # Marcar intercepción
        x_enemigo, y_enemigo = misil_enemigo.obtenerCoordenadas(self.tiempoIntercepcion)
        plt.scatter([x_enemigo], [y_enemigo], color='red', label='Intercepción', zorder=5, s=100)

        # Personalizar gráfico
        plt.title('Trayectoria de los Misiles')
        plt.xlabel('Distancia (m)')
        plt.ylabel('Altura (m)')
        plt.grid()
        plt.legend()
        plt.xlim(0, max(misil_enemigo.dMax, self.Xintercepcion + self.posicion_inicial) * 1.1)
        plt.ylim(0, max(misil_enemigo.hMax, self.hIntercepcion) * 1.1)
        plt.show()


# Configurar el misil enemigo
misil_enemigo = MisilEnemigo(4000, 45)
misil_enemigo.localizarMisilEnemigo()

# Altura de intercepción
hIntercepcion = 100000  

# Calcular el tiempo de intercepción
tiemposValidos = misil_enemigo.interceptarEnemigo(hIntercepcion)

if tiemposValidos:
    tiempoSeleccionado = tiemposValidos[0]  # Tiempo seleccionado para la intercepción

    # Distancia de intercepción calculada
    x_intercepcion, _ = misil_enemigo.obtenerCoordenadas(tiempoSeleccionado)

    # Configurar el misil interceptador con una posición inicial de 10,000 metros
    posicion_inicial_interceptador = 10000  # El interceptador empieza a 10,000 metros

    misil_interceptor = MisilInterceptador(x_intercepcion, hIntercepcion, tiempoSeleccionado, posicion_inicial_interceptador)
    misil_interceptor.calcularParametros()
    misil_interceptor.graficarTrayectorias(misil_enemigo)

