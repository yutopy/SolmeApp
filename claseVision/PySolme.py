# -*- coding: utf-8 -*-
"""
Esta clase toma fotografías de moldes de alta costuras, ubicados sobre un patrón cuadrado y genera un modelo imprimible
del molde con medidas precisas

Created on Wed May 18:07:14 2021
@author: jolumartinez
"""

# import the necessary packages
import numpy as np
import cv2
import requests
import os.path
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas

class ModelosSolme:

    def __init__(self):
        """Inicializador del objeto miembro de la clase"""

    def getImage(self, url):
        """Este método recibe una url, descarga una imagen de la url y devuelve la imagen en un tamaño trabajable"""

        #img = requests.get(url)

        path_folder = os.getcwd()

        img = cv2.imread(path_folder + "/imgPrueba/1.jpeg")

        #Conversión de RGB a HSV
        hsv_original = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        #Configuración de máscaras para el color rojo
        redBajo1 = np.array([0, 230, 20], np.uint8)
        redAlto1 = np.array([8, 255, 255], np.uint8)

        redBajo2 = np.array([175, 230, 20], np.uint8)
        redAlto2 = np.array([179, 255, 255], np.uint8)

        #Filtrado de imagen
        maskRed1 = cv2.inRange(hsv_original, redBajo1, redAlto1)
        maskRed2 = cv2.inRange(hsv_original, redBajo2, redAlto2)
        maskRed = cv2.add(maskRed1, maskRed2)

        #Limpieza y eliminación de ruido en imagen
        kernel = np.ones((3, 3), np.uint8)
        bolas = cv2.morphologyEx(maskRed, cv2.MORPH_OPEN, kernel)
        bolas = cv2.morphologyEx(maskRed, cv2.MORPH_CLOSE, kernel)

        # Encontrar contornos
        contours, _ = cv2.findContours(bolas, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        #Dibujar contornos encontrados sobre la imagen original
        cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

        cv2.imshow('Original', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        #Calcular estadísticas de los objetos hayados en la imagen
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bolas)

        print(centroids)

        #Filtrado de los objetos de la imagen por tamaño, obviando el fondo.
        valor_max_pix = (np.max(stats[:4][1:])) / 2
        pin = np.where((stats[:, 4][1:]) > valor_max_pix)
        pin = pin[0] + 1

        #Se obtiene un arreglo con los centroides
        centroids = np.array(centroids[pin])

        #Se organiza el arreglo para garantizar las ubicaciones del cuadrado de referencia
        centroids = centroids[centroids[:, 0].argsort()]

        if centroids[0][1] < centroids[1][1]:
            ref_1 = centroids[0]
            ref_2 = centroids[1]
        else:
            ref_2 = centroids[0]
            ref_1 = centroids[1]

        if centroids[2][1] < centroids[3][1]:
            ref_3 = centroids[2]
            ref_4 = centroids[3]
        else:
            ref_4 = centroids[2]
            ref_3 = centroids[3]

        #Se genera el vector ordenado de coordenadas de los círculos rojos para calcular la homografía
        las_xprima = np.array([ref_1, ref_2, ref_3, ref_4])

        #Se genera un vector con coordenasa de referencia en pixeles, directamente proporcionales al tamaño del cuadrado de referencia
        las_x = np.array([(0, 0), (0, 1000), (1000, 0), (1000, 1000)])

        #Se calcula la homogrfía H
        H, estado = cv2.findHomography(las_xprima, las_x, cv2.RANSAC, 0.01)

        #Se rectifica la imagen original para obtener el cuadrado perfecto de nxn
        rectificada = cv2.warpPerspective(img, H,
                                          (int(1.5 * img.shape[1]),
                                           int(1.5 * img.shape[0])))

        #Se recorta la imagen a el área de interés
        rectificada = rectificada[100:900, 100:900]

        cv2.imshow('Rectificada', rectificada)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        gray_rectificada = cv2.cvtColor(rectificada, cv2.COLOR_BGR2GRAY)
        _, bin_rectificada = cv2.threshold(gray_rectificada, 150, 200, cv2.THRESH_BINARY_INV)
        print(type(bin_rectificada))

        cv2.imshow('Rectificada contornos', bin_rectificada)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Encontrar contornos del objeto de interés
        #contours, _ = cv2.findContours(bin_rectificada, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Dibujar contornos encontrados sobre la imagen rectificada
        #cv2.drawContours(rectificada, contours, -1, (0, 255, 0), 2)

        # Calcular estadísticas de los objetos hayados en la imagen
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_rectificada)

        print(labels.shape)

        # Detectamos los bordes con Canny
        canny = cv2.Canny(gray_rectificada, 50, 150)

        # Buscamos los contornos
        (contornos, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Mostramos el número de objetos por consola
        print("He encontrado {} objetos".format(len(contornos)))

        #Se crea una plantilla en blanco para la salida
        modelo = np.ones((800, 800, 3), np.uint8)*255

        #Se dibuja el contorno del moedlo para ver que si esté bien
        cv2.drawContours(modelo, contornos, -1, (255, 0, 0), 2)

        #Se redimensiona el modelo y se suavisa. Hay que subir resolución para la impresión
        modelo = cv2.resize(modelo, (2400, 2400), interpolation = cv2.INTER_AREA)

        #Se guarda la imagen como archivo jpg, para luego poder insertarla en el PDF
        cv2.imwrite("img_modelo.jpg", modelo)

        #Se muesra el modelo final
        cv2.imshow("Modelo", modelo)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        #Se establece el tamaño del lienzo PDF
        pagesize = (800 * mm, 800 * mm)

        #Se crea el lienzo con el nombre Modelo.
        c = canvas.Canvas("modelo.pdf", pagesize=pagesize)

        #Se inserta la imagen y se redimensiona a 800X800 mm como la original
        c.drawImage("img_modelo.jpg", 0, 0, width=800*mm, height=800*mm)
        c.save()

        return modelo

    def verificarOrdenes(self):
        return

def main():
    print("Iniciando")
    primer_paso = ModelosSolme()
    img=primer_paso.getImage("Hola mundo")

# ===========================================================================
if __name__ == '__main__':
    main()