# Explicación del Proyecto de Simulación de Misiles

<p align="justify">
El proyecto que estás desarrollando está relacionado con la simulación de trayectorias de misiles, tanto de un misil enemigo como de un misil interceptador. Este tipo de simulaciones tienen aplicaciones en campos como la defensa militar, la física y la ingeniería, ya que permiten modelar el comportamiento de proyectiles y cómo diferentes parámetros afectan su trayectoria. A continuación, se describe detalladamente el funcionamiento de cada uno de los componentes incluidos en los archivos proporcionados.
</p>

## Archivo: `ventana.pyw`

<p align="justify">
Este archivo está diseñado para gestionar la interfaz gráfica del programa usando la librería <strong>Tkinter</strong> en Python. La interfaz permite al usuario ingresar los parámetros necesarios, como la velocidad inicial y el ángulo del misil. El código también incluye la opción de mostrar la trayectoria del misil en una gráfica, utilizando <strong>Matplotlib</strong>.

En este archivo, se encuentran los elementos básicos de la interfaz, como:
- Campos de entrada para la velocidad y el ángulo.
- Botones de interacción, como el de "Calcular", que ejecuta la función para calcular los parámetros de la trayectoria.
- Un cuadro de texto para mostrar los resultados como la altura máxima, la distancia recorrida y el tiempo de vuelo.
- Además, una gráfica de la trayectoria del misil se genera para proporcionar una visualización detallada del recorrido.

La interfaz está diseñada de manera sencilla pero funcional, permitiendo a los usuarios visualizar de forma clara los resultados de las simulaciones.
</p>

## Archivo: `logicaVersion2ConInterfazGrafica.py`

<p align="justify">
Este archivo es la columna vertebral del proyecto, ya que contiene la lógica central que permite realizar los cálculos necesarios para la simulación de las trayectorias de los misiles. Se implementan dos clases clave: <strong>MisilEnemigo</strong> y <strong>MisilInterceptador</strong>. Estas clases modelan las características físicas de ambos misiles, como la velocidad, el ángulo y las ecuaciones necesarias para calcular su posición a lo largo del tiempo.

<strong>1. MisilEnemigo</strong>:
   - Esta clase calcula parámetros como la altura máxima, la distancia máxima que recorrerá el misil enemigo, y el tiempo total de vuelo. 
   - También es capaz de calcular los tiempos en los que el misil alcanza una cierta altura de intercepción, lo que es fundamental para coordinar la intercepción.

<strong>2. MisilInterceptador</strong>:
   - La clase del misil interceptador calcula los parámetros necesarios para interceptar el misil enemigo. Se resuelven ecuaciones físicas para determinar la velocidad inicial y el ángulo que debe tener el misil interceptador para alcanzar el punto de intercepción deseado.
   - Además, verifica si la intercepción fue exitosa comparando las coordenadas del misil interceptador con las del misil enemigo.

Esta sección del código también se encarga de graficar las trayectorias de ambos misiles y de marcar visualmente el punto de intercepción, si es que ocurre.
</p>

## Archivo: `test.py`

<p align="justify">
Este archivo incluye una versión simplificada de las clases mencionadas anteriormente, además de ejecutar directamente una simulación de prueba. En este archivo, se realiza lo siguiente:
- Se configuran los parámetros iniciales del misil enemigo (como la velocidad y el ángulo).
- Se calcula la altura máxima, la distancia máxima y el tiempo de vuelo.
- Se determina si el misil interceptador es capaz de interceptar el misil enemigo, basado en la altura de intercepción especificada.

El archivo también incluye la funcionalidad de graficar las trayectorias de ambos misiles, utilizando <strong>Matplotlib</strong>, para visualizar la simulación y observar el momento en que el misil interceptador alcanza al enemigo.
</p>

## Conclusión

<p align="justify">
Este proyecto simula una situación de intercepción de misiles utilizando Python. La combinación de interfaces gráficas con <strong>Tkinter</strong> y el poder de cálculo de <strong>NumPy</strong> y <strong>SymPy</strong> permite una representación detallada tanto de los cálculos como de la visualización gráfica de las trayectorias. El enfoque modular del proyecto, con la separación de la lógica en clases como <strong>MisilEnemigo</strong> y <strong>MisilInterceptador</strong>, facilita su comprensión y ampliación, lo que es útil si se desea añadir más complejidad o nuevas funcionalidades al sistema.

La simulación gráfica es particularmente útil para entender visualmente cómo los diferentes parámetros influyen en las trayectorias, lo que puede ser aplicable tanto en simulaciones de defensa militar como en aplicaciones académicas.
</p>
