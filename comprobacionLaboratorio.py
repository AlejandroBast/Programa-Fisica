import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, messagebox
from tkinter import ttk

# Función para validar la entrada de velocidad y ángulo
def validar_entrada(v0, angulo, interceptor=False):
    if v0 <= 0:
        raise ValueError("La velocidad inicial debe ser mayor que cero.")
    if not interceptor and (angulo < 0 or angulo > 90):
        raise ValueError("El ángulo debe estar entre 0 y 90 grados para el misil enemigo.")
    if interceptor and angulo < 0:
        raise ValueError("El ángulo del interceptor no puede ser negativo.")

# Función para calcular la trayectoria usando movimiento parabólico
def trayectoria_misil(v0, angulo, x_inicial=0, y_inicial=0, g=9.81, dt=0.01):
    angulo_rad = np.radians(angulo)  # Convertir el ángulo a radianes
    t_vuelo = (2 * v0 * np.sin(angulo_rad)) / g  # Calcular el tiempo total de vuelo
    t = np.linspace(0, t_vuelo, num=500)  # Crear un array de tiempo

    # Ecuaciones de movimiento parabólico
    x = x_inicial + v0 * np.cos(angulo_rad) * t
    y = y_inicial + v0 * np.sin(angulo_rad) * t - 0.5 * g * t**2

    return x, y, t

# Función para encontrar el punto de intersección
def encontrar_interseccion(x1, y1, x2, y2):
    for i in range(len(x1)):
        if np.isclose(x1[i], x2[i], atol=1) and np.isclose(y1[i], y2[i], atol=1):
            return x1[i], y1[i]
    return None, None

# Función para obtener parámetros según la combinación seleccionada
def obtener_parametros_seleccion():
    seleccion = combo_parametros.get()
    if seleccion == "Velocidad baja y ángulo bajo":
        return 30, 20, 25, 100  # Ejemplo de valores (ángulo interceptor > 90)
    elif seleccion == "Velocidad baja y ángulo alto":
        return 30, 60, 25, 110
    elif seleccion == "Velocidad alta y ángulo bajo":
        return 80, 20, 75, 100
    elif seleccion == "Velocidad alta y ángulo alto":
        return 80, 60, 75, 120
    return None

# Función para graficar las trayectorias
def graficar_trayectorias():
    try:
        parametros = obtener_parametros_seleccion()
        if parametros:
            v0_1, angulo_1, v0_2, angulo_2 = parametros
            x_inicial_interceptor = 0
        else:
            # Obtener valores manualmente desde la interfaz gráfica
            v0_1 = float(entry_v0_1.get())
            angulo_1 = float(entry_angulo_1.get())
            v0_2 = float(entry_v0_2.get())
            angulo_2 = float(entry_angulo_2.get())
            x_inicial_interceptor = float(entry_x_inicial.get())

        # Validar los valores de entrada (el ángulo del interceptor puede ser mayor a 90)
        validar_entrada(v0_1, angulo_1)
        validar_entrada(v0_2, angulo_2, interceptor=True)

        # Calcular trayectorias
        x1, y1, t1 = trayectoria_misil(v0_1, angulo_1, x_inicial=0, y_inicial=0)
        x2, y2, t2 = trayectoria_misil(v0_2, angulo_2, x_inicial=x_inicial_interceptor, y_inicial=0)

        # Encontrar el punto de intersección
        x_inter, y_inter = encontrar_interseccion(x1, y1, x2, y2)
        
        # Graficar
        plt.figure(figsize=(10, 5))
        plt.plot(x1, y1, label="Misil Enemigo", color='black')
        plt.plot(x2, y2, label="Misil Interceptor", color='blue')

        # Si se encuentra un punto de intersección, se marca
        if x_inter is not None and y_inter is not None:
            plt.scatter(x_inter, y_inter, color='red', label='Intercepción')
            messagebox.showinfo("Éxito", f"¡Intercepción exitosa en (x: {x_inter:.2f}, y: {y_inter:.2f})!")
        else:
            messagebox.showwarning("Fallo", "No se encontró un punto de intersección entre los misiles.")

        plt.title("Trayectoria del Proyectil")
        plt.xlabel("Distancia (m)")
        plt.ylabel("Altura (m)")
        plt.legend()
        plt.grid(True)
        plt.show()

    except ValueError:
        messagebox.showerror("Error de entrada", "Por favor, ingrese valores numéricos válidos para los ángulos y velocidades.")

# Crear la interfaz gráfica con tkinter
ventana = Tk()
ventana.title("Simulación de Misiles")

# Etiquetas y entradas para el Misil Enemigo
Label(ventana, text="Misil Enemigo - Velocidad inicial (m/s):").grid(row=0, column=0)
entry_v0_1 = Entry(ventana)
entry_v0_1.grid(row=0, column=1)

Label(ventana, text="Misil Enemigo - Ángulo (grados):").grid(row=1, column=0)
entry_angulo_1 = Entry(ventana)
entry_angulo_1.grid(row=1, column=1)

# Etiquetas y entradas para el Misil Interceptor
Label(ventana, text="Misil Interceptor - Velocidad inicial (m/s):").grid(row=2, column=0)
entry_v0_2 = Entry(ventana)
entry_v0_2.grid(row=2, column=1)

Label(ventana, text="Misil Interceptor - Ángulo (grados):").grid(row=3, column=0)
entry_angulo_2 = Entry(ventana)
entry_angulo_2.grid(row=3, column=1)

# Entrada para la posición inicial del interceptor
Label(ventana, text="Misil Interceptor - Posición inicial (m):").grid(row=4, column=0)
entry_x_inicial = Entry(ventana)
entry_x_inicial.grid(row=4, column=1)

# Combobox para seleccionar combinación de parámetros
Label(ventana, text="Seleccionar combinación de parámetros:").grid(row=5, column=0)
combo_parametros = ttk.Combobox(ventana, values=[
    "Velocidad baja y ángulo bajo",
    "Velocidad baja y ángulo alto",
    "Velocidad alta y ángulo bajo",
    "Velocidad alta y ángulo alto"
])
combo_parametros.grid(row=5, column=1)

# Botón para graficar
btn_graficar = Button(ventana, text="Graficar Trayectorias", command=graficar_trayectorias)
btn_graficar.grid(row=6, column=0, columnspan=2)

# Iniciar la interfaz gráfica
ventana.mainloop()
