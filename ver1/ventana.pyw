from tkinter import *
from numpy import *
from  matplotlib import pyplot as plt

#ventana =  Tk()
#ventana.title("Simulacion de Trayectoria de Movimiento Parabolico (STMP)")
#ventana.geometry("612x384")
#ventana.resizable(False, False)
#ventana.config(bg="black")
#ventana.iconbitmap("icono.ico")

#screm = Frame()
#screm.pack(fill='both',  expand=True)
#screm.config(bg='blue')
#screm.config(width=612, height=384)
#screm.config(bd=15)
#screm.config(relief="sunken")
#screm.config(cursor="")

#ventana.mainloop()

window  = Tk()
window.title('STMP - Calculo de Lanzamiento')
window.iconbitmap("icono.ico")
frameUno =  Frame(window, width="1024", height= '720')
frameUno.pack()

#imagen = PhotoImage(file='gato.png')
#imagenLugar = Label(frameUno, image=imagen)
#imagenLugar.place(x='306', y='192')

# ingreso de data
cuadroVelocidad  = Entry(frameUno)
cuadroVelocidad.grid(row=0,  column=1)
cuadroAngulo = Entry(frameUno)
cuadroAngulo.grid(row=1,  column=1)
# text
VelocidadLabel = Label(frameUno, text='Velocidad Inicial (m/s): ')
VelocidadLabel.grid(row=0, column=0, pady=20)
AnguloLabel =  Label(frameUno, text='Angulo (g°): ')
AnguloLabel.grid(row=1, column=0, pady=20)

# cuadro de texto largo
cuadroTexto = Text(frameUno, width=25, height=5)
cuadroTexto.grid(row=2, column=0, columnspan=2, pady=20)
# barra scrolvertical
scrollVertical = Scrollbar(frameUno, command=cuadroTexto.yview)
scrollVertical.grid(row=2, column=2, sticky='nsew')
cuadroTexto.config(yscrollcommand=scrollVertical.set)
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

        # Mostrar los resultados en el cuadro de texto
        cuadroTexto.delete(1.0, "end")
        cuadroTexto.insert("end", f"Altura máxima: {round(hmax, 2)} m\n")
        cuadroTexto.insert("end", f"Distancia máxima: {round(dmax, 2)} m\n")
        cuadroTexto.insert("end", f"Tiempo de vuelo: {round(tv, 2)} s\n")



        # Calcular la trayectoria (x, y)
        t = linspace(0, tv, 100)
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
        cuadroTexto.delete(1.0, "end")
        cuadroTexto.insert("end", f"Error: {e}\nPor favor ingrese valores numéricos válidos.\n")

# Botón de cálculo
boton = Button(frameUno, text='Calcular', command=calcular)
boton.grid(row=3, column=0, columnspan=2, pady=20)




window.mainloop()
