# -*- coding: utf-8 -*-
"""
NUAM Ph.D Class

Created on Wed Sep 13 18:07:14 2017
@author: jolumartinez
"""

# Imports

import cv2
import numpy as np
import os.path
import serial
import math
from scipy.interpolate import interp1d
from time import time
import numpy as np
from numpy import *
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import imutils
import glob
from tqdm import tqdm
import PIL.ExifTags
import PIL.Image
from PIL.ExifTags import GPSTAGS
import open3d as o3d
from datetime import datetime
import sys
#import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets


puntos_click = list()


# ================================================================
def click_and_count(event, x, y, flags, param):
    """Definicion del callback que atiende el mouse"""

    global puntos_click

    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        puntos_click.append((x, y))


# +=================================================================================================
class ProyectividadOpenCV():
    """
    Esta es una clase para solucionar problemas con homografias
    """
    # Atributos de la clase
    error_reproyeccion = 4

    # --------------------------------------------------------------------------
    def __init__(self):
        """Inicializador del objeto miembro de la clase"""

    # --------------------------------------------------------------------------
    def coser_imagenes(self, ruta_img_base, ruta_img_adicional, radio=0.7, error_reproyeccion=4,
                       coincidencias=False):
        """Metodo que carga una imagen desde una ruta en disco duro"""

        imagen_adicional = ruta_img_adicional
        imagen_base = ruta_img_base

        # Se obtienen los puntos deinterés

        (kpsBase, featuresBase) = self.obtener_puntos_interes(imagen_base)
        (kpsAdicional, featuresAdicional) = self.obtener_puntos_interes(imagen_adicional)
        # Se buscan las coincidencias

        M = self.encontrar_coincidencias(imagen_base, imagen_adicional, kpsBase, kpsAdicional, featuresBase,
                                         featuresAdicional, radio)

        if M is None:
            print("Sin coincidencias")
            return None, None

        if len(M) > 10:
            # construct the two sets of points

            #M2 = cv2.getPerspectiveTransform(featuresBase, featuresAdicional)
            (H, status) = self.encontrar_H_RANSAC_Estable(M, kpsBase, kpsAdicional, error_reproyeccion)
            if H is None:
                print("No se encontró la homografía")
                return None, None

            vis = self.dibujar_coincidencias(imagen_base, imagen_adicional, kpsBase, kpsAdicional, M, status)

            width = imagen_base.shape[1] + imagen_adicional.shape[1]
            height = imagen_base.shape[0]

            result = cv2.warpPerspective(imagen_base, H, (width, height))
            result[0:imagen_adicional.shape[0], 0:imagen_adicional.shape[1]] = imagen_adicional
            return result, vis

        print("Pocas coincidencias")
        return None, None
    
    # --------------------------------------------------------------------------
    def estabilizador_imagen(self, imagen_base, imagen_a_estabilizar, radio=1, error_reproyeccion=5,
                             coincidencias=False):
        """Esta clase devuelve una secuencia de imágenes tomadas de la cámara estabilizada con respecto a la primera imagen"""

        # Se obtienen los puntos deinterés

        (kpsBase, featuresBase) = self.obtener_puntos_interes(imagen_base)
        (kpsAdicional, featuresAdicional) = self.obtener_puntos_interes(imagen_a_estabilizar)
        # Se buscan las coincidencias

        M = self.encontrar_coincidencias(imagen_base, imagen_a_estabilizar, kpsBase, kpsAdicional, featuresBase,
                                         featuresAdicional, radio)

        if M is None:
            print("Sin coincidencias")
            return None

        if len(M) > 10:
            # construct the two sets of points

            #M2 = cv2.getPerspectiveTransform(featuresBase, featuresAdicional)
            (H, status) = self.encontrar_H_RANSAC_Estable(M, kpsBase, kpsAdicional, error_reproyeccion)
            print(H)
            print(status)
            if H is None:
                print("No se encontró la homografía")
                return None
            estabilizada = cv2.warpPerspective(imagen_base, H, (imagen_base.shape[1], imagen_base.shape[0]))
            return estabilizada

        print("Pocas coincidencias")
        return None

    def estabilizador_imagen_with_H(self, imagen_base, H=None):
        """Esta clase devuelve una secuencia de imágenes tomadas de la cámara estabilizada con respecto a la primera imagen"""

        estabilizada = cv2.warpPerspective(imagen_base, H, (imagen_base.shape[1], imagen_base.shape[0]))
        return estabilizada

    def img_alignment_sequoia(self, img_RGB, img_GRE, img_base_NIR, img_RED, img_REG, width, height):
        """This class takes the five images given by Sequoia Camera and makes a photogrammetric
        alignment. Returns four images (GRE, NIR, RED, REG) aligned with the RGB image"""

        # Se valida que si estén todas las variables en el argumento

        # width, height = img_SIZE

        # Se redimencionan todas las imagenes al mismo tamaño especificado en image_SIZE

        b_RGB = cv2.resize(img_RGB, (width, height), interpolation=cv2.INTER_LINEAR)
        b_GRE = cv2.resize(img_GRE, (width, height), interpolation=cv2.INTER_LINEAR)
        base_NIR = cv2.resize(img_base_NIR, (width, height), interpolation=cv2.INTER_LINEAR)
        b_RED = cv2.resize(img_RED, (width, height), interpolation=cv2.INTER_LINEAR)
        b_REG = cv2.resize(img_REG, (width, height), interpolation=cv2.INTER_LINEAR)

        # Se estabilizan todas las imágenes con respecto a la imagen base

        stb_GRE = self.estabilizador_imagen(b_GRE, base_NIR)
        if stb_GRE is None:
            print("GRE None")
        stb_RGB = self.estabilizador_imagen(b_RGB, base_NIR)
        if stb_GRE is None:
            print("RGB None")
        stb_RED = self.estabilizador_imagen(b_RED, base_NIR)
        if stb_GRE is None:
            print("RED None")
        stb_REG = self.estabilizador_imagen(b_REG, base_NIR)
        if stb_GRE is None:
            print("REG None")

        return stb_RGB, stb_GRE, base_NIR, stb_RED, stb_REG

    # --------------------------------------------------------------------------
    def obtener_puntos_interes(self, imagen):
        """Se obtienen los puntos de interes cn SIFT"""

        descriptor = cv2.xfeatures2d.SIFT_create()
        #orb = cv2.ORB_create(nfeatures=1500)
        (kps, features) = descriptor.detectAndCompute(imagen, None)
        #keypoints_orb, descriptors = orb.detectAndCompute(imagen, None)

        return kps, features
        #return keypoints_orb, descriptors

    # --------------------------------------------------------------------------
    def encontrar_coincidencias(self, img1, img2, kpsA, kpsB, featuresA, featuresB, ratio):
        """Metodo para estimar la homografia"""

        #matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        #knn_matches = matcher.knnMatch(featuresA, featuresB, 2)

        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []
        #
        #        # loop over the raw matches
        for m in rawMatches:
            #            # ensure the distance is within a certain ratio of each
            #            # other (i.e. Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        #        print (matches)
        return matches

    # --------------------------------------------------------------------------
    def encontrar_H_RANSAC(self, matches, kpsA, kpsB, reprojThresh):
        """Metodo para aplicar una H a una imagen y obtener la proyectividad"""

        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i].pt for (_, i) in matches])
            ptsB = np.float32([kpsB[i].pt for (i, _) in matches])

            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)

            # return the matches along with the homograpy matrix
            # and status of each matched point
            return (H, status)

        # otherwise, no homograpy could be computed
        return None

    # --------------------------------------------------------------------------
    def encontrar_H_RANSAC_Estable(self, matches, kpsA, kpsB, reprojThresh):
        """Metodo para aplicar una H a una imagen y obtener la proyectividad"""

        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i].pt for (_, i) in matches])
            ptsB = np.float32([kpsB[i].pt for (i, _) in matches])

            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)

            return (H, status)

        return None

    def dibujar_coincidencias(self, imagen_base, imagen_adicional, kpsA, kpsB, matches, status):

        (hA, wA) = imagen_base.shape[:2]
        (hB, wB) = imagen_adicional.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imagen_base
        vis[0:hB, wA:] = imagen_adicional

        # loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # only process the match if the keypoint was successfully
            # matched
            if s == 1:
                # draw the match
                ptA = (int(kpsA[queryIdx].pt[0]), int(kpsA[queryIdx].pt[1]))
                ptB = (int(kpsB[trainIdx].pt[0]) + wA, int(kpsB[trainIdx].pt[1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)

        # return the visualization
        return vis

    # --------------------------------------------------------------------------
    def encontrar_H_marcas(self, las_xprima, las_x):
        """Metodo para estimar la homografia"""
        # Se utiliza 0 y no RANSAC porque deseo que utilice todos los puntos que se tienen
        H, estado = cv2.findHomography(las_x, las_xprima, 0, 0.1)
        return H, estado

    # --------------------------------------------------------------------------
    def estabilizar_desde_marcas(self, imagen, marcas_click, marcas_cad_mm):
        """Esta clase retorna una imagen estabilizada con base en una imagen abstraida delas marcas del cad dadas en mm"""

        # Lo primero es tratar la imagen entrante
        blur = cv2.blur(imagen, (3, 3))
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # Se aplica un filtro de color verde para separar las marcas del fondo
        thresh_marcas = cv2.inRange(hsv, np.array((49, 50, 50)), np.array((107, 255, 255)))
        marcas_H = list()
        cad_H = list()
        # Se hace una busqueda de las marcas visibles en un radio de 30 pixelesy se filtranpor area para sacar los pares que permitiran hallar la homografia
        for i in range(0, len(marcas_click)):
            #            print(i)
            x_men = marcas_click[i][0] - 10
            x_may = marcas_click[i][0] + 10
            y_men = marcas_click[i][1] - 10
            y_may = marcas_click[i][1] + 10
            area_marca = thresh_marcas[y_men:y_may, x_men:x_may]
            image_marcas, contours_marcas, hierarchy_marcas = cv2.findContours(area_marca, cv2.RETR_LIST,
                                                                               cv2.CHAIN_APPROX_SIMPLE)

            max_area = 65
            best_cnt = 1
            for cnt in contours_marcas:
                area = 1
                area = cv2.contourArea(cnt)
                #                print(contours_marcas)
                #                print(area,m)
                if area > max_area and area < 85:
                    max_area = area
                    best_cnt = cnt
                    # finding centroids of best_cnt and draw a circle there
                    cM = cv2.moments(best_cnt)
                    cx, cy = int(cM['m10'] / cM['m00']), int(cM['m01'] / cM['m00'])
                    cx = x_men + cx
                    cy = y_men + cy
                    marcas_H.append((cx, cy))
                    cad_H.append((marcas_cad_mm[i][0] + 100, marcas_cad_mm[i][1]))
        #                    print(marcas_H,cad_H)

        las_x = np.array(cad_H)
        las_xprima = np.array(marcas_H)
        print(las_x, las_xprima)
        if len(las_xprima) > 4:
            H, estado = self.encontrar_H_marcas(las_x, las_xprima)

            estabilizada = cv2.warpPerspective(imagen, H, (1200, 1200))

            return estabilizada

        return None

    # --------------------------------------------------------------------------
    def estabilizar_desde_centroides_marcas(self, imagen, marcas_click, marcas_cad_mm):
        """Esta clase retorna una imagen estabilizada con base en una imagen abstraida delas marcas del cad dadas en mm"""

        las_x = np.array(marcas_cad_mm)
        las_xprima = np.array(marcas_click)
        print(las_x, las_xprima)
        if len(las_xprima) > 4:
            H, estado = self.encontrar_H_marcas(las_x, las_xprima)

            estabilizada = cv2.warpPerspective(imagen, H, (650, 650))

            return estabilizada

        return None

    # --------------------------------------------------------------------------
    def inicializar_marcas(self, img_base):
        """Permite al usuario hacer click en el centro apriximado de cada marca y las guarda en orden"""

        global puntos_click

        # Copiar la imagen original para poder escribir sobre ella
        # Sin modificarla
        imagen_conmarcas = self.img_base.copy()

        # Mostrar la imagen
        cv2.namedWindow("Imagen_base")
        cv2.setMouseCallback("Imagen_base", click_and_count)

        while True:
            # Mostrar a imagen
            cv2.imshow("Imagen_base", imagen_conmarcas)
            key = cv2.waitKey(1) & 0xFF

            # Menu principal
            # Si se presiona r resetee la imagen
            if key == ord("r"):
                puntos_click = list()
                imagen_conmarcas = self.img_base.copy()

            # Si se presiona q salir
            elif key == ord("q"):
                return puntos_click

            # Graficar los puntos que hayan en puntos_click
            if puntos_click:
                for pts_id, coords in enumerate(puntos_click):
                    # Coordenadas
                    x, y = coords[0], coords[1]
                    # Dibujar un circulo
                    cv2.circle(imagen_conmarcas, (x, y), 5, (0, 0, 255), 5, 2)
                    # Seleccionar una fuente
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(imagen_conmarcas, str(pts_id + 1), (x, y), font, 10, (0, 0, 255), 5)

    # ------------------------------------------------------------------------------------------------

    def cinematica_inversa(self, a, b):
        """Recibe las coordenadas en centimetros"""
        # Se valida que la coordenada se encuentre dentro del area de trabajo. Si no esta se ubica en el centro el manipulador
        if a <= 14 or a >= 34:
            a = 15
        if b <= 4 or b >= 26:
            b = 16

        xp = a
        yp = b

        xa = 0
        ya = 0
        xb = 46
        yb = 0
        xc = 46 / 2
        yc = 46 * math.sin(math.pi / 3)

        # Dimenciones de los eslabones y acopladores del manipulador (Unidades en cm.) 
        manivela = 19

        # Eslabones (Cadenas Cinematica 1)
        l1 = manivela
        L_DA = l1
        l4 = manivela
        L_GD = l4

        # Eslabones (Cadena Cinematica 2)
        l2 = manivela
        L_EB = l2
        l5 = manivela
        L_HE = l5

        # Eslabones (Cadena Cinematica 3)
        l3 = manivela
        L_FC = l3
        l6 = manivela
        L_IF = l6

        # plataforma movil
        # El parametro (h) representa el baricentro de la plataforma.
        h = 7.5056
        # phi=0; % Plataforma no rota.
        phi = 0 * math.pi / 180  # Plataforma rota.

        # Datos de conversión (Grados --> Bits)

        grados = 360
        decimal = 4096
        #    Resolucion del servomotor.

        #        xp=23#               23.5
        #        yp=13.279056191#       13.279056191

        # Coordenadas de la plataforma movil 
        # Coordenadas del punto G.
        xg = xp - h * math.cos(phi + (math.pi / 6))
        yg = yp - h * math.sin(phi + (math.pi / 6))
        # Coordenadas del punto H.
        xh = xp - h * math.cos(phi + (math.pi - (math.pi / 6)))
        yh = yp - h * math.sin(phi + (math.pi - (math.pi / 6)))

        # Coodenadas del punto I.
        xi = xp - h * math.cos(phi + (3 * math.pi / 2))
        yi = yp - h * math.sin(phi + (3 * math.pi / 2))

        # Primera cadena vectorial 1.
        L_GA = math.sqrt((xg - xa) ** 2 + (yg - ya) ** 2)  # REVISADO
        gamma1 = math.acos((L_GA ** 2 + L_DA ** 2 - L_GD ** 2) / (2 * L_GA * L_DA))  # REVISADO
        fi1 = math.atan2((yg - ya), (xg - xa))  # Revisado
        tetha1 = fi1 + gamma1  # revisado

        # Segunda cadena vectorial 2.
        L_HB = math.sqrt((xh - xb) ** 2 + (yh - yb) ** 2)  # Revisado
        gamma2 = math.acos((L_HB ** 2 + L_EB ** 2 - L_HE ** 2) / (2 * L_EB * L_HB))  # Revisado
        fi2 = math.atan2((yh - yb), (xh - xb))  # revisado
        tetha2 = fi2 + gamma2  # revisado

        # Tercera cadena vetorial 3.
        L_IC = math.sqrt((xi - xc) ** 2 + (yi - yc) ** 2)  # Revisado
        gamma3 = math.acos((L_IC ** 2 + L_FC ** 2 - L_IF ** 2) / (2 * L_FC * L_IC))  # Revisado
        fi3 = math.atan2((yi - yc), (xi - xc))  # revisado
        tetha3 = fi3 + gamma3  # revisado

        tetha11 = tetha1 * 180 / math.pi

        tetha22 = tetha2 * 180 / math.pi

        tetha33 = tetha3 * 180 / math.pi

        # Luego se inicia el factor de conversion (Grados-->Bytes) para que los
        # servor puedan iniciar la lectura y establecer inicio de movimiento.

        # Para dar inicio al movimiento se establece la pose inicial de la
        # plataforma movil.

        # cadena 1
        if tetha11 <= 0:
            tetha11 = tetha11 - 30
        elif tetha11 >= 0:
            tetha11 = tetha11 - 30

        #     cadena 2
        if tetha22 <= 0:
            tetha22 = tetha22 + 45
        elif tetha22 >= 0:
            tetha22 = tetha22 + 45

        #     cadena 3
        if tetha33 <= 0:
            tetha33 = tetha33 + 65
        elif tetha33 >= 0:
            tetha33 = tetha33 + 65

        #    Ajuste por minimos cuadrados (Error)

        m = 0.99182076813655761024
        b = -10.9331436699857752489
        tetha11 = m * tetha11 + b
        tetha11 = tetha11 + 19

        #     para el servo 2

        m2 = 0.98968705547652916074
        b2 = -8.4679943100995732575
        tetha22 = m2 * tetha22 + b2
        tetha22 = tetha22 + 17

        #     para el servo 3
        m3 = 0.99497392128971076339
        b3 = -3.7439544807965860597
        tetha33 = m3 * tetha33 + b3
        tetha33 = tetha33 + 6.5

        #     Inicio de conversion - Esta parte envia el dato en bytes al driver.
        # Se convierten a decimal para poder hacer luego la conversión a bytes en el serial
        Btheta11 = round((tetha11 * decimal) / grados)
        Btheta22 = round((tetha22 * decimal) / grados)
        Btheta33 = round((tetha33 * decimal) / grados)

        return Btheta11, Btheta22, Btheta33

    # ---------------------------------------------------------------------------------------------------

    def abrir_puerto_serial(self, puerto='COM3', tasa_bs=1000000, paridad=1, rtscts=1, timeout=0):
        """Este metodo abre el puerto serial especificado en el argumento con las carc¿acteristicas de comunicacion de los motores"""

        ser = serial.Serial(
            port=puerto,
            baudrate=tasa_bs,
            parity=serial.PARITY_NONE,
            rtscts=rtscts,
            timeout=timeout
            #    stopbits=1,
            #    bytesize=8
        )
        return ser

    # ------------------------------------------------------------------------------------------------

    def cerrar_puerto_serial(self, ser):
        """Este metodo cierra el puerto serial"""

        ser.close()
        return None

    # ------------------------------------------------------------------------------------------------

    def enviar_tethas_servomotores(self, ser, b1, b2, b3):
        """Este metodo envía los angulos betha a los servomotores correspondientes"""

        betha = ([b1, b2, b3])
        bin_betha1 = bin(betha[0])
        bin_betha2 = bin(betha[1])
        bin_betha3 = bin(betha[2])

        bin_betha1 = "0000000000" + bin_betha1[2:(len(bin_betha1))]
        bin_betha2 = "0000000000" + bin_betha2[2:(len(bin_betha2))]
        bin_betha3 = "0000000000" + bin_betha3[2:(len(bin_betha3))]

        nl_bin_betha1 = bin_betha1[(len(bin_betha1) - 8):(len(bin_betha1))]
        nh_bin_betha1 = bin_betha1[(len(bin_betha1) - 12):(len(bin_betha1) - 8)]

        nl_bin_betha2 = bin_betha2[(len(bin_betha2) - 8):(len(bin_betha2))]
        nh_bin_betha2 = bin_betha2[(len(bin_betha2) - 12):(len(bin_betha2) - 8)]

        nl_bin_betha3 = bin_betha3[(len(bin_betha3) - 8):(len(bin_betha3))]
        nh_bin_betha3 = bin_betha3[(len(bin_betha3) - 12):(len(bin_betha3) - 8)]

        nl_dec_betha1 = int(nl_bin_betha1, 2)
        nh_dec_betha1 = int(nh_bin_betha1, 2)

        nl_dec_betha2 = int(nl_bin_betha2, 2)
        nh_dec_betha2 = int(nh_bin_betha2, 2)

        nl_dec_betha3 = int(nl_bin_betha3, 2)
        nh_dec_betha3 = int(nh_bin_betha3, 2)

        # print(nl_dec_betha2)
        # print(nh_dec_betha2)

        r1 = 1 + 5 + 3 + 30 + nl_dec_betha1 + nh_dec_betha1
        r2 = 2 + 5 + 3 + 30 + nl_dec_betha2 + nh_dec_betha2
        r3 = 3 + 5 + 3 + 30 + nl_dec_betha3 + nh_dec_betha3

        z1 = bin(r1)
        z1 = "0000000000" + z1[2:(len(z1))]
        z2 = bin(r2)
        z2 = "0000000000" + z2[2:(len(z2))]
        z3 = bin(r3)
        z3 = "0000000000" + z3[2:(len(z3))]

        z1 = z1[(len(z1) - 12):(len(z1))]
        z2 = z2[(len(z2) - 12):(len(z2))]
        z3 = z3[(len(z3) - 12):(len(z3))]
        # print(z1)

        not_z1 = bin(int(z1, 2) ^ 4095)
        not_z2 = bin(int(z2, 2) ^ 4095)
        not_z3 = bin(int(z3, 2) ^ 4095)
        #        print(not_z1)

        n11 = not_z1[(len(not_z1) - 8):(len(not_z1))]
        n22 = not_z2[(len(not_z2) - 8):(len(not_z2))]
        n33 = not_z3[(len(not_z3) - 8):(len(not_z3))]
        #        print(n11)

        p11 = int(n11, 2)  # este seria el checksum
        p22 = int(n22, 2)
        p33 = int(n33, 2)

        # Parametro para enviarposicion a losservos
        parametro = 30

        #        vector= [255,255,1,5,3,parametro,nl_dec_betha1,nh_dec_betha1,p11,255,255,2,5,3,parametro,nl_dec_betha2,nh_dec_betha2,p22,255,255,3,5,3,parametro,nl_dec_betha3,nh_dec_betha3,p33]
        vector_1 = [255, 255, 1, 5, 3, parametro, nl_dec_betha1, nh_dec_betha1, p11]
        vector_2 = [255, 255, 2, 5, 3, parametro, nl_dec_betha2, nh_dec_betha2, p22]
        vector_3 = [255, 255, 3, 5, 3, parametro, nl_dec_betha3, nh_dec_betha3, p33]

        ser.write(vector_1)
        ser.write(vector_2)
        ser.write(vector_3)

        mess_status = ser.read(1000)

        return mess_status

    # ------------------------------------------------------------------------------------------------

    def inicializar_servos(self, ser):
        """Este metodo envía los angulos betha a los servomotores correspondientes"""
        # Parametro para enviarposicion a losservos
        parametro = 32
        betha = ([9, 9, 9])
        bin_betha1 = bin(betha[0])
        bin_betha2 = bin(betha[1])
        bin_betha3 = bin(betha[2])

        bin_betha1 = "0000000000" + bin_betha1[2:(len(bin_betha1))]
        bin_betha2 = "0000000000" + bin_betha2[2:(len(bin_betha2))]
        bin_betha3 = "0000000000" + bin_betha3[2:(len(bin_betha3))]

        nl_bin_betha1 = bin_betha1[(len(bin_betha1) - 8):(len(bin_betha1))]
        nh_bin_betha1 = bin_betha1[(len(bin_betha1) - 12):(len(bin_betha1) - 8)]

        nl_bin_betha2 = bin_betha2[(len(bin_betha2) - 8):(len(bin_betha2))]
        nh_bin_betha2 = bin_betha2[(len(bin_betha2) - 12):(len(bin_betha2) - 8)]

        nl_bin_betha3 = bin_betha3[(len(bin_betha3) - 8):(len(bin_betha3))]
        nh_bin_betha3 = bin_betha3[(len(bin_betha3) - 12):(len(bin_betha3) - 8)]

        nl_dec_betha1 = int(nl_bin_betha1, 2)
        nh_dec_betha1 = int(nh_bin_betha1, 2)

        nl_dec_betha2 = int(nl_bin_betha2, 2)
        nh_dec_betha2 = int(nh_bin_betha2, 2)

        nl_dec_betha3 = int(nl_bin_betha3, 2)
        nh_dec_betha3 = int(nh_bin_betha3, 2)

        # print(nl_dec_betha2)
        # print(nh_dec_betha2)

        r1 = 1 + 5 + 3 + parametro + nl_dec_betha1 + nh_dec_betha1
        r2 = 2 + 5 + 3 + parametro + nl_dec_betha2 + nh_dec_betha2
        r3 = 3 + 5 + 3 + parametro + nl_dec_betha3 + nh_dec_betha3

        z1 = bin(r1)
        z1 = "0000000000" + z1[2:(len(z1))]
        z2 = bin(r2)
        z2 = "0000000000" + z2[2:(len(z2))]
        z3 = bin(r3)
        z3 = "0000000000" + z3[2:(len(z3))]

        z1 = z1[(len(z1) - 12):(len(z1))]
        z2 = z2[(len(z2) - 12):(len(z2))]
        z3 = z3[(len(z3) - 12):(len(z3))]
        # print(z1)

        not_z1 = bin(int(z1, 2) ^ 4095)
        not_z2 = bin(int(z2, 2) ^ 4095)
        not_z3 = bin(int(z3, 2) ^ 4095)
        #        print(not_z1)

        n11 = not_z1[(len(not_z1) - 8):(len(not_z1))]
        n22 = not_z2[(len(not_z2) - 8):(len(not_z2))]
        n33 = not_z3[(len(not_z3) - 8):(len(not_z3))]
        #        print(n11)

        p11 = int(n11, 2)  # este seria el checksum
        p22 = int(n22, 2)
        p33 = int(n33, 2)

        #        vector= [255,255,1,5,3,parametro,nl_dec_betha1,nh_dec_betha1,p11,255,255,2,5,3,parametro,nl_dec_betha2,nh_dec_betha2,p22,255,255,3,5,3,parametro,nl_dec_betha3,nh_dec_betha3,p33]
        vector_1 = [255, 255, 1, 5, 3, parametro, nl_dec_betha1, nh_dec_betha1, p11]
        vector_2 = [255, 255, 2, 5, 3, parametro, nl_dec_betha2, nh_dec_betha2, p22]
        vector_3 = [255, 255, 3, 5, 3, parametro, nl_dec_betha3, nh_dec_betha3, p33]

        ser.write(vector_1)
        ser.write(vector_2)
        ser.write(vector_3)

        mess_status = ser.read(1000)

        return mess_status

    # ------------------------------------------------------------------------------------------------

    # ===========================================================================
    def manipulador_mecanica(self):
        """Funcion principal
           Solo se debe ejecutar si se ejecuta el programa de forma individual
           Pero no se debe ejecutar si se carga como modulo dentro de otro programa
        """

        a = 80
        b = -100
        # Coordenadas de busqueda las marcas
        marcas_cad_mm = (
        [[150, -50], [310, -50], [130, 0], [330, 0], [170, 50], [290, 50], [100, 100], [360, 100], [250, 145],
         [435, 145], [80, 220], [380, 220], [170, 250], [290, 250], [80, 280], [380, 280], [130, 330], [300, 330],
         [230, 318.4]])
        marcas_cad_mm_1 = (
        [[150 + a, 650 + b], [130 + a, 600 + b], [330 + a, 600 + b], [170 + a, 550 + b], [290 + a, 550 + b],
         [100 + a, 500 + b], [360 + a, 500 + b], [80 + a, 380 + b], [380 + a, 380 + b], [170 + a, 350 + b],
         [80 + a, 320 + b], [380 + a, 320 + b], [130 + a, 270 + b], [230 + a, 281.6 + b]])
        marcas_cad_mm_neg = (
        [[0, 0], [150, 50], [310, 50], [130, 0], [330, 0], [170, -50], [290, -50], [100, -100], [360, -100], [25, -145],
         [435, -145], [80, -220], [380, -220], [170, -250], [290, -250], [80, -280], [380, -280], [130, -330],
         [300, -330], [230, -318.4]])
        marcas_click = (
        [[248, 428], [359, 431], [238, 389], [378, 392], [276, 354], [340, 355], [223, 322], [396, 323], [176, 288],
         [426, 291], [200, 234], [412, 246], [282, 219], [342, 224], [203, 189], [417, 198], [244, 180], [381, 184],
         [311, 173]])
        centroides_marcas = (
        [[247, 426], [237, 388], [376, 390], [276, 353], [339, 354], [222, 320.5], [395, 322], [199, 233], [411, 245],
         [280.5, 218], [202, 188], [416, 197], [242, 179], [310, 172]])

        referencia_marca_17_medido = [201, 195]
        referencia_marca_17_cad = [130, 330]
        nuevo_cero = [71, 525]

        # Se utiliza esta linea si se desea probar e manipulador con un video precargado
        #    cap = cv2.VideoCapture('videoFinalM.wmv')

        # Se utiliza esta linea si se desea probar directamente con la camara. Hay que especificar el numero de la camara en el sistema
        cap = cv2.VideoCapture(0)

        # Se captura el valor de la tasa de adquisicion del video para alimentar Kalman. Solo para video
        #    fps = cap.get(cv2.CAP_PROP_FPS)

        # Se especifica la tasa de captura para Kalman. ¿Como se hace?
        #    fps = 30

        # si no se conce la ubicacion de las marcas, se pueden indicar con la siguiente linea
        # marcas_click = prm.inicializar_marcas(img_base)

        # Se crea el objeto e la clase proyectividad
        estabilizador = ProyectividadOpenCV()

        # Se carga una imagen base para hallar la homografia de esta contra el CAD y asi utilizarla como base
        img_for_mm = cv2.imread("img_base.png")

        # Este metodo halla la homografia contra el cad desde una serie de puntos correspondientes a los centros estimados. El se encarga de buscar los centroides
        # img_base = estabilizador.estabilizar_desde_marcas(img_for_mm,marcas_click,marcas_cad_mm_1)

        # Este metodo halla la homografia contra el cad desde una serie de puntos correspondientes a los centroides de las marcas
        img_base = estabilizador.estabilizar_desde_centroides_marcas(img_for_mm, centroides_marcas, marcas_cad_mm_1)

        # Se crea una variable delta de t para kalman
        delta_t = 0.1

        # Se mide el tiempo que pasa entre la captura de un frame y otro
        tiempo_inicial = time()

        # Se inicializa Kalman
        cx, cy = 200, 200
        kalman = cv2.KalmanFilter(4, 2)
        kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        kalman.transitionMatrix = np.array([[1, 0, delta_t, 0], [0, 1, 0, delta_t], [0, 0, 1, 0], [0, 0, 0, 1]],
                                           np.float32)
        kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) * 0.01
        kalman.measurementNoiseCov = np.array([[1, 0], [0, 1]], np.float32) * 0.0001
        tp = [23, 13]

        # Se abre el puerto serial y se deja abierto para una comunicacion constante
        ser = estabilizador.abrir_puerto_serial(puerto='COM6')  # Hay que verificar el puerto
        if ser.isOpen():
            estabilizador.inicializar_servos(ser)

        #    ser = serial.Serial(
        #    port='COM5',
        #    baudrate=921600,
        #    parity=serial.PARITY_EVEN,
        #    rtscts=1,
        #    timeout=0
        ##    stopbits=1,
        ##    bytesize=8
        #    )
        tiempo_inicial = 0
        tiempo_final = 0.1
        while (True):
            tiempo_final = time()
            delta_t = tiempo_final - tiempo_inicial
            tiempo_inicial = tiempo_final
            # Capture frame-by-frame
            ret, frame = cap.read()

            print(delta_t)

            # Esta clase estabiliza automaticamente la imagen con base una imagen inicial
            estabilizada = estabilizador.estabilizador_imagen(frame, img_base)

            # Se aplica un ruido gausiano para suavizar bordes
            blur = cv2.blur(estabilizada, (3, 3))
            # Se hace la transformacion a HSV
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            # Se aplica la mascara de color que solo deja pasar rojos. Video
            #        thresh_objeto = cv2.inRange(hsv,np.array((0,50,50)), np.array((10,255,255)))

            #        Se aplica la mascara de color que solo deja pasar rojos. Camara
            thresh_objeto = cv2.inRange(hsv, np.array((160, 100, 100)), np.array((179, 255, 255)))

            # se buscan los contornos en la imagen filtada para rojos
            image, contours, hierarchy = cv2.findContours(thresh_objeto, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            # Se inicializa la variable para contar los frames en los que se pierde el objeto para alimentar Kalman
            cont_frame = 1

            # Se hace la busqueda del objeto y se filtra por area para determinar que sea el adecuado
            max_area = 550
            best_cnt = 1
            for cnt in contours:
                area = 1
                area = cv2.contourArea(cnt)
                #        print(area)
                if area > max_area and area < 750:
                    max_area = area
                    best_cnt = cnt
                    # Si seencuentra un area que cumpla, entonces, se halla el centroide de esta
                    M = cv2.moments(best_cnt)
                    cx, cy = int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])

                    # Se dibuja una cruz verde sobre el objeto encontrado
                    cv2.line(blur, (cx - 10, cy), (cx + 10, cy), (0, 255, 0), 1)
                    cv2.line(blur, (cx, cy - 10), (cx, cy + 10), (0, 255, 0), 1)

                    # Se hace la conversion del formato para alimentar Kalman con el centroide
                    mp = np.array([[np.float32(cx)], [np.float32(cy)]])
                    tp = kalman.predict()
                    kalman.correct(mp)

                    # Como el objeto fue encontrado, entonces, se deja en 1 el conteo de frames
                    cont_frame = 1

                # Si no seencuentra el objeto, se hace la estimacion de Kalman y no se actualiza la medida
                if area <= max_area or area >= 750:
                    kalman.transitionMatrix = np.array(
                        [[1, 0, cont_frame * delta_t, 0], [0, 1, 0, cont_frame * delta_t], [0, 0, 1, 0], [0, 0, 0, 1]],
                        np.float32)

                    # Se hace el conteo de los frames en los que no se encuentra la marca para alimentar Kalman
                    cont_frame = cont_frame + 1

                    # Sedibuja una cruz azul en la posicion estimada del objeto
                    tp = kalman.predict()
                    cv2.line(blur, (tp[0] - 10, tp[1]), (tp[0] + 10, tp[1]), (255, 0, 0), 1)
                    cv2.line(blur, (tp[0], tp[1] - 10), (tp[0], tp[1] + 10), (255, 0, 0), 1)

            # Se halla la varianza de la estimacion para reducir la zona de busqueda en el siguiente frame
            varianza_x = kalman.errorCovPost[0, 0]
            varianza_y = kalman.errorCovPost[1, 1]
            devstd_x = varianza_x ** 0.5
            devstd_y = varianza_y ** 0.5

            # para 6 desviaciones estandar
            marco_x = devstd_x * 6
            marco_y = devstd_y * 6

            # Se dibuja un circulo blanco que crece con la varianza a razon de 6 desviaciones estandar
            cv2.circle(blur, (int(tp[0][0]), int(tp[1][0])), int(marco_x), (255, 255, 255), 1, cv2.LINE_AA)
            #        print(tp)

            # Se obtienen las coordenadas en centimetros para la cinematicainversa
            cor_x = 10 + (tp[0][0] - nuevo_cero[0]) / 10
            cor_y = (nuevo_cero[1] - tp[1][0]) / 10
            #        print(cor_x,cor_y)
            if cor_x <= 14 or cor_x >= 34:
                cor_x = 23
            if cor_y <= 4 or cor_y >= 26:
                cor_y = 13.28

            #        print(cor_x,cor_y)
            # Se utiliza la cinematica inversa para obtener el valr de los angulos en decimal de 0 a 4096
            b1, b2, b3 = estabilizador.cinematica_inversa(cor_x, cor_y)
            ##        print(tp[0]/10,tp[1]/10)
            #        print(angulos_decimales)

            if ser.isOpen():
                mensaje_status = estabilizador.enviar_tethas_servomotores(ser, b1, b2, b3)

            #        print(mensaje_status)
            # Visualizacion de imagenes
            cv2.imshow('Umbral', blur)
            cv2.imshow('Mask', thresh_objeto)
            #    cv2.imshow('Marcas',thresh_marcas)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        ser.close()
        cap.release()
        cv2.destroyAllWindows()

    def downsample_image(self, image, reduce_factor):
        for i in range(0, reduce_factor):
            # Check if image is color or grayscale
            if len(image.shape) > 2:
                row, col = image.shape[:2]
            else:
                row, col = image.shape

            image = cv2.pyrDown(image, dstsize=(col // 2, row // 2))
        return image

    # Function to create point cloud file
    def create_output(self, vertices, colors, filename):
        colors = colors.reshape(-1, 3)
        vertices = np.hstack([vertices.reshape(-1, 3), colors])

        ply_header = '''ply
    		format ascii 1.0
    		element vertex %(vert_num)d
    		property float x
    		property float y
    		property float z
    		property uchar red
    		property uchar green
    		property uchar blue
    		end_header
    		'''
        with open(filename, 'w') as f:
            f.write(ply_header % dict(vert_num=len(vertices)))
            np.savetxt(f, vertices, '%f %f %f %d %d %d')

    def disparity_map(self, url_folder="./ejemplos/example_9/", left_cam = 1, right_cam = 2,  img_left=0, img_right=0, win_size=5, min_disp=-1, max_disp=63, blockSize=7):
        """Este método calcula el mapa de disparidad de dos imagenes y lo entrega como una nueva imagen visualizable"
        "Recibe las imágenes y la ruta de los parḿetros de cámara"
        "Entrega la imagen del mapa de disparidad"""

        url_params_left = url_folder + "params_cam_left/"
        url_params_right = url_folder + "params_cam_right/"

        # Load camera parameters
        ret_left = np.load(url_params_left + 'ret.npy')
        K_left = np.load(url_params_left + 'K.npy')
        dist_left = np.load(url_params_left + 'dist.npy')

        ret_right = np.load(url_params_right + 'ret.npy')
        K_right = np.load(url_params_right + 'K.npy')
        dist_right = np.load(url_params_right + 'dist.npy')

        # Get height and width. Note: It assumes that both pictures are the same size. They HAVE to be same size
        h, w = img_right.shape[:2]
        # print(h, w)

        # Get optimal camera matrix for better undistortion
        new_camera_matrix_left, roi_left = cv2.getOptimalNewCameraMatrix(K_left, dist_left, (w, h), 1, (w, h))
        new_camera_matrix_right, roi_right = cv2.getOptimalNewCameraMatrix(K_right, dist_right, (w, h), 1, (w, h))

        # Undistort images
        img_left_undistorted = cv2.undistort(img_left, K_left, dist_left, None, new_camera_matrix_left)
        img_right_undistorted = cv2.undistort(img_right, K_right, dist_right, None, new_camera_matrix_right)

        # Downsample each image 3 times (because they're too big)
        img_left_downsampled = self.downsample_image(img_left_undistorted, 0)
        img_right_downsampled = self.downsample_image(img_right_undistorted, 0)

        # Set disparity parameters
        # Note: disparity range is tuned according to specific parameters obtained through trial and error.
        #win_size = 5
        #min_disp = -1
        #max_disp = 63  # min_disp * 9
        num_disp = max_disp - min_disp  # Needs to be divisible by 16

        # Create Block matching object.
        stereo = cv2.StereoSGBM_create(minDisparity=min_disp,
                                       numDisparities=num_disp,
                                       blockSize=blockSize,
                                       uniquenessRatio=10,
                                       speckleWindowSize=0,
                                       speckleRange=2,
                                       disp12MaxDiff=2,
                                       P1=8 * 3 * win_size ** 2,  # 8*3*win_size**2,
                                       P2=32 * 3 * win_size ** 2)  # 32*3*win_size**2)

        # Compute disparity map
        #print("\nComputing the disparity  map...")
        disparity_map = stereo.compute(img_left_downsampled, img_right_downsampled)
        img_disparity_map = self.matrix_to_image(disparity_map)

        return img_disparity_map

    def stereo_3D_reconstruction_real_time(self, url_folder="./ejemplos/example_9/", left_cam = 1, right_cam = 2,  img_left=0, img_right=0, disparity_map=None, ffl=0.00001):
        "Este método realiza la reconstrucción de una escena 3D con base en un conjunto de imágene de la misma"
        "Recibe la URL dnde están guardados los parámetros de cámara y la URL de las imágenes"
        "Entrega la escena reconstruida"

        url_params_left = url_folder + "params_cam_left/"
        url_params_right = url_folder + "params_cam_right/"

        # Load camera parameters
        ret_left = np.load(url_params_left + 'ret.npy')
        K_left = np.load(url_params_left + 'K.npy')
        dist_left = np.load(url_params_left + 'dist.npy')

        ret_right = np.load(url_params_right + 'ret.npy')
        K_right = np.load(url_params_right + 'K.npy')
        dist_right = np.load(url_params_right + 'dist.npy')

        # Get height and width. Note: It assumes that both pictures are the same size. They HAVE to be same size
        h, w = img_right.shape[:2]
        # print(h, w)

        # Get optimal camera matrix for better undistortion
        new_camera_matrix_left, roi_left = cv2.getOptimalNewCameraMatrix(K_left, dist_left, (w, h), 1, (w, h))
        new_camera_matrix_right, roi_right = cv2.getOptimalNewCameraMatrix(K_right, dist_right, (w, h), 1, (w, h))

        # Undistort images
        img_left_undistorted = cv2.undistort(img_left, K_left, dist_left, None, new_camera_matrix_left)
        img_right_undistorted = cv2.undistort(img_right, K_right, dist_right, None, new_camera_matrix_right)

        # Downsample each image 3 times (because they're too big)
        img_left_downsampled = self.downsample_image(img_left_undistorted, 0)
        img_right_downsampled = self.downsample_image(img_right_undistorted, 0)

        # Compute disparity map
        print("\nComputing the disparity map...")
        img_disparity_map = self.matrix_to_image(disparity_map)

        print("Cierre la ventana para continuar")

        # Show disparity map before generating 3D cloud to verify that point cloud will be usable.
        #cv2.imshow('Disparity Map', img_disparity_map)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        #plt.imshow(disparity_map, 'gray')
        #plt.savefig("disparity.png")
        #plt.show()

        # Generate  point cloud.
        print("\nGenerating the 3D map...")

        # Get new downsampled width and height
        h, w = img_right_downsampled.shape[:2]

        #print(K_left[0,0], K_left[1,1], K_right[0,0], K_right[1,1])

        focal_length = (K_left[0,0]+K_left[1,1]+K_right[0,0]+K_right[1,1])/4

        # Load focal length.
        #focal_length = np.load('./camera_params/FocalLength.npy')

        # Perspective transformation matrix
        # This transformation matrix is from the openCV documentation, didn't seem to work for me.
        Q = np.float32([[1, 0, 0, -w / 2.0],
                        [0, -1, 0, h / 2.0],
                        [0, 0, 0, -focal_length*0.001],
                        [0, 0, 1, 0]])

        # This transformation matrix is derived from Prof. Didier Stricker's power point presentation on computer vision.
        # Link : https://ags.cs.uni-kl.de/fileadmin/inf_ags/3dcv-ws14-15/3DCV_lec01_camera.pdf
        Q2 = np.float32([[1, 0, 0, -w / 2.0],
                         [0, -1, 0, h / 2.0],
                         [0, 0, focal_length*ffl, 0],  # Focal length multiplication obtained experimentally.
                         [0, 0, 0, 1]])

        # Reproject points into 3D
        points_3D = cv2.reprojectImageTo3D(disparity_map, Q2)
        # Get color points
        colors = cv2.cvtColor(img_right_downsampled, cv2.COLOR_BGR2RGB)

        # Get rid of points with value 0 (i.e no depth)
        mask_map = disparity_map > disparity_map.min()
        #mask_map = disparity_map

        # Mask colors and points.
        output_points = points_3D[mask_map]
        output_colors = colors[mask_map]

        # Define name for output file
        path_folder = os.getcwd()
        output_file = 'reconstructed.ply'

        # Generate point cloud
        print("\n Creating the output file... \n")
        self.create_output(output_points, output_colors, output_file)

    def stereo_3D_reconstruction(self):
        "Este método realiza la reconstrucción de una escena 3D con base en un conjunto de imágene de la misma"
        "Recibe la URL dnde están guardados los parámetros de cámara y la URL de las imágenes"
        "Entrega la escena reconstruida"


        # Load camera parameters
        ret_0 = np.load('./ejemplos/example_9/cam_0_params/ret.npy')
        K_0 = np.load('./ejemplos/example_9/cam_0_params/K.npy')
        dist_0 = np.load('./ejemplos/example_9/cam_0_params/dist.npy')

        ret_1 = np.load('./ejemplos/example_9/cam_1_params/ret.npy')
        K_1 = np.load('./ejemplos/example_9/cam_1_params/K.npy')
        dist_1 = np.load('./ejemplos/example_9/cam_1_params/dist.npy')

        # Specify image paths
        img_path1 = './ejemplos/nube2/image_0.jpg'
        img_path2 = './ejemplos/nube1/image_0.jpg'

        # Load pictures
        img_0 = cv2.imread(img_path1)
        img_1 = cv2.imread(img_path2)

        # Get height and width. Note: It assumes that both pictures are the same size. They HAVE to be same size
        h, w = img_1.shape[:2]
        #print(h, w)

        # Get optimal camera matrix for better undistortion
        new_camera_matrix_0, roi_0 = cv2.getOptimalNewCameraMatrix(K_0, dist_0, (w, h), 1, (w, h))
        new_camera_matrix_1, roi_1 = cv2.getOptimalNewCameraMatrix(K_1, dist_1, (w, h), 1, (w, h))

        # Undistort images
        img_0_undistorted = cv2.undistort(img_0, K_0, dist_0, None, new_camera_matrix_0)
        img_1_undistorted = cv2.undistort(img_1, K_1, dist_1, None, new_camera_matrix_1)

        # Downsample each image 3 times (because they're too big)
        img_0_downsampled = self.downsample_image(img_0_undistorted, 0)
        img_1_downsampled = self.downsample_image(img_1_undistorted, 0)

        # Set disparity parameters
        # Note: disparity range is tuned according to specific parameters obtained through trial and error.
        win_size = 1
        min_disp = 0
        max_disp = 16  # min_disp * 9
        num_disp = max_disp - min_disp  # Needs to be divisible by 16

        # Create Block matching object.
        stereo = cv2.StereoSGBM_create(minDisparity=min_disp,
                                       numDisparities=num_disp,
                                       blockSize=2,
                                       uniquenessRatio=5,
                                       speckleWindowSize=5,
                                       speckleRange=5,
                                       disp12MaxDiff=2,
                                       P1=8 * 3 * win_size ** 2,  # 8*3*win_size**2,
                                       P2=32 * 3 * win_size ** 2)  # 32*3*win_size**2)

        # Compute disparity map
        print("\nComputing the disparity  map...")
        disparity_map = stereo.compute(img_0_downsampled, img_1_downsampled)
        img_disparity_map = self.matrix_to_image(disparity_map)

        print("Cierre la ventana para continuar")

        # Show disparity map before generating 3D cloud to verify that point cloud will be usable.
        cv2.imshow('Disparity Map', img_disparity_map)
        cv2.waitKey(0)

        cv2.destroyAllWindows()
        #plt.imshow(disparity_map, 'gray')
        #plt.savefig("disparity.png")
        #plt.show()

        # Generate  point cloud.
        print("\nGenerating the 3D map...")

        # Get new downsampled width and height
        h, w = img_1_downsampled.shape[:2]

        focal_length = (K_0[0,0]+K_0[1,1]+K_1[0,0]+K_1[1,1])/4

        # Load focal length.
        #focal_length = np.load('./camera_params/FocalLength.npy')

        # Perspective transformation matrix
        # This transformation matrix is from the openCV documentation, didn't seem to work for me.
        Q = np.float32([[1, 0, 0, -w / 2.0],
                        [0, -1, 0, h / 2.0],
                        [0, 0, 0, -focal_length],
                        [0, 0, 1, 0]])

        # This transformation matrix is derived from Prof. Didier Stricker's power point presentation on computer vision.
        # Link : https://ags.cs.uni-kl.de/fileadmin/inf_ags/3dcv-ws14-15/3DCV_lec01_camera.pdf
        Q2 = np.float32([[1, 0, 0, 0],
                         [0, -1, 0, 0],
                         [0, 0, focal_length * 0.0001, 0],  # Focal length multiplication obtained experimentally.
                         [0, 0, 0, 1]])

        # Reproject points into 3D
        points_3D = cv2.reprojectImageTo3D(disparity_map, Q2)
        # Get color points
        colors = cv2.cvtColor(img_1_downsampled, cv2.COLOR_BGR2RGB)

        # Get rid of points with value 0 (i.e no depth)
        mask_map = disparity_map > disparity_map.min()
        #mask_map = disparity_map

        # Mask colors and points.
        output_points = points_3D[mask_map]
        output_colors = colors[mask_map]

        # Define name for output file
        output_file = 'reconstructed.ply'

        # Generate point cloud
        print("\n Creating the output file... \n")
        self.create_output(output_points, output_colors, output_file)

    def video_from_camera(self, num_camera=0):
        cap = cv2.VideoCapture(num_camera)
        fps = cap.get(cv2.CAP_PROP_FPS)
        # print(fps)
        # fgbg = cv2.createBackgroundSubtractorMOG2(5, 10, True)

        while (True):

            # Capture frame-by-frame
            ret, frame = cap.read()

            #    cv2.imshow('ndvi4',ndvi4)
            cv2.imshow('original', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        return frame

    def focal_length_from_image(self, path_image):
        "Este método extrae la distancia focal de la información EXIF de una imagen"

        # Get exif data in order to get focal length.
        exif_img = PIL.Image.open(path_image)
        # print(exif_img)
        exif_data = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in exif_img._getexif().items()
            if k in PIL.ExifTags.TAGS}
        # Get focal length in tuple form
        focal_length_exif = exif_data['FocalLength']
        # print(focal_length_exif)
        # Get focal length in decimal form
        focal_length = focal_length_exif[0] / focal_length_exif[1]
        # np.save("./camera_params/FocalLength", focal_length)
        return focal_length

    def video_stabilizer_full(self, video_input="ejemplos/example_1/billarVideo.mp4"):

        cap = cv2.VideoCapture(video_input)

        img_base = cv2.imread("ejemplos/example_1/baseBillar.png")
        img_base = cv2.resize(img_base, (900, 500), interpolation=cv2.INTER_LINEAR)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (900, 500))

        # estabilizador = self.ProyectividadOpenCV()

        while (True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            frame = cv2.resize(frame, (900, 500), interpolation=cv2.INTER_LINEAR)
            estabilizada = self.estabilizador_imagen(frame, img_base)
            out.write(estabilizada)

            # Display the resulting frame
            cv2.imshow('frame', estabilizada)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        out.release()
        cap.release()
        cv2.destroyAllWindows()
        return "Video is ready"

    def ndvi_calculation(self, url_img_RED="ejemplos/example_2/img_RED.TIF",
                         url_img_NIR="ejemplos/example_2/img_NIR.TIF", radio=0.75, error_repro=4):
        """En este método se calcula el índice NDVI a partir de un par de imágenes entregadas en el argumento"""
        print(url_img_RED)
        "Se leen las imágenes"
        #img_RGB = cv2.imread(url_img_RED,cv2.IMREAD_UNCHANGED)
        #print(img_RGB.shape)
        #img_RED = img_RGB[:,:,2]
        img_RED = cv2.imread(url_img_RED, 0)
        #print(img_RED.shape)
        if img_RED is None:
            print("Imagen base no legible")
            return None, None
        stb_NIR = cv2.imread(url_img_NIR, 0)
        if stb_NIR is None:
            print("Imagen NIR no legible")
            return None, None
        #print(stb_NIR.shape)

        #img_RED = cv2.resize(img_RED, (width, height), interpolation=cv2.INTER_LINEAR)
        #stb_NIR = cv2.resize(stb_NIR, (width, height), interpolation=cv2.INTER_LINEAR)

        "Se alinean as imágenes y se utiliza la imagen roja como imagen base"

        stb_RED = self.estabilizador_imagen(img_RED, stb_NIR,radio,error_repro)
        if stb_RED is None:
            return None, None

        "Se convierten las imágenes en arreglos trabajables con numpy y matplotlib"
        red = array(stb_RED, dtype=float)
        nir = array(stb_NIR, dtype=float)

        "Se verifican y corrigen las divisiones por cero"
        check = np.logical_and(red > 1, nir > 1)

        "Se calcula el índice ndvi"
        ndvi = np.where(check, (nir - red) / (nir + red), 0)

        ndvi_index = ndvi

        "Se verifica que todos los valores queden sobre cero"
        if ndvi.min() < 0:
            ndvi = ndvi + (ndvi.min() * -1)

        ndvi = (ndvi * 255) / ndvi.max()
        ndvi = ndvi.round()

        ndvi_image = np.array(ndvi, dtype=np.uint8)

        return ndvi_index, ndvi_image

    def ndvi_calculation_with_H(self, url_img_RED="ejemplos/example_2/img_RED.TIF",
                         url_img_NIR="ejemplos/example_2/img_NIR.TIF", H=None):
        """En este método se calcula el índice NDVI a partir de un par de imágenes entregadas en el argumento"""
        print(url_img_RED)
        "Se leen las imágenes"
        img_RED = cv2.imread(url_img_RED, 0)
        #print(img_RED.shape)
        if img_RED is None:
            print("Imagen base no legible")
            return None, None
        stb_NIR = cv2.imread(url_img_NIR, 0)
        if stb_NIR is None:
            print("Imagen NIR no legible")
            return None, None

        "Se alinean as imágenes y se utiliza la imagen roja como imagen base"

        stb_RED = self.estabilizador_imagen_with_H(img_RED,H)
        if stb_RED is None:
            return None, None

        "Se convierten las imágenes en arreglos trabajables con numpy y matplotlib"
        red = array(stb_RED, dtype=float)
        nir = array(stb_NIR, dtype=float)

        "Se verifican y corrigen las divisiones por cero"
        check = np.logical_and(red > 1, nir > 1)

        "Se calcula el índice ndvi"
        ndvi = np.where(check, (nir - red) / (nir + red), 0)

        ndvi_index = ndvi

        "Se verifica que todos los valores queden sobre cero"
        if ndvi.min() < 0:
            ndvi = ndvi + (ndvi.min() * -1)

        ndvi = (ndvi * 255) / ndvi.max()
        ndvi = ndvi.round()

        ndvi_image = np.array(ndvi, dtype=np.uint8)

        return ndvi_index, ndvi_image

    def image_collection_for_calibration(self, num_camera=1, num_images=15, url_collection="./ejemplos/example_9/"):
        "Este método permite construir un directorio de imágenes de cantidad variable desde una cámara"
        "Recibe numero camara DEF(1), numero de imagenes DEF(15) y URL para guardar imagenes DEF(example_9)"

        "Captura de conjunto de imagenes para calibracion"
        image_list = []

        try:
            os.stat(url_collection)
        except:
            os.mkdir(url_collection)

        url_collection = url_collection + "coll_cam_" + str(num_camera) + "/"
        # Si el directorio no existe, se crea
        try:
            os.stat(url_collection)
        except:
            os.mkdir(url_collection)

        for i in range(num_images):
            frame = self.video_from_camera(num_camera)
            # Crea una carpeta para cada camara
            label_image = url_collection + "image_" + str(i) + ".jpg"
            cv2.imwrite(label_image, frame)
            image_list.append(frame)
            print(str(i) + " image saved from camera " + str(num_camera))
        print("Image collection completed")
        return

    def img_coll_for_two_cams_calibration(self, first_cam=1, second_cam=2, num_images = 15, url_collection="./ejemplos/example_9/"):
        "Este método permite construir un directorio de imágenes de cantidad variable desde dos cámaras al mismo tiempo"
        "Recibe numero camara 1 y número de cámara 2 DEF(1 y 2), numero de imagenes DEF(15) y URL para guardar imagenes DEF(example_9)"

        "Captura de conjunto de imagenes para calibracion"
        image_list_first_cam = []
        image_list_second_cam = []

        try:
            os.stat(url_collection)
        except:
            os.mkdir(url_collection)

        url_collection_first_cam = url_collection + "coll_cam_" + str(first_cam) + "/"
        url_collection_second_cam = url_collection + "coll_cam_" + str(second_cam) + "/"

        # Si el directorio no existe, se crea
        try:
            os.stat(url_collection_first_cam)
        except:
            os.mkdir(url_collection_first_cam)

        try:
            os.stat(url_collection_second_cam)
        except:
            os.mkdir(url_collection_second_cam)

        cap1 = cv2.VideoCapture(first_cam)
        cap2 = cv2.VideoCapture(second_cam)

        #for i in range(num_images):

        img_count = 0

        while (True):

            # Capture frame-by-frame
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()

            #    cv2.imshow('ndvi4',ndvi4)
            cv2.imshow('original1', frame1)
            cv2.imshow('original2', frame2)

            if cv2.waitKey(1) & 0xFF == ord('t'):
                # frame = self.video_from_camera(num_camera)
                # Crea una carpeta para cada camara
                label_image_first = url_collection_first_cam + "image_" + str(img_count) + ".jpg"
                label_image_second = url_collection_second_cam + "image_" + str(img_count) + ".jpg"
                cv2.imwrite(label_image_first, frame1)
                cv2.imwrite(label_image_second, frame2)
                image_list_first_cam.append(frame1)
                image_list_second_cam.append(frame2)
                print(str(img_count) + " image saved from cameras " + str(first_cam) + " and " + str(second_cam))
                img_count = img_count + 1

            if cv2.waitKey(1) & 0xFF == ord('q') or img_count == num_images:
                break

        # When everything done, release the capture
        cap1.release()
        cap2.release()
        cv2.destroyAllWindows()


        print("Image collection completed")
        return image_list_first_cam, image_list_second_cam


    def cam_calibration_with_img_collection(self, url_img_collection="./ejemplos/example_9/",
                                            chessboard_size=(9, 6), num_camera=1, lr_cam="left"):
        "Método para calibracion de camara con colección de imágenes disponible"
        "Recibe el tamaño del tablero y la ruta para la colección de imágenes"
        print("Ingreso a la clase")

        url_folder = url_img_collection

        url_img_collection = url_img_collection + "coll_cam_" + lr_cam + "/"

        try:
            os.stat(url_img_collection)
        except:
            print("Collection does'nt exist")
            return "Collection does'nt exist"

        url_img_collection = url_img_collection + "*"
        # chessboard_size = (9, 6)

        # Define arrays to save detected points
        obj_points = []  # 3D points in real world space
        img_points = []  # 3D points in image plane
        # Prepare grid and points to display
        objp = np.zeros((np.prod(chessboard_size), 3), dtype=np.float32)
        objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

        # read images
        # calibration_paths = glob.glob('/ejemplos/example_9/image_?.jpg')
        calibration_paths = glob.glob(url_img_collection)
        print(len(calibration_paths))
        # Iterate over images to find intrinsic matrix
        for image_path in tqdm(calibration_paths):
            # Load image
            image = cv2.imread(image_path)
            # print(image_path)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            print("Image loaded, Analizying...")
            # find chessboard corners
            ret, corners = cv2.findChessboardCorners(gray_image, chessboard_size, None)
            if ret == True:
                print("Chessboard detected!")
                print(image_path)
                # define criteria for subpixel accuracy
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                # refine corner location (to subpixel accuracy) based on criteria.
                cv2.cornerSubPix(gray_image, corners, (5, 5), (-1, -1), criteria)
                obj_points.append(objp)
                img_points.append(corners)

        ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray_image.shape[::-1], None, None)

        # Save parameters into numpy file
        url_parametros = url_folder + "params_cam_" + lr_cam + "/"

        #Si el directorio no existe, se crea
        try:
            os.stat(url_parametros)
        except:
            os.mkdir(url_parametros)

        #Se guardan los datos de calibración como archivos np para que estén disponibles
        np.save(url_parametros+"ret", ret)
        np.save(url_parametros+"K", K)
        np.save(url_parametros+"dist", dist)
        np.save(url_parametros+"rvecs", rvecs)
        np.save(url_parametros+"tvecs", tvecs)

        final_messaje = "Finished calibration. Outputs folder is: " + url_parametros

        return final_messaje

    def cam_calibration_without_img_collection(self, chessboard_size=(9, 6), num_images=15, num_camera=1,
                                               url_collection="./ejemplos/example_9/cam_"):
        "Este método permite crear la colección de imágenes y hacer la calibración de cámara"
        "Recibe el tamaño del tablero DEF(9X6), la cantidad de imágenes para la colecciónDEF(15) y la cámara a calibrar DEF(1)"
        "Retorna los cinco parámetros de calibración de camara"

        # Creando la collección de imágenes
        print("Paso 1: Creando la collección de imágenes \n")
        print("Siga las instrucciones paso a paso")
        self.image_collection_for_calibration(num_camera, num_images, url_collection)

        # Calibrando la cámara
        print("Paso 2: Calculando parámetros de calibración \n")
        print("Este proceso puede tardar varios segundos")
        ret, K, dist, rvecs, tvecs = self.cam_calibration_with_img_collection(url_collection, chessboard_size,
                                                                              num_camera)

        return ret, K, dist, rvecs, tvecs

    def matrix_to_image(self, mtx):
        "Este método toma un arreglo  en cualquier formato y lo convierte en una imagen para openCV"

        "Se verifica que todos los valores queden sobre cero"
        if mtx.min() < 0:
            mtx = mtx + (mtx.min() * -1)

        mtx = (mtx * 255) / mtx.max()
        mtx = mtx.round()

        final_img = np.array(mtx, dtype=np.uint8)
        return final_img

    def point_cloud_generation(self, focal_length, img_1_downsampled, disparity_map):

        "Este método permite generar una nube de puntos y visualizarla con Open3D"

        # Generate  point cloud.
        print("\nGenerating the 3D map...")

        # Get new downsampled width and height
        h, w = img_1_downsampled.shape[:2]

        #focal_length = (K_0[0, 0] + K_0[1, 1] + K_1[0, 0] + K_1[1, 1]) / 4

        # Load focal length.
        # focal_length = np.load('./camera_params/FocalLength.npy')

        # Perspective transformation matrix
        # This transformation matrix is from the openCV documentation, didn't seem to work for me.
        Q = np.float32([[1, 0, 0, -w / 2.0],
                        [0, -1, 0, h / 2.0],
                        [0, 0, 0, -focal_length],
                        [0, 0, 1, 0]])

        # This transformation matrix is derived from Prof. Didier Stricker's power point presentation on computer vision.
        # Link : https://ags.cs.uni-kl.de/fileadmin/inf_ags/3dcv-ws14-15/3DCV_lec01_camera.pdf
        Q2 = np.float32([[1, 0, 0, 0],
                         [0, -1, 0, 0],
                         [0, 0, focal_length * 0.0001, 0],  # Focal length multiplication obtained experimentally.
                         [0, 0, 0, 1]])

        # Reproject points into 3D
        points_3D = cv2.reprojectImageTo3D(disparity_map, Q2)
        # Get color points
        colors = cv2.cvtColor(img_1_downsampled, cv2.COLOR_BGR2RGB)

        # Get rid of points with value 0 (i.e no depth)
        mask_map = disparity_map > disparity_map.min()
        # mask_map = disparity_map

        # Mask colors and points.
        output_points = points_3D[mask_map]
        output_colors = colors[mask_map]

        # Define name for output file
        output_file = 'reconstructed.ply'

        # Generate point cloud
        print("\n Creating the output file... \n")
        self.create_output(output_points, output_colors, output_file)

    def exif_get_if_exist(self, data, key):
        "Este método verifica la existencia de un dato en el directorio de datos EXIF"
        if key in data:
            return data[key]
        return "no_key"
        
    def lat_lon_from_image(self, path_image):
        "Este método extrae la latitud y longitud de una imagen de la camara sequoia"

        # Get exif data in order to get focal length.
        try:
            # print("Aquí estoy")
            exif_img = PIL.Image.open(path_image)
        except:
            return None

        # print(exif_img)
        exif_data = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in exif_img._getexif().items()
            if k in PIL.ExifTags.TAGS}

        gps_info = self.exif_get_if_exist(exif_data, 'GPSInfo')
        print(gps_info)
        if gps_info == "no_key":
            #print(path_image)
            return "Tag GPSInfo does'nt exist"

        ref_NS = self.exif_get_if_exist(gps_info, 1)
        print(ref_NS)
        if ref_NS == "no_key":
            return "Tag 1 (Nort-South) does'nt exist"

        ref_WE = self.exif_get_if_exist(gps_info, 3)
        if ref_WE == "no_key":
            return "Tag 3 (West-East) does'nt exist"

        dms_NS = self.exif_get_if_exist(gps_info, 2)
        if dms_NS == "no_key":
            return "Tag 2 (West-East) does'nt exist"

        dms_WE = self.exif_get_if_exist(gps_info, 4)
        if dms_WE == "no_key":
            return "Tag 4 (West-East) does'nt exist"

        degress_NS = self.dms_to_degress(dms_NS)

        degress_WE = self.dms_to_degress(dms_WE)

        lat = degress_NS
        lon = degress_WE

        if ref_NS == "S":
            lat = 0-degress_NS

        if ref_WE == "W":
            lon = 0-degress_WE

        return (lat, lon)

        # print(focal_length_exif)
        # Get focal length in decimal form
        #focal_length = focal_length_exif[0] / focal_length_exif[1]
        # np.save("./camera_params/FocalLength", focal_length)
        #return focal_length

    def dms_to_degress(self, value):
        """Este método permite convertir los datos de gps de dias, minutos y segundos a grados"""
        print(type(value))
        if type(value) is tuple:

            d = float(value[0])

            m = float(value[1])

            s = float(value[2])

            return d + (m / 60.0) + (s / 3600.0)

        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)

    def graph_gps_points(self, x, y):
        """Este método permite graficar una nube de puntos"""
        #plt.plot(x)
        plt.scatter(x, y)
        #plt.plot(x, y, 'r--')
        #plt.xticks(6, fecha)
        #plt.savefig('Temperatura 1.png')
        #plt.xlim(2, 50)
        plt.show()

    def image_collection_for_2_cams_calibration(self, num_camera_left=1, num_camera_right=2, num_images=15, url_collection="./ejemplos/example_9/"):
        """Este método permite construir un directorio de imágenes de cantidad variable desde dos cámaras"
        "Recibe numero camara DEF(1), numero de imagenes DEF(15) y URL para guardar imagenes DEF(example_9)"""

        "Captura de conjunto de imagenes para calibracion"
        image_list_left = []
        image_list_right = []

        try:
            os.stat(url_collection)
        except:
            os.mkdir(url_collection)

        url_collection_left = url_collection + "coll_cam_left/"
        # Si el directorio no existe, se crea
        try:
            os.stat(url_collection_left)
        except:
            os.mkdir(url_collection_left)

        url_collection_right = url_collection + "coll_cam_right/"
        # Si el directorio no existe, se crea
        try:
            os.stat(url_collection_right)
        except:
            os.mkdir(url_collection_right)

        for i in range(num_images):
            frame_left, frame_right = self.video_from_2_cameras(num_camera_left, num_camera_right)

            # Crea una etiqueta para cada imagen
            label_image_left = url_collection_left + "image_" + str(i) + ".jpg"
            label_image_right = url_collection_right + "image_" + str(i) + ".jpg"

            cv2.imwrite(label_image_left, frame_left)
            cv2.imwrite(label_image_right, frame_right)

            image_list_left.append(frame_left)
            image_list_right.append(frame_right)

            print(str(i) + " image saved from cameras " + str(num_camera_left) + " and " + str(num_camera_right))
        print("Image collection completed")
        return

    def video_from_2_cameras(self, num_camera_left=1, num_camera_right=2):
        cap1 = cv2.VideoCapture(num_camera_left)
        fps1 = cap1.get(cv2.CAP_PROP_FPS)

        cap2 = cv2.VideoCapture(num_camera_right)
        fps2 = cap2.get(cv2.CAP_PROP_FPS)
        # print(fps)
        # fgbg = cv2.createBackgroundSubtractorMOG2(5, 10, True)

        while (True):

            # Capture frame-by-frame
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()

            #    cv2.imshow('ndvi4',ndvi4)
            cv2.imshow('Camera 1 (I)', frame1)
            cv2.imshow('Camera 2 (D)', frame2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap1.release()
        cap2.release()

        cv2.destroyAllWindows()
        return frame1, frame2

    def interfaz_control_xyz(self):
        #app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QWidget()
        #window = QtWidgets.QMainWindow()
        window.setGeometry(0, 0, 1100, 800)
        window.setWindowTitle("PyQT Tuts!")
        self.btn_serial(window)
        self.labels_camera(window)
        return

    def btn_serial(self, window):
        btn = QtWidgets.QPushButton("Quit", window)
        #btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.clicked.connect(self.close_application)
        btn.resize(100, 100)
        btn.move(100, 100)
        window.show()
        return

    def labels_camera(self, window):
        window.styleSheet('font-size: 30px;')
        window.setMinimumWidth(600)

        layout = QtWidgets.QHBoxLayout
        window.setLayout(layout)

        window.comboBox = QtWidgets.QComboBox()
        window.comboBox.addItem("motif")
        window.comboBox.addItem("Windows")
        window.comboBox.addItem("cde")
        window.comboBox.addItem("Plastique")
        window.comboBox.addItem("Cleanlooks")
        window.comboBox.addItem("windowsvista")
        layout.addWidget(window.comboBox)

        #window.comboBox.move(50, 250)

        #window.styleChoice.move(50, 150)
        #window.comboBox.activated[str].connect(window.style_choice)
        window.show()
        return

    def close_application(self):
        print("whooaaaa so custom!!!")
        sys.exit()

    def tracking_coordenadas(self, camara):
        cap1 = cv2.VideoCapture(camara)
        while True:
            ret1, frame1 = cap1.read()

            #segmentacion de circulos rojos
            hsv_original = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

            redBajo1 = np.array([0, 100, 20], np.uint8)
            redAlto1 = np.array([8, 255, 255], np.uint8)

            redBajo2 = np.array([175, 100, 20], np.uint8)
            redAlto2 = np.array([179, 255, 255], np.uint8)

            maskRed1 = cv2.inRange(hsv_original, redBajo1, redAlto1)
            maskRed2 = cv2.inRange(hsv_original, redBajo2, redAlto2)
            maskRed = cv2.add(maskRed1, maskRed2)

            #Eliminar ruido
            kernel = np.ones((3, 3), np.uint8)
            bolas = cv2.morphologyEx(maskRed, cv2.MORPH_OPEN, kernel)
            bolas = cv2.morphologyEx(maskRed, cv2.MORPH_CLOSE, kernel)

            #Encontrar contornos
            contours, _ = cv2.findContours(bolas, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bolas)

            valor_max_pix = (np.max(stats[:4][1:])) / 2
            pin = np.where((stats[:, 4][1:]) > valor_max_pix)
            pin = pin[0] + 1

            coordenadas_x = np.array([centroids[pin[0]][0],centroids[pin[1]][0],centroids[pin[2]][0],centroids[pin[3]][0]], np.uint8)
            coordenadas_y = np.array(
                [centroids[pin[0]][1], centroids[pin[1]][1], centroids[pin[2]][1], centroids[pin[3]][1]], np.uint8)

            centro_x = np.max(coordenadas_x)-np.min(coordenadas_x)
            centro_y = np.max(coordenadas_y)-np.min(coordenadas_y)

            centroids=np.array(centroids[pin])

            centroids=centroids[centroids[:,0].argsort()]

            if centroids[0][1]<centroids[1][1]:
                ref_1 = centroids[0]
                ref_2 = centroids[1]
            else:
                ref_2 = centroids[0]
                ref_1 = centroids[1]

            if centroids[2][1]<centroids[3][1]:
                ref_3 = centroids[2]
                ref_4 = centroids[3]
            else:
                ref_4 = centroids[2]
                ref_3 = centroids[3]

            las_xprima = np.array([ref_1,ref_2,ref_3,ref_4])

            las_x = np.array([(0, 0), (0, 300), (300, 0), (300, 300)])

            H, estado = cv2.findHomography(las_xprima, las_x, cv2.RANSAC, 0.01)

            rectificada = cv2.warpPerspective(frame1, H,
                                              (int(1.5 * frame1.shape[1]),
                                               int(1.5 * frame1.shape[0])))

            redBajo1 = np.array([0, 0, 200], np.uint8)
            redAlto1 = np.array([25, 150, 255], np.uint8)

            redBajo2 = np.array([170, 0, 200], np.uint8)
            redAlto2 = np.array([179, 20, 255], np.uint8)

            hsv_rectificada = cv2.cvtColor(rectificada, cv2.COLOR_BGR2HSV)
            maskRed1 = cv2.inRange(hsv_rectificada, redBajo1, redAlto1)
            maskRed2 = cv2.inRange(hsv_rectificada, redBajo2, redAlto2)
            maskRed = cv2.add(maskRed1, maskRed2)

            # Eliminar ruido
            kernel = np.ones((3, 3), np.uint8)
            bolas = cv2.morphologyEx(maskRed1, cv2.MORPH_OPEN, kernel)
            bolas = cv2.morphologyEx(maskRed1, cv2.MORPH_CLOSE, kernel)

            # Encontrar contornos
            contours, _ = cv2.findContours(bolas, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            #cv2.drawContours(rectificada, contours, -1, (0, 255, 0), 2)

            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bolas)
            #print(stats)
            #print(labels)
            #print(centroids)
            #print(np.max(stats[:4][1:]))

            valor_max_pix = (np.max(stats[:4][1:])) /2


            try:
                pin = np.where((stats[:,4][1:]) > valor_max_pix)
                pin = pin[0] + 1
                #print(pin)
                centroids = np.array(centroids[pin])
                print(centroids[0][0])
                cv2.circle(rectificada, (int(centroids[0][0]), int(centroids[0][1])), 5, (0, 0, 255), 5, 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(rectificada, (str(centroids[0][0]) + " " + str(centroids[0][1])), (int(centroids[0][0]), int(centroids[0][1])), font,
                            1, (0, 0, 255), 2, cv2.LINE_AA)
            except:
                print("No se encuentra el laser")

            cv2.namedWindow("Original")
            cv2.imshow("Original", frame1)


            cv2.namedWindow("Circ")
            cv2.imshow("Circ", rectificada)

            cv2.namedWindow("Circulos")
            cv2.imshow("Circulos", maskRed1)
            #cv2.waitKey(0)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

        return

    """
    # Clonar la imagen original para poder escribir sobre ella
        # sin modificarla
        imagen_conpuntos = frame1

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
                imagen_conpuntos = img.copy()

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
                    cv2.putText(imagen_conpuntos, str(pts_id + 1), (x, y), font,
                                4, (0, 0, 255), 2, cv2.LINE_AA)

        las_xprima = np.array(puntos_click)

        las_x = np.array([(0, 0), (0, 300), (300, 0), (300, 300)])

        H, estado = cv2.findHomography(las_xprima, las_x, cv2.RANSAC, 0.01)

        rectificada = cv2.warpPerspective(img, H,
                                          (int(1.5 * img.shape[1]),
                                           int(1.5 * img.shape[0])))

        puntos_click = list()

        # Clonar la imagen original para poder escribir sobre ella
        # sin modificarla
        # Mostrar la imagen

        cv2.namedWindow("Rectificada")
        cv2.imshow("Rectificada", rectificada)

        cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

        # cv2.imshow('detected circles', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        while True:
            ret1, frame1 = cap1.read()
            image1 = frame1
            img = image1

            rectificada = cv2.warpPerspective(img, H,
                                              (int(1.5 * img.shape[1]),
                                               int(1.5 * img.shape[0])))

            redBajo1 = np.array([0, 0, 200], np.uint8)
            redAlto1 = np.array([8, 8, 255], np.uint8)

            redBajo2 = np.array([165, 0, 200], np.uint8)
            redAlto2 = np.array([179, 8, 255], np.uint8)

            maskLaserBajo = np.array([150, 0, 20], np.uint8)
            maskLaserAlto = np.array([179, 100, 255], np.uint8)

            hsv_rectificada = cv2.cvtColor(rectificada, cv2.COLOR_BGR2HSV)
            maskRed1 = cv2.inRange(hsv_rectificada, redBajo1, redAlto1)
            maskRed2 = cv2.inRange(hsv_rectificada, redBajo2, redAlto2)
            maskRed = cv2.add(maskRed1, maskRed2)
            laserMaskRed = cv2.inRange(hsv_rectificada, maskLaserBajo, maskLaserAlto)

            cv2.namedWindow("Rectificada")
            cv2.imshow("Rectificada", maskRed)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        """

        
def main():
    print("\n Computer Vision Class by Jorge Martínez \n \n")
    print("Type 1 for Video Stabilizer example \n")
    print("Type 2 for Photogrametric Alignment example \n")
    print("Type 3 for NDVI example \n")
    print("Type 4 for camera test\n")
    print("Example 5 is in construction\n")
    print("Introduzca 6 para hacer una reconstrucción estereoscópica a partir de dos imágens\n")
    print("Introduzca 7 para visualizar un mapa de disparidad en tiempo real (necesita dos cámaras enfocando la misma escena\n)")
    print("Introduzca 8 para hacer la calibración de una cámara (debe contar con el patrón de calibración impreso)\n")
    print("Introduzca 9 para crear una colección de imágenes y almacenarla en una carpeta\n")
    print("Introduzca 11 para hacer una colección de imágenes desde dos cámaras y almacenarlas en una carpeta\n")
    print("Introduzca 12 para extraer la información GPS de la metadata de una imagen y convertirla a formato latitud y longitud\n")
    print("Introduzca 13 para extraer las coordenadas GPS de la metadata de un conjunto de imàgenes y graficarlas en un plano cartesiano\n")
    print("Introduzca 14 para generar un conjunto de imágenes NDVI de una vcarpeta con imágenes de cámara sequoia\n")
    print("Introduzca ...\n")

    ejemplo = input()

    #Ejemplo estable para estabilizador de video or software
    if ejemplo == "1":
        "Ejemplo estable para hacer estabilización de video"
        print("Descargue el video billarVideo.mp4, ubíquelo en la carpeta ejemplos/example_1 y oprima enter\n")
        print("\nType Ok to verify")
        url_video_input = input()

        example_1 = ProyectividadOpenCV()
        print("Este proceso puede tardar varios minutos dependiendo del tamaño del video")
        print("El tamaño al que se redimencioann todos los videos por defecto es 700X500 \n")
        video_stabilizer = example_1.video_stabilizer_full()
        print("Trabajo finalizado, el video estabilizado puede encontrarse en la carpeta VisionPC junto a la clase")

    elif ejemplo == "19":
        app = QtWidgets.QApplication(sys.argv)
        example_19 = ProyectividadOpenCV()
        GUI = example_19.interfaz_control_xyz()
        sys.exit(app.exec_())

    elif ejemplo == "30":
        example_30 = ProyectividadOpenCV()
        example_30.tracking_coordenadas(1)


    #**Ejemplo estable para alineación fotogramétrica de las imágenes Sequoia
    elif ejemplo == "2":
        "Ejemplo estable para hacer alineación fotogramétrica de imágenes"
        print("Comenzado proceso con imágenes de prueba propias \n")
        print(
            "Por favor ingrese ancho y alto deseado para las imágenes \npor ejemplo 700,500. De no asignarlos, los valores por defecto serán 700X500 \n \n")
        print("Ancho=")
        width_str = input()
        print("Alto=")
        height_str = input()

        width = int(width_str)
        height = int(height_str)

        example_2 = ProyectividadOpenCV()

        path_folder = os.getcwd()

        img_RGB = cv2.imread(path_folder + "/ejemplos/example_2/img_RGB.JPG", 0)
        img_GRE = cv2.imread(path_folder + "/ejemplos/example_2/img_GRE.TIF", 0)
        img_NIR = cv2.imread(path_folder + "/ejemplos/example_2/img_NIR.TIF", 0)
        img_RED = cv2.imread(path_folder + "/ejemplos/example_2/img_RED.TIF", 0)
        img_REG = cv2.imread(path_folder + "/ejemplos/example_2/img_REG.TIF", 0)

        merged_fix_bad = cv2.merge((img_GRE, img_RED, img_NIR))
        merged_fix_bad = cv2.resize(merged_fix_bad, (width, height), interpolation=cv2.INTER_LINEAR)

        stb_RGB, stb_GRE, stb_NIR, stb_RED, stb_REG = example_2.img_alignment_sequoia(img_RGB, img_GRE, img_NIR,
                                                                                      img_RED, img_REG, width, height)

        merged_fix_stb = cv2.merge((stb_GRE, stb_RED, stb_NIR))

        print(
            "La primera imagen que se genera simplemente superpone las imágenes sin alinear \n Cerrar la ventana para continuar \n")
        cv2.imshow('frame', merged_fix_bad)
        cv2.waitKey(0)

        print("La siguiente imagen si se encuentra debidamente alineada. Cerrar la ventana para terminar")
        cv2.imshow('frame', merged_fix_stb)
        cv2.waitKey(0)

        cv2.destroyAllWindows()

    #**Ejemplo estable para generar imagen NDVI con NIR y RED
    elif ejemplo == "3":
        "Ejemplo estable para generar imagen NDVI"
        print("Se construye el objeto")
        example_3 = ProyectividadOpenCV()

        path_folder = os.getcwd()

        print("Para este ejemplo se utilizará el mismo conjunto de imágenes del ejemplo 2")
        url_img_RED = path_folder + "/ejemplos/example_2/img_RED.TIF"
        url_img_NIR = path_folder + "/ejemplos/example_2/img_NIR.TIF"

        "Se envían las URL y se obtienen los índices NDVI y una imagen adecuada para visualizar"

        ndvi_index, ndvi_image = example_3.ndvi_calculation(url_img_RED, url_img_NIR, 4, 9)

        if ndvi_image is not None:
            "Se pinta la imagen con colormap de OpenCV. En mi caso, RAINBOW fue la mejor opción"
            im_color = cv2.applyColorMap(ndvi_image, cv2.COLORMAP_RAINBOW)

            print(ndvi_index)

            cv2.imshow('frame', im_color)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            print("Cerrar la ventana para finalizar")

        else:
            print("No se puedo completar la operación")

    #Ejemplo de prueba para abrir cámaras del pc (Se ingresa el número de cámara a visualizar)
    elif ejemplo == "4":
        "Ejemplo de prueba para abrir cámaras en el PC"

        print("Digite el numero de camara que desea visualizar")
        num_camera = input()

        example_4 = ProyectividadOpenCV()
        example_4.video_from_camera(int(num_camera))

    #Ejemplo estable para generar la imagen 3D
    elif ejemplo == '5':
        """Ejemplo para ejecutar el proceso de generación de la imagen 3D completo
            configuración sugerida:
            - ffd: 0.00001
            - 7
            -1
            15
            4"""

        print("Paso 1: lectura de imágenes desde cámaras")
        example_5 = ProyectividadOpenCV()

        print("Paso 2: calibración de cámara \n")
        print("¿Las cámaras están calibradas (y/n)? \n")
        var = input()
        if var == 'n':
            print("Generando colección de imágenes para calibración \n")
            print("Ingrese la cantidad de imágenes que desea")

            image_quantity = input()
            print("\nType num camera left")
            num_camera_left = input()

            print("\nType num camera right")
            num_camera_right = input()

            print("\nType folder name")
            folder_name = input()

            path_folder = os.getcwd()

            url_collection = path_folder + "/ejemplos/" + str(folder_name) + "/"
            example_5.image_collection_for_2_cams_calibration(int(num_camera_left), int(num_camera_right), int(image_quantity), url_collection)

            print("\n Calibrando cámara Izquierda:")

            url_folder = path_folder + "/ejemplos/" + folder_name + "/"

            calibrationl = example_5.cam_calibration_with_img_collection(url_folder, (6, 4), int(num_camera_left), "left")
            print(calibrationl)

            print("\n Calibrando cámara Derecha:")

            calibrationr = example_5.cam_calibration_with_img_collection(url_folder, (6, 4), int(num_camera_right), "right")
            print(calibrationr)

            cap_left = cv2.VideoCapture(int(num_camera_left))

            cap_right = cv2.VideoCapture(int(num_camera_right))

            while (True):

                # Capture frame-by-frame
                ret_left, frame_left = cap_left.read()
                ret_right, frame_right = cap_right.read()

                disparity_map = example_5.disparity_map(url_folder, int(num_camera_left), int(num_camera_right),
                                                        frame_left, frame_right)

                cv2.imshow('Disparity Map', disparity_map)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # When everything done, release the capture
            cap_left.release()
            cap_right.release()
            cv2.destroyAllWindows()

        elif var == 'y':
            #print("Type ffl")
            #ffl = float(input())
            #print("Type win_size")
            #win_size = int(input())
            #print("Type min_disp")
            #min_disp = int(input())
            #print("Type max_disp")
            #max_disp = int(input())  # min_disp * 9 63
            #print("Type blockSize")
            #blockSize = int(input())

            ffl = 0.00001
            win_size = 7
            min_disp = -1
            max_disp = 15
            blockSize = 4

            print("\nType num camera left")
            num_camera_left = input()

            print("\nType num camera right")
            num_camera_right = input()

            print("\nType folder name")
            folder_name = input()

            path_folder = os.getcwd()

            url_folder = path_folder + "/ejemplos/" + folder_name + "/"

            cap_left = cv2.VideoCapture(int(num_camera_left))

            cap_right = cv2.VideoCapture(int(num_camera_right))

            while (True):

                # Capture frame-by-frame
                ret_left, frame_left = cap_left.read()
                ret_right, frame_right = cap_right.read()

                disparity_map = example_5.disparity_map(url_folder, int(num_camera_left), int(num_camera_right),
                                                        frame_left, frame_right, win_size, min_disp, max_disp, blockSize)

                cv2.imshow('Disparity Map', disparity_map)

                if cv2.waitKey(1) & 0xFF == ord('m'):
                    #cv2.destroyAllWindows()
                    #cap_left.release()
                    #cap_right.release()
                    print("Select an option")
                    option=input()
                    if option == 'm':
                        #cv2.destroyAllWindows()

                        print("Type ffl")
                        ffl = float(input())
                        print("Type win_size")
                        win_size = int(input())
                        print("Type min_disp")
                        min_disp = int(input())
                        print("Type max_disp")
                        max_disp = int(input())  # min_disp * 9 63
                        print("Type blockSize")
                        blockSize=int(input())

                    elif option == 'g':
                        #cv2.destroyAllWindows()
                        example_5.stereo_3D_reconstruction_real_time(url_folder, int(num_camera_left),
                                                                     int(num_camera_right),
                                                                     frame_left, frame_right, disparity_map, ffl)
                        cloud = o3d.io.read_point_cloud(path_folder + "/reconstructed.ply")  # Read the point cloud
                        o3d.visualization.draw_geometries([cloud])  # Visualize the point cloud

                    else:
                        cap_left.release()
                        cap_right.release()
                        cv2.destroyAllWindows()
                        break

            # When everything done, release the capture

        else:
            print("Opción incorrecta")

    #**Ejemplo estable para reconstrucción de imagen 3D con cámaras calibradas e imágenes guardadas previamente
    elif ejemplo == '6':
        "Ejemplo estable para reconstrución estereoscópica"
        example_6 = ProyectividadOpenCV()
        example_6.stereo_3D_reconstruction()

        cloud = o3d.io.read_point_cloud("reconstructed.ply")  # Read the point cloud
        o3d.visualization.draw_geometries([cloud])  # Visualize the point cloud

    #**Ejemplo estable para visualizar el mapa de disparidad con dos cámaras en tiemo real (estar seguro del número de la cámara)
    elif ejemplo == '7':
        "Ejemplo estable para calcular y visualiar mapa de disparidad en tiempo real"

        example_7 = ProyectividadOpenCV()

        print("Type folder name")
        folder_name = input()

        if folder_name == '':
            folder_name == 'example_9'

        print("Type cam left number")
        cam_left_number = input()

        if cam_left_number == '':
            print("Please type a correct number")
            return

        print("Type cam right number")
        cam_right_number = input()

        if cam_right_number == '':
            print("Please type a correct number")
            return

        cap_left = cv2.VideoCapture(int(cam_left_number))

        cap_right = cv2.VideoCapture(int(cam_right_number))

        fps = cap_left.get(cv2.CAP_PROP_FPS)

        url_folder = "./ejemplos/" + folder_name + "/"

        while (True):

            # Capture frame-by-frame
            ret_left, frame_left = cap_left.read()
            ret_right, frame_right = cap_right.read()

            disparity_map = example_7.disparity_map(url_folder, int(cam_left_number), int(cam_right_number), frame_left, frame_right)

            cv2.imshow('Disparity Map', disparity_map)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap_left.release()
        cap_right.release()
        cv2.destroyAllWindows()

    #**Ejemplo estable para realizar la calibración de cámara teniendo la colección de imágenes previamente guardadas
    elif ejemplo == "8":
        "Ejemplo estable para Calibracion de camara"
        print("Camera calibration\n")

        example_8 = ProyectividadOpenCV()

        print("Type folder name")
        folder_name = input()

        if folder_name == '':
            folder_name == 'example_9'

        print("Type cam number")
        cam_number = input()

        if cam_number == '':
            cam_number = 1

        url_folder = "./ejemplos/" + folder_name + "/"
        calibration = example_8.cam_calibration_with_img_collection(url_folder, (6, 4), cam_number)
        print(calibration)

    #**Ejemplo estable para crear colecciones imágenes y guardarlas en alguna carpeta del pc (para calibración de cámara)
    elif ejemplo == '9':

        "Ejemplo estable permite crear una coleccion de imágenes y guardarlas en la carpeta"

        example_9 = ProyectividadOpenCV()
        print("Type image quantity what you want:\n")
        image_quantity = input()
        print("\nType num camera")
        num_camera = input()
        print("\nType folder name")
        folder_name = input()
        url_collection = "./ejemplos/" + str(folder_name) + "/"
        example_9.image_collection_for_calibration(int(num_camera), int(image_quantity), url_collection)

    #Ejemplo estable para proyectar dos cámaras al mismo tiempo
    elif ejemplo == '10':
        """Ejemplo estable parsa proyectar dos cámaras al mismo tiempo"""

        cap1 = cv2.VideoCapture(1)
        cap2 = cv2.VideoCapture(2)

        #fps = cap.get(cv2.CAP_PROP_FPS)
        # print(fps)
        # fgbg = cv2.createBackgroundSubtractorMOG2(5, 10, True)

        while (True):

            # Capture frame-by-frame
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()

            #    cv2.imshow('ndvi4',ndvi4)
            cv2.imshow('original1', frame1)
            cv2.imshow('original2', frame2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap1.release()
        cap2.release()
        cv2.destroyAllWindows()

    #Ejemplo estable permite crear una coleccion de imágenes desde dos cámaras y guardarlas en la carpeta
    elif ejemplo == '11':
        "Ejemplo estable permite crear una coleccion de imágenes desde dos cámaras y guardarlas en la carpeta"

        example_9 = ProyectividadOpenCV()
        print("Type image quantity what you want:\n")
        image_quantity = input()
        print("\nType first camera number")
        first_camera = input()
        print("\nType second camera number")
        second_camera = input()
        print("\nType folder name")
        folder_name = input()
        url_collection = "./ejemplos/" + str(folder_name) + "/"
        img_list = example_9.img_coll_for_two_cams_calibration(int(first_camera), int(second_camera), int(image_quantity), url_collection)

    # **Ejemplo estable para extraer las coordenadas Latitud y Longitud de las etiquetas exif de una imagen
    elif ejemplo == '12':
        print("Extrayendo TAGS \n")
        example_12 = ProyectividadOpenCV()
        path_folder = os.getcwd()
        url_img = path_folder + "/ejemplos/example_2/img_RGB.JPG"
        # url_img = "/Users/jorgeluismartinezvalencia/Dropbox/UTP/PycharmProjects/stereo_measure/visionPC/ejemplos/example_2/img_RGB.JPG"
        lat_lon = example_12.lat_lon_from_image(url_img)
        print(lat_lon)

    # **Ejemplo estable para graficar la nube de puntos de las ubicaciones de las fotografías.
    elif ejemplo == '13':
        lat_lon = []
        example_13 = ProyectividadOpenCV()
        path_folder = os.getcwd()
        ruta = path_folder + "/ejemplos/convertirNDVI/*.JPG"
        for name in glob.glob(ruta):
            a = example_13.lat_lon_from_image(name)
            if type(a) is tuple:
                lat_lon.append(a)
                print(a)
            # print(name)
        # nombres = glob.glob('ejemplos/0007/*.jpg')
        # print(lat_lon[0][0])
        arreglo = np.array(lat_lon)
        # print(arreglo.shape)
        x = arreglo.T[0]
        y = arreglo.T[1]
        example_13.graph_gps_points(x, y)

    # Ejemplo estable para calcular imágenes NDVI de una carpeta con imágenes etiquetadas Sequpoia (hay que entregar H)
    elif ejemplo == '14':
        # print("Ejemplo 14 seleccionado")
        example_14 = ProyectividadOpenCV()
        exitos = []
        # file_path = "ejemplos/0007"
        path_folder = os.getcwd()
        ruta = path_folder + "/ejemplos/convertirNDVI/*.JPG"
        # ruta = path_folder + "/ejemplos/convertirNDVI/IMG_191115_163840_0001_*.JPG"
        # print(ruta)
        # IMG_200803_165240_0440_NDVI.png
        # for name in os.path.join(ruta_mac, '/*.JPG'):
        for name in glob.glob(str(ruta)):
            # print(name)
            st_img = True
            img_RGB = name
            img_NIR = glob.glob(img_RGB[0:-19] + "*" + img_RGB[-12:-7] + "NIR.TIF")[0]
            img_REG = img_RGB[0:-7] + "REG.TIF"
            img_RED = glob.glob(img_RGB[0:-19] + "*" + img_RGB[-12:-7] + "RED.TIF")[0]
            img_GRE = img_RGB[0:-7] + "GRE.TIF"
            img_NDVI = img_RGB[0:-7] + "NDVI.png"
            try:
                # print("Aquí estoy")
                os.stat(img_NIR)
            except:
                st_img = False
                print("Imagen NIR no legible")

            if st_img == True:
                # print("ejecutando...")

                H = np.array([[1.00520482e+00, - 6.59338125e-03, - 1.08229636e+01],
                              [8.42019665e-03, 1.00417154e+00, - 3.80836118e+01],
                              [1.58625362e-06, - 1.99225479e-06, 1.00000000e+00]])

                ndvi_index, ndvi_image = example_14.ndvi_calculation_with_H(img_RED, img_NIR, H)

                if ndvi_image is not None:
                    im_color = cv2.applyColorMap(ndvi_image, cv2.COLORMAP_RAINBOW)
                    cv2.imwrite(img_NDVI, im_color)
                    print("Operacion exitosa")
                    exitos.append(name)

        print("Terminado...")
        print(exitos)
        print(len(exitos))

    # Ejemplo estable para mostrar una panorámica de dos cámaras en tiempo real
    elif ejemplo == '15':
        """Ejemplo estable para mostrar una panorámica de dos cámaras en tiempo real"""

        example_15 = ProyectividadOpenCV()

        cap1 = cv2.VideoCapture(1)
        cap2 = cv2.VideoCapture(2)

        # fps = cap.get(cv2.CAP_PROP_FPS)
        # print(fps)
        # fgbg = cv2.createBackgroundSubtractorMOG2(5, 10, True)

        while (True):

            # Capture frame-by-frame
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()

            panoramica, coincidencias = example_15.coser_imagenes(frame2, frame1, 0.5, 2)

            if panoramica is not None:
                cv2.imshow('Panoramica', panoramica)
                cv2.imshow('Coincidencias', coincidencias)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap1.release()
        cap2.release()
        cv2.destroyAllWindows()

    elif ejemplo == '16':
        cap1 = cv2.VideoCapture(2)
        cap2 = cv2.VideoCapture(0)
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        image1 = frame1
        image2 = frame2
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        canny1 = cv2.Canny(gray1, 230, 235)
        canny1 = cv2.dilate(canny1, None, iterations=1)
        canny1 = cv2.erode(canny1, None, iterations=1)

        images = np.hstack((gray1, canny1))

        # Display the resulting frame
        cv2.imshow('Frame', images)
        cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

        canny2 = cv2.Canny(gray2, 100, 150)
        canny2 = cv2.dilate(canny2, None, iterations=1)
        canny2 = cv2.erode(canny2, None, iterations=1)
        # _, th = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        # _,cnts,_ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# OpenCV 3
        cnts1, _ = cv2.findContours(canny1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # OpenCV 4
        cnts2, _ = cv2.findContours(canny2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # OpenCV 4
        cv2.drawContours(image1, cnts1, 4, (0,255,0), 2)
        for c in cnts1:
            epsilon = 0.01 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            # print(len(approx))
            x, y, w, h = cv2.boundingRect(approx)
            #if len(approx) == 3:
            #    cv2.putText(image1, 'Triangulo', (x, y - 5), 1, 1.5, (0, 255, 0), 2)
            if len(approx) == 4:
                aspect_ratio = float(w) / h
                print('aspect_ratio= ', aspect_ratio)
                if aspect_ratio == 1:
                    cv2.putText(image1, 'Cuadrado', (x, y - 5), 1, 1.5, (0, 255, 0), 2)
                else:
                    cv2.putText(image1, 'Rectangulo', (x, y - 5), 1, 1.5, (0, 255, 0), 2)
            #if len(approx) == 5:
            #    cv2.putText(image1, 'Pentagono', (x, y - 5), 1, 1.5, (0, 255, 0), 2)
            #if len(approx) == 6:
            #    cv2.putText(image1, 'Hexagono', (x, y - 5), 1, 1.5, (0, 255, 0), 2)
            #if len(approx) > 10:
            #    cv2.putText(image1, 'Circulo', (x, y - 5), 1, 1.5, (0, 255, 0), 2)
            cv2.drawContours(image1, [approx], 0, (0, 255, 0), 2)
            cv2.imshow('image', image1)
            cv2.waitKey(0)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap1.release()
        cap2.release()
        cv2.destroyAllWindows()

    elif ejemplo == "17":
        """Detección de círculos con HOG"""
        cap1 = cv2.VideoCapture(2)
        cap2 = cv2.VideoCapture(0)
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        image1 = frame1
        img = image1
        image2 = frame2
        src = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        src2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        #img = cv2.imread('data/stuff.jpg')
        #src = cv2.medianBlur(img, 5)
        #src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(src, cv2.HOUGH_GRADIENT, 1, 100,
                                   param1=50, param2=30, minRadius=10, maxRadius=100)

        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # dibujar circulo
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # dibujar centro
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

        global puntos_click

        # Clonar la imagen original para poder escribir sobre ella
        # sin modificarla
        imagen_conpuntos = img

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
                imagen_conpuntos = img.copy()

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
                    cv2.putText(imagen_conpuntos, str(pts_id + 1), (x, y), font,
                                4, (0, 0, 255), 2, cv2.LINE_AA)

        las_xprima = np.array(puntos_click)

        las_x = np.array([(150, 150), (150, 200), (200, 150), (200, 200)])

        H, estado = cv2.findHomography(las_xprima, las_x, cv2.RANSAC,0.01)

        rectificada = cv2.warpPerspective(img, H,
                                               (int(1.5 * img.shape[1]),
                                                int(1.5 * img.shape[0])))
        cv2.namedWindow("Rectificada")
        cv2.imshow("Rectificada", rectificada)
        cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()


        #cv2.imshow('detected circles', img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

    elif ejemplo == "18":
        """Detección de círculos con HOG"""
        cap1 = cv2.VideoCapture(2)
        cap2 = cv2.VideoCapture(0)
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        image1 = frame1
        img = image1
        img2 = frame2
        src = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        src2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        #img = cv2.imread('data/stuff.jpg')
        #src = cv2.medianBlur(img, 5)
        #src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(src, cv2.HOUGH_GRADIENT, 1, 100,
                                   param1=50, param2=30, minRadius=10, maxRadius=100)

        circles2 = cv2.HoughCircles(src2, cv2.HOUGH_GRADIENT, 1, 100,
                                   param1=50, param2=30, minRadius=10, maxRadius=100)

        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # dibujar circulo
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # dibujar centro
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

        circles2 = np.uint16(np.around(circles2))
        for i in circles2[0, :]:
            # dibujar circulo
            cv2.circle(img2, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # dibujar centro
            cv2.circle(img2, (i[0], i[1]), 2, (0, 0, 255), 3)


        # Clonar la imagen original para poder escribir sobre ella
        # sin modificarla
        imagen_conpuntos = img

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
                imagen_conpuntos = img.copy()

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
                    cv2.putText(imagen_conpuntos, str(pts_id + 1), (x, y), font,
                                4, (0, 0, 255), 2, cv2.LINE_AA)

        las_xprima = np.array(puntos_click)

        las_x = np.array([(150, 150), (150, 200), (200, 150), (200, 200)])

        H, estado = cv2.findHomography(las_xprima, las_x, cv2.RANSAC, 0.01)

        rectificada = cv2.warpPerspective(img, H,
                                          (int(1.5 * img.shape[1]),
                                           int(1.5 * img.shape[0])))

        puntos_click = list()


        # Clonar la imagen original para poder escribir sobre ella
        # sin modificarla
        imagen_conpuntos2 = img2

        # Mostrar la imagen
        cv2.namedWindow("Imagen_Original2")
        cv2.setMouseCallback("Imagen_Original2", click_and_count)

        while True:
            # mostrar la imagen
            cv2.imshow("Imagen_Original2", imagen_conpuntos2)
            key = cv2.waitKey(1) & 0xFF

            # menu principal
            # Si se presiona "r" resetee la imagen
            if key == ord("r"):
                puntos_click = list()
                imagen_conpuntos2 = img2.copy()

            # Si se presiona "q" salir
            elif key == ord("q"):
                break

            # Graficar los puntos que hayan en puntos_click
            if puntos_click:
                for pts_id, coords in enumerate(puntos_click):
                    # coordenadas
                    x2, y2 = coords[0], coords[1]
                    # dibujar un circulo
                    cv2.circle(imagen_conpuntos2, (x2, y2), 5, (0, 0, 255), 5, 2)
                    # Seleccionar una fuente
                    font2 = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(imagen_conpuntos2, str(pts_id + 1), (x2, y2), font2,
                                4, (0, 0, 255), 2, cv2.LINE_AA)


        las_xprima2 = np.array(puntos_click)

        las_x2 = np.array([(150, 150), (150, 200), (200, 150), (200, 200)])

        H2, estado2 = cv2.findHomography(las_xprima2, las_x2, cv2.RANSAC, 0.01)

        rectificada2 = cv2.warpPerspective(img2, H2,
                                          (int(1.5 * img2.shape[1]),
                                           int(1.5 * img2.shape[0])))


        cv2.namedWindow("Rectificada")
        cv2.imshow("Rectificada", rectificada)
        cv2.namedWindow("Rectificada2")
        cv2.imshow("Rectificada2", rectificada2)

        cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()


        #cv2.imshow('detected circles', img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

    elif ejemplo=="20":
        cap1 = cv2.VideoCapture(1)
        ret1, frame1 = cap1.read()
        image1 = frame1
        img = image1
        src = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        # img = cv2.imread('data/stuff.jpg')
        # src = cv2.medianBlur(img, 5)
        # src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(src, cv2.HOUGH_GRADIENT, 1, 100,
                                   param1=50, param2=30, minRadius=10, maxRadius=150)

        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # dibujar circulo
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # dibujar centro
            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

        # Clonar la imagen original para poder escribir sobre ella
        # sin modificarla
        imagen_conpuntos = img

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
                imagen_conpuntos = img.copy()

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
                    cv2.putText(imagen_conpuntos, str(pts_id + 1), (x, y), font,
                                4, (0, 0, 255), 2, cv2.LINE_AA)

        las_xprima = np.array(puntos_click)

        las_x = np.array([(0, 0), (0, 300), (300, 0), (300, 300)])

        H, estado = cv2.findHomography(las_xprima, las_x, cv2.RANSAC, 0.01)

        rectificada = cv2.warpPerspective(img, H,
                                          (int(1.5 * img.shape[1]),
                                           int(1.5 * img.shape[0])))

        puntos_click = list()

        # Clonar la imagen original para poder escribir sobre ella
        # sin modificarla
        # Mostrar la imagen

        cv2.namedWindow("Rectificada")
        cv2.imshow("Rectificada", rectificada)

        cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

        # cv2.imshow('detected circles', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        while True:
            ret1, frame1 = cap1.read()
            image1 = frame1
            img = image1

            rectificada = cv2.warpPerspective(img, H,
                                              (int(1.5 * img.shape[1]),
                                               int(1.5 * img.shape[0])))

            redBajo1=np.array([0, 0,200],np.uint8)
            redAlto1=np.array([8, 8, 255], np.uint8)

            redBajo2 = np.array([165, 0, 200], np.uint8)
            redAlto2 = np.array([179, 8, 255], np.uint8)

            maskLaserBajo = np.array([150,0,20],np.uint8)
            maskLaserAlto = np.array([179,100,255],np.uint8)

            hsv_rectificada = cv2.cvtColor(rectificada, cv2.COLOR_BGR2HSV)
            maskRed1=cv2.inRange(hsv_rectificada, redBajo1, redAlto1)
            maskRed2=cv2.inRange(hsv_rectificada, redBajo2, redAlto2)
            maskRed=cv2.add(maskRed1,maskRed2)
            laserMaskRed = cv2.inRange(hsv_rectificada,maskLaserBajo,maskLaserAlto)

            cv2.namedWindow("Rectificada")
            cv2.imshow("Rectificada", maskRed)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    else:
        print("You typed:")
        print(ejemplo)
        print("And this is not a valid option")

# ===========================================================================
if __name__ == '__main__':
    main()
