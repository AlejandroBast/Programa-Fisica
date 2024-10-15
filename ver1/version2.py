import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Frame, Label, Entry, Button, PhotoImage, StringVar
from math import sin, cos, radians, pi

# Configuración de la ventana principal
window = Tk()
window.title('STMP - Cálculo de Lanzamiento')
window.geometry("600x500")  # Tamaño de la ventana
window.configure(bg='lightblue')
window.resizable(False, False)  # Color de fondo

# Configuración del frame
frameUno = Frame(window, width=600, height=250, bg='lightblue')
frameUno.pack(pady=20)

# Imagen (opcional, cambia la ruta a la correcta)
#imagen = PhotoImage(file='gato.png')
#imagenLugar = Label(frameUno, image=imagen)
#imagenLugar.place(x=150, y=10)

# Entrada de datos
cuadroVelocidad = Entry(frameUno, font=('Arial', 14), width=10)
cuadroVelocidad.grid(row=0, column=1, padx=20, pady=10)
cuadroAngulo = Entry(frameUno, font=('Arial', 14), width=10)
cuadroAngulo.grid(row=1, column=1, padx=20, pady=10)

# Etiquetas
VelocidadLabel = Label(frameUno, text='Velocidad Inicial (m/s): ', bg='lightblue', font=('Arial', 12))
VelocidadLabel.grid(row=0, column=0, pady=10)
AnguloLabel = Label(frameUno, text='Ángulo (°): ', bg='lightblue', font=('Arial', 12))
AnguloLabel.grid(row=1, column=0, pady=10)

# Variables para mostrar los resultados
alturaVar = StringVar()
distanciaVar = StringVar()
tiempoVar = StringVar()

# Etiquetas para mostrar los resultados
resultadoAltura = Label(frameUno, textvariable=alturaVar, bg='lightblue', font=('Arial', 12, 'bold'), fg='green')
resultadoAltura.grid(row=2, column=0, columnspan=2, pady=10)
resultadoDistancia = Label(frameUno, textvariable=distanciaVar, bg='lightblue', font=('Arial', 12, 'bold'), fg='green')
resultadoDistancia.grid(row=3, column=0, columnspan=2, pady=10)
resultadoTiempo = Label(frameUno, textvariable=tiempoVar, bg='lightblue', font=('Arial', 12, 'bold'), fg='green')
resultadoTiempo.grid(row=4, column=0, columnspan=2, pady=10)

# Función de cálculo
def calcular():
    try:
        # Obtener y convertir valores de entrada
        vo = float(cuadroVelocidad.get())  # Obtener velocidad inicial
        ang = float(cuadroAngulo.get())    # Obtener ángulo
        g = 9.81
        x0 = 0
        y0 = 0

        # Verificar que los valores sean no negativos
        if vo < 0 or ang < 0:
            raise ValueError("Los valores no pueden ser negativos.")

        # Transformar ángulo a radianes
        angRad = radians(ang)

        # Calcular altura máxima
        hmax = y0 + (vo**2 * (sin(angRad)**2)) / (2 * g)

        # Calcular distancia máxima
        dmax = (vo**2 * sin(2 * angRad)) / g

        # Calcular tiempo de vuelo
        tv = (2 * vo * sin(angRad)) / g

        # Mostrar los resultados en las etiquetas
        alturaVar.set(f"Altura máxima: {round(hmax, 2)} m")
        distanciaVar.set(f"Distancia máxima: {round(dmax, 2)} m")
        tiempoVar.set(f"Tiempo de vuelo: {round(tv, 2)} s")

        # Calcular la trayectoria (x, y)
        t = np.linspace(0, tv, 100)
        x = x0 + vo * cos(angRad) * t
        y = y0 + vo * sin(angRad) * t - 0.5 * g * t**2

        # Graficar la trayectoria
        plt.figure()
        plt.plot(x, y)
        plt.xlabel('Distancia (m)')
        plt.ylabel('Altura (m)')
        plt.title('Trayectoria del proyectil')
        plt.grid(True)
        plt.show()

    except ValueError as e:
        # En caso de error, mostrar un mensaje en rojo
        alturaVar.set(f"Error: {e}")
        distanciaVar.set("")
        tiempoVar.set("")

# Botón de cálculo
boton = Button(frameUno, text='Calcular', command=calcular, bg='blue', fg='white', font=('Arial', 14))
boton.grid(row=5, column=0, columnspan=2, pady=20)

# Ejecutar la ventana
window.mainloop()
