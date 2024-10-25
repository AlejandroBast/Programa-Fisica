import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sympy import symbols, solve, Eq, sin, cos
import matplotlib.pyplot as plt
from tkinter import ttk, messagebox

class MisilEnemigo:
    def __init__(self, v0, anguloDisparo):
        self.v0 = v0
        self.angulo = np.radians(anguloDisparo) 
        self.g = 9.8
        self.dMax = None
        self.hMax = None
        self.tiempoVuelo = None

        self.hIntercepcion = None
        self.tiemposDeIntercepcion = []
        self.tiempoSeleccionado = None

        self.x = None
        self.y = None

    def getTiempo(self):
        return self.tiempoSeleccionado
    
    def getCordenadaX(self):
        return self.x
    
    def getCordenadaY(self):
        return self.y
    
    def getV0(self):
        return self.v0
    
    def getAngulo(self):
        return self.angulo

    def getHintercepcion(self):
        return self.hIntercepcion

    def calcularParametrosEnemigo(self):
        self.hMax = (self.v0**2 * (np.sin(self.angulo)**2)) / (2 * self.g) 
        self.dMax = (self.v0**2 * np.sin(2 * self.angulo)) / self.g  
        self.tiempoVuelo = 2 * (self.v0 * np.sin(self.angulo)) / self.g 

        print(f''' 
                Parametros Misil Enemigo:
            Hmax: {self.hMax},
            Dmax: {self.dMax},  
            Tiempo de Vuelo: {self.tiempoVuelo}
              ''')
    
    def calcularTiempos(self, hIntercepcion):
        self.hIntercepcion = hIntercepcion

        if hIntercepcion > self.hMax:
            print('No se puede interceptar el misil enemigo.')
            return False
        else:
            t = symbols('t')
            EcuacionAltura = Eq(self.v0 * sin(self.angulo) * t - 0.5 * self.g * t**2, hIntercepcion)
            tiempos = solve(EcuacionAltura, t)

            self.tiemposDeIntercepcion = [float(sol.evalf()) for sol in tiempos if sol.is_real and 0 <= sol.evalf() <= self.tiempoVuelo]

            if len(self.tiemposDeIntercepcion) == 0:
                print('No hay soluciones reales para la intercepción.')
                return None
            else:
                print(f'''
                Tiempos en los que lleva a la altura deseada:
            Tiempo de ascenso: {self.tiemposDeIntercepcion[0]},
            Tiempo de descenso: {self.tiemposDeIntercepcion[1]}
                    ''')
            return self.tiemposDeIntercepcion
    
    def seleccionarTiempo(self, opcion):
        if opcion == 1:
            self.tiempoSeleccionado = self.tiemposDeIntercepcion[0]
            return  self.tiempoSeleccionado

        elif opcion  == 2:
            self.tiempoSeleccionado  = self.tiemposDeIntercepcion[1]
            return self.tiempoSeleccionado
        else:
            print('Opción no válida, escoje una opcion 1 o 2')

    def obtenerCoordenadas(self):
        if self.tiempoSeleccionado:
            self.x = self.v0 * np.cos(self.angulo) * self.tiempoSeleccionado
            self.y = self.v0 * np.sin(self.angulo) * self.tiempoSeleccionado - 0.5 * self.g * self.tiempoSeleccionado**2
            print(f'''Coordenada X en el tiempo: {self.tiempoSeleccionado}s 
                  X = {self.x}''')
            if self.hIntercepcion == round(self.y):
                print('calculos de los gods uwu')
            else:
                print('no papu, ', 'Y:', y, 'y hIntercepcion:',  self.hIntercepcion, 'no son lo mismo')

        else:
            print('escoje un tiempo de intercepcion')
        return self.x
    def mostrarTrayectoria(self):
        times = np.linspace(0, self.tiempoVuelo, 100)
        x =  self.v0 * np.cos(self.angulo) * times
        y =  self.v0 * np.sin(self.angulo) * times - 0.5 * self.g * times**2


        plt.figure()
        plt.plot(x, y, label='Enemigo', color='red')
        plt.xlabel('Distancia(m)')
        plt.ylabel('Altura(m)')
        plt.title('Trayectoria del Misil Enemigo')
        plt.grid(True)

        plt.show()


class MisilInterceptador:
    def __init__(self, posicion_inicial, enemigo):

        self.X_intercepcion = 0
        self.Y_Intercepcion = 0

        self.tiempoIntercepcion = 0

        self.posicion_inicial = posicion_inicial
        self.v0 = 0
        self.angulo = 0

        self.g = 9.8
        self.enemigo = enemigo

    def calcularParametros(self):
        self.tiempoIntercepcion = self.enemigo.getTiempo()
        self.X_intercepcion  = self.enemigo.getCordenadaX()
        self.Y_Intercepcion = self.enemigo.getCordenadaY()
        t = self.tiempoIntercepcion
        v0, angulo = symbols('v0 angulo')

        EcuacionAltura = Eq(v0 * sin(angulo) * t - 0.5 * self.g * t**2, self.Y_Intercepcion)
        EcuacionDistancia = Eq(v0 * cos(angulo) * t, self.X_intercepcion - self.posicion_inicial)
        respuestas = solve((EcuacionAltura, EcuacionDistancia), (v0, angulo))

        for i in respuestas:
            if i[0].is_real and i[0] > 0 and i[1].is_real:
                self.v0 = float(i[0])
                self.angulo = float(i[1])
                print(f"Velocidad inicial necesaria: {self.v0:.2f} m/s")
                print(f"Ángulo de disparo necesario: {np.degrees(self.angulo):.2f}°")
                print(f"Tiempo de impacto: {self.tiempoIntercepcion:.2f}s")
                return self.v0, self.angulo
        print("No se encontraron soluciones reales para el ángulo y la velocidad inicial.")
        return None, None
    
    def verificarIntercepcion(self):
        x = self.posicion_inicial + self.v0 * np.cos(self.angulo) * self.tiempoIntercepcion
        y = self.v0 * np.sin(self.angulo) * self.tiempoIntercepcion - 0.5 * self.g * self.tiempoIntercepcion**2
        #if x == self.enemigo.getCordenadaX() and  y == self.enemigo.getCordenadaY():

        if np.isclose(x, self.enemigo.getCordenadaX(), atol=1e-1) and np.isclose(y, self.enemigo.getCordenadaY(), atol=1e-1):
            print(f'''Intercepcion Exitosa!!
        Enemigo                           interceptor
        X:{self.enemigo.getCordenadaX():.2f}  X:{x:.2f}
        Y:{self.enemigo.getCordenadaY():.2f}  Y:{y:.2f} 
                  ''')
        else:
            print(f'''Intercepcion Fallida!!
        Enemigo                             interceptor
        X:{self.enemigo.getCordenadaX():.2f}  X:{x:.2f}
        Y:{self.enemigo.getCordenadaY():.2f}  Y:{y:.2f} 
                  ''')

    def GraficarSimulacion(self):
        # interceptardore
        times = np.linspace(0, self.tiempoIntercepcion, 100)
        x = self.posicion_inicial + self.v0 * np.cos(self.angulo) * times
        y = self.v0 * np.sin(self.angulo) * times - 0.5 * self.g * times**2

        # enemigo
        enemy_times = np.linspace(0, self.tiempoIntercepcion, 100)
        xEnemy = self.enemigo.v0 * np.cos(self.enemigo.angulo) * enemy_times
        yEnemy = self.enemigo.v0 * np.sin(self.enemigo.angulo) * enemy_times - 0.5 * self.enemigo.g * enemy_times**2


        plt.figure()
        plt.plot(x, y, label='Misil Interceptor', color='blue')  
        plt.plot(xEnemy, yEnemy, label='Misil Enemigo', color='black')  

        # Marcar la intercepción
        plt.scatter(self.enemigo.getCordenadaX(), self.enemigo.getCordenadaY(), color='red', label='Intercepción')  # Color de la intercepción

        plt.xlabel('Distancia (m)')
        plt.ylabel('Altura (m)')
        plt.title('Trayectoria del Proyectil')
        plt.legend()
        plt.grid(True)
        plt.ylim(0, max(max(y.max(), yEnemy.max()), 0) * 1.1)  
        plt.xlim(0, max(max(x.max(), xEnemy.max()), 0) * 1.1) 
        plt.show()

    def aplicarFormulaDeT(self):
        # para el interceptor
        interceptor = (self.posicion_inicial - self.X_intercepcion) / self.v0
        # para el enemigo
        enemigo = (0 - self.enemigo.getHintercepcion()) /  self.enemigo.getV0()

        if interceptor ==  enemigo:
            print('alfin')
        elif np.isclose(interceptor,  enemigo, atol=1e-1):
            print('ahora si')
        elif interceptor == self.enemigo.getTiempo():
            print('si da')
        else:
            print('nah coma mrd')




# (Código de las clases MisilEnemigo y MisilInterceptador aquí, tal como lo tienes)

class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Intercepción de Misiles")

        self.frames = {}
        for F in (PantallaEnemigo, PantallaInterceptor):
            frame = F(self.root, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PantallaEnemigo)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class PantallaEnemigo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # Etiquetas y entradas para ángulo y velocidad inicial del enemigo
        tk.Label(self, text="Ángulo de disparo (grados):").grid(row=0, column=0)
        self.angulo_entry = tk.Entry(self)
        self.angulo_entry.grid(row=0, column=1)

        tk.Label(self, text="Velocidad inicial (m/s):").grid(row=1, column=0)
        self.velocidad_entry = tk.Entry(self)
        self.velocidad_entry.grid(row=1, column=1)

        # Botón para calcular parámetros y mostrar trayectoria
        btn_calcular = tk.Button(self, text="Calcular y mostrar trayectoria", command=self.calcular_y_mostrar_trayectoria)
        btn_calcular.grid(row=2, columnspan=2)

        # Botón para pasar a la siguiente pantalla
        btn_siguiente = tk.Button(self, text="Siguiente", command=lambda: controller.show_frame(PantallaInterceptor))
        btn_siguiente.grid(row=3, columnspan=2)

    def calcular_y_mostrar_trayectoria(self):
        try:
            angulo = float(self.angulo_entry.get())
            velocidad = float(self.velocidad_entry.get())

            # Creación del misil enemigo y cálculos
            self.enemigo = MisilEnemigo(velocidad, angulo)
            self.enemigo.calcularParametrosEnemigo()
            self.enemigo.mostrarTrayectoria()

            # Almacenar la instancia de MisilEnemigo en el controlador para usarla en la siguiente pantalla
            self.controller.frames[PantallaInterceptor].enemigo = self.enemigo

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")


class PantallaInterceptor(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # Etiquetas y entradas para posición inicial y altura de intercepción
        tk.Label(self, text="Posición inicial (m):").grid(row=0, column=0)
        self.posicion_entry = tk.Entry(self)
        self.posicion_entry.grid(row=0, column=1)

        tk.Label(self, text="Altura de intercepción (m):").grid(row=1, column=0)
        self.altura_entry = tk.Entry(self)
        self.altura_entry.grid(row=1, column=1)

        # Botón para calcular y mostrar la simulación
        btn_simular = tk.Button(self, text="Simular intercepción", command=self.simular_intercepcion)
        btn_simular.grid(row=2, columnspan=2)

    def simular_intercepcion(self):
        try:
            posicion = float(self.posicion_entry.get())
            altura = float(self.altura_entry.get())

            # Obtener el enemigo de la pantalla anterior
            enemigo = self.enemigo

            # Calcular los tiempos de intercepción
            if not enemigo.calcularTiempos(altura):
                return

            enemigo.seleccionarTiempo(1)  # Selecciona el tiempo de ascenso
            enemigo.obtenerCoordenadas()

            # Creación del misil interceptor y cálculos
            interceptor = MisilInterceptador(posicion, enemigo)
            interceptor.calcularParametros()
            interceptor.verificarIntercepcion()
            interceptor.GraficarSimulacion()

            # Mostrar resultados
            messagebox.showinfo("Intercepción Exitosa", f"Velocidad Inicial Necesaria: {interceptor.v0:.2f} m/s\n"
                                                        f"Ángulo de Disparo Necesario: {np.degrees(interceptor.angulo):.2f}°\n"
                                                        f"Tiempo de Impacto: {interceptor.tiempoIntercepcion:.2f}s")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
 






