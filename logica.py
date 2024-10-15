import numpy as np
from matplotlib import pyplot as plt
from sympy import symbols, solve, Eq, sin, cos


class MisilEnemigo:
    def  __init__(self, v0, anguloDisparo):
        self.v0 = v0
        self.angulo = np.radians(anguloDisparo)
        self.g  = 9.8

        self.hMax = 0
        self.dMax = 0
        self.tiempoVuelo  = 0


    def localizarMisilEnemigo(self):
        y0 = 0
        x0 = 0

        self.hMax = y0 + (self.v0**2 * (np.sin(self.angulo)**2))*0.5 / 9.8 # altura maxima
        self.dMax = (self.v0**2 * np.sin(2 * self.angulo)) / self.g # distancia maxima
        self.tiempoVuelo = 2*(self.v0 * np.sin(self.angulo)) / self.g # tiempo de vuelo

        print('Tiempo de vuelo misil enemigo',  round(self.tiempoVuelo, 2))
        print('distancia maxima: ', round(self.dMax, 2))
        print('Altura Maxima: ',  round(self.hMax, 2))
        print('this works!!!!')

        return  self.hMax, self.dMax, self.tiempoVuelo
    
    def obtenerCoordenadas(self, t):
        x = self.v0 * np.cos(self.angulo) * t
        y = self.v0 * np.sin(self.angulo) * t - 0.5 * self.g * t**2
        print('cordenadas:  ', x, y)

        return x, y

    def interceptarEnemigo(self, hIntercepcion):
        if hIntercepcion > self.hMax:
            print('No se puede interceptar el misil enemigo')
            return False
        else:
            t = symbols('t')
            EcuacionAltura = Eq(self.v0 * sin(self.angulo) * t - 0.5 * self.g * t**2, hIntercepcion)
            tiempos = solve(EcuacionAltura, t)

            tiemposValidos = [float(sol.evalf()) for sol in tiempos  if sol.is_real and 0 <= sol.evalf() <= self.tiempoVuelo]


            if len(tiemposValidos) == 0:
                print('No hay soluciones reales para la intercepción')
                return None

            # Manejo para subida y bajada
            tiempoIntercepcionSubida = round(tiemposValidos[0], 2)
            if len(tiemposValidos) > 1:
                tiempoIntercepcionBajada = round(tiemposValidos[1], 2)
                print(f'El misil llega a {hIntercepcion} m, de subida a los {tiempoIntercepcionSubida}s, y de bajada a los {tiempoIntercepcionBajada}s')
            else:
                print(f'El misil llega a {hIntercepcion} m a los {tiempoIntercepcionSubida} s')

            return tiemposValidos


class MisilInterceptador:
    def __init__(self, Xintercepcion, hIntercepcion, tiempoIntercepcion):
        self.Xintercepcion = Xintercepcion
        self.hIntercepcion = hIntercepcion
        self.v0 = 0
        self.angulo = 0
        self.g = 9.8

        self.tiempoIntercepcion = tiempoIntercepcion


    def calcularParametros(self):
        t = self.tiempoIntercepcion

        # Ecuaciones para resolver el ángulo y velocidad inicial
        v0, angulo = symbols('v0 angulo')

        # Ecuación de altura
        EcuacionAltura = Eq(v0 * sin(angulo) * t - 0.5 * self.g * t**2, self.hIntercepcion)

        # Ecuación de distancia horizontal
        EcuacionDistancia = Eq(v0 * cos(angulo) * t, self.Xintercepcion)

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
                print(f"Ángulo de disparo necesario: {self.angulo:.2f}°")
                return self.v0, self.angulo
    # Si no hay soluciones válidas
        print("No se encontraron soluciones reales para el ángulo y la velocidad inicial.")
        return None, None
    
    def obtenerCoordenadas(self):
        x = self.v0 * np.cos(self.angulo) * self.tiempoIntercepcion
        y = self.v0 * np.sin(self.angulo) * self.tiempoIntercepcion - 0.5 * self.g * self.tiempoIntercepcion**2
        return x, y

    def verificarIntercepcion(self, misil_enemigo):
        # Obtener la posición del interceptador en el tiempo de intercepción
        x_interceptador, y_interceptador = self.obtenerCoordenadas()

        # Obtener la posición del misil enemigo en el mismo tiempo
        x_enemigo, y_enemigo = misil_enemigo.obtenerCoordenadas(self.tiempoIntercepcion)

        # Comparar posiciones
        if np.isclose(x_interceptador, x_enemigo, atol=1e-2) and np.isclose(y_interceptador, y_enemigo, atol=1e-2):
            print("¡Intercepción exitosa!")
            plt.figure()\
            
        else:
            print(f"Falló la intercepción. Posiciones - Enemigo: ({x_enemigo}, {y_enemigo}), Interceptador: ({x_interceptador}, {y_interceptador})")
        
    def graficarTrayectorias(self, misil_enemigo):
        # Gráficos
        t_total = np.linspace(0, misil_enemigo.tiempoVuelo, num=500)
        x_misil_enemigo = [misil_enemigo.obtenerCoordenadas(t)[0] for t in t_total]
        y_misil_enemigo = [misil_enemigo.obtenerCoordenadas(t)[1] for t in t_total]

        # Obtener coordenadas del misil interceptador
        t_interceptador = np.linspace(0, self.tiempoIntercepcion, num=500)
        x_interceptador = [self.v0 * np.cos(self.angulo) * t for t in t_interceptador]
        y_interceptador = [self.v0 * np.sin(self.angulo) * t - 0.5 * self.g * t**2 for t in t_interceptador]

        # Graficar
        plt.figure(figsize=(12, 6))
        plt.plot(x_misil_enemigo, y_misil_enemigo, label='Misil Enemigo', color='red')
        plt.plot(x_interceptador, y_interceptador, label='Misil Interceptador', color='blue', linestyle='--')  # Línea discontinua para mayor visibilidad
        
        # Marcar intercepción
        x_enemigo, y_enemigo = misil_enemigo.obtenerCoordenadas(self.tiempoIntercepcion)
        plt.scatter([x_enemigo], [y_enemigo], color='green', label='Intercepción', zorder=5, s=100)  # Punto de intercepción en verde

        # Personalizar gráfico
        plt.title('Trayectoria de los Misiles')
        plt.xlabel('Distancia (m)')
        plt.ylabel('Altura (m)')
        plt.axhline(0, color='black', lw=0.5, ls='--')
        plt.axvline(0, color='black', lw=0.5, ls='--')
        plt.grid()
        plt.legend()
        plt.xlim(0, max(misil_enemigo.dMax, self.Xintercepcion) * 1.1)
        plt.ylim(0, max(misil_enemigo.hMax, self.hIntercepcion) * 1.1)
        plt.show()



misil_enemigo = MisilEnemigo(4000, 45)
misil_enemigo.localizarMisilEnemigo()

tiempoValido = misil_enemigo.interceptarEnemigo(204081.5)

if  tiempoValido:
    tiempoSeleccionado =  tiempoValido[0]
    misil_interceptor = MisilInterceptador(239096.31755411098, 204081.5, tiempoSeleccionado)
    misil_interceptor.calcularParametros()
    misil_interceptor.verificarIntercepcion(misil_enemigo)
    misil_interceptor.graficarTrayectorias(misil_enemigo)

