# **Defensa Planetaria - Computación Paralela** 🌌

Un juego desarrollado en Python con Pygame que utiliza conceptos de **computación paralela** para gestionar múltiples elementos dinámicos, como meteoritos y balas, en tiempo real. El objetivo del juego es defender el planeta destruyendo meteoritos con una nave espacial.

## **Características principales**
- **Juego interactivo:** Usa las teclas del teclado para controlar la nave y disparar balas.
- **Gráficos personalizados:** Incluye fondos, sprites de meteoritos, balas y la nave.
- **Computación paralela:** Cada bala y meteorito se gestiona en su propio hilo, demostrando la práctica del paralelismo en Python.

---

## **Requisitos del sistema**
1. **Python** 3.8 o superior.
2. Librerías de Python:
   - `pygame`
3. **Sistema operativo:** Funciona en Windows, macOS y Linux.

---

## **Instalación**
1. **Clona este repositorio**:
   ```bash
   git clone https://github.com/whocar3s/Proyecto-Paralela.git
   cd Proyecto-Paralela/Defensa-Planetaria
2. **Instala las dependencias necesarias**:
    ```bash
    pip install pygame
## **Ejecución del Juego**##
Para ejecutar el juego, sigue estos pasos:

1. Abre la terminal o consola de comandos y navega hasta la carpeta del proyecto:
    ```bash
    cd Defensa-Planetaria
2. Ejecuta el archivo principal:
    ```bash
    python game.py
## **Controles del Juego** ##
- **Flechas izquierda/derecha:** Rotan la nave hacia la izquierda o derecha.
- **Barra espaciadora:** Dispara una bala desde la nave.
- **Enter:** Comienza o pausa el juego.
- **Escape:** Sale del juego en cualquier momento

## **Implementación de Paralelismo** ##

**Uso de Hilos (Threading)**
 
 El juego utiliza la librería `threading` de Python para ejecutar meteoritos y balas en hilos separados. Esto permite que los objetos se muevan y actualicen de manera independiente sin bloquear el ciclo principal del juego, mejorando la fluidez.

- **Meteoritos:** Cada meteorito cae en su propio hilo, actualizando su posición sin interferir con otros objetos.

- **Balas:** Cada bala disparada se gestiona en su propio hilo, permitiendo que se mueva sin afectar el rendimiento del juego en general.

## **Grupo:** ##
- Camilo Madero
- Paula Paez
- Juan Felipe Rojas
- Santiago Sotelo