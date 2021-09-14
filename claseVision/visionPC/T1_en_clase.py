#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is an example on homography estimation using OpenCV

Created on Tue Sep 12 21:01:53 2017
@author: gholguin
"""

import cv2
import numpy as np

# variable global con las coordenadas
puntos_click = list()

# ================================================================
def click_and_count(event, x, y, flags, param):
    """Definicion del callback que atiende el mouse"""

    global puntos_click

    if event == cv2.EVENT_LBUTTONDOWN:
        puntos_click.append((x, y))

# =================================================================
class HomografiasOpenCV():
    """
    Esta es una clase para solucionar problemas con homografías
    """

    # Atributos de la clase
    error_reproyeccion = 0.01

    # --------------------------------------------------------
    def __init__(self):
        """Inicializador del objeto miembro de la clase"""

        # Atributos del objeto
        self.imagen_original = 0
        self.rectificada = 0

        self.las_xprima = np.array(list())
        self.las_x = np.array(list())

        self.H = list()

    # --------------------------------------------------------
    def cargar_imagen(self, ruta):
        """Metodo que carga una imagen desde una ruta en DD"""

        # exite un archivo en "ruta"

        # si exite, cargar la imagen
        self.imagen_original = cv2.imread(ruta)

    # --------------------------------------------------------
    def obtener4puntos(self):
        """Permite al usuario hacer clic en 4 puntos"""

        global puntos_click

        # Clonar la imagen original para poder escribir sobre ella
        # sin modificarla
        imagen_conpuntos = self.imagen_original.copy()

        # Mostrar la imagen
        cv2.namedWindow("Imagen_Original")
        cv2.setMouseCallback("Imagen_Original", click_and_count)

        while True:
            # mostrar la imagen
            cv2.imshow("Imagen_Original", imagen_conpuntos)
            key = cv2.waitKey(1) & 0xFF

            # menu principal
            # Si se presiona "r" resetee la imagen
            if key == ord("r"):
                puntos_click = list()
                imagen_conpuntos = self.imagen_original.copy()

            # Si se presiona "q" salir
            elif key == ord("q"):
                break

            # Graficar los puntos que hayan en puntos_click
            if puntos_click:
                for pts_id, coords in enumerate(puntos_click):
                    # coordenadas
                    x, y = coords[0], coords[1]
                    # dibujar un circulo
                    cv2.circle(imagen_conpuntos, (x, y), 5, (0, 0, 255), 5, 2)
                    # Seleccionar una fuente
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(imagen_conpuntos, str(pts_id+1), (x, y), font,
                                4, (0, 0, 255), 2, cv2.LINE_AA)

    # --------------------------------------------------------
    def encontrar_H(self):
        """Metodo para estimar la homografia"""

        self.H, estado = cv2.findHomography(self.las_xprima, self.las_x, cv2.RANSAC,
                                            self.error_reproyeccion)

        return self.H, estado

    # --------------------------------------------------------
    def remover_proyectividad(self):
        """Metodo para aplicar una H a una imagen y obtener la proyectividad"""

        self.rectificada = cv2.warpPerspective(self.imagen_original, self.H,
                                               (int(1.5*self.imagen_original.shape[1]),
                                               int(1.5*self.imagen_original.shape[0])))
        cv2.namedWindow("Rectificada")
        cv2.imshow("Rectificada", self.rectificada)
        cv2.waitKey(0)

# ==========================================================================
def main():
    """Funcion principal
       Solo se debe ejecutar, si se ejecuta el programa de forma individual
       Pero no se debe ejecutar si se carga como modulo dentro de otro programa
    """

    # Crear un objeto de la clase HomografiasOpenCV
    objetoh = HomografiasOpenCV()

    # Cargar una imagen en el objeto
    objetoh.cargar_imagen("capilla60.jpg")

    # Permitir al usuario marcar 4 puntos
    objetoh.obtener4puntos()

    # establecer correspondencias
    objetoh.las_xprima = np.array(puntos_click)
    print(puntos_click)
    objetoh.las_x = np.array([(100, 200), (500, 200), (500, 500), (100, 500)])

    # encontrar H
    H, estado = objetoh.encontrar_H()

    # remover pryectividad
    objetoh.remover_proyectividad()

# ==========================================================================
if __name__ == '__main__':
    main()

