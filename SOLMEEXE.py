"""El siguiente programa genera una interfáz gráfica de usuario que permite usar de una forma más cómoda
la clase de visión por computador desarrollada por el experto Jorge Martinez"""


from tkinter import*
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import cv2
import os
import imutils
from skimage import io
import numpy as np
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas


def elegir_imagen():

    # Rutina para abrir el buscador de archivos cargar imágenes, y procesarlas

    path_image = filedialog.askopenfilename(filetypes=[
        ("image", ".jpg"),
        ("image", ".jpeg"),
        ("image", ".png")])

    if len(path_image) > 0:

        # Al confirmarse que el path es lógico se define  una variable global "img"

        global img

        img = io.imread(path_image) # Luego se lee la imagen del path

        imageToShow = imutils.resize(img, width=400) # Escalado de la imagen para mostrar en el GUI
        imageToShow = Image.fromarray(imageToShow)
        imageToShow = ImageTk.PhotoImage(image=imageToShow)

        lblInputImage.configure(image=imageToShow)
        lblInputImage.img = imageToShow

        lblInfo1 = Label(root, text="IMAGEN DE ENTRADA")
        lblInfo1.grid(column=0, row=1, padx=10, pady=10)


def procesar():

    global modelo

    imge = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    hsv_original = cv2.cvtColor(imge, cv2.COLOR_BGR2HSV)

     #img = requests.get(url)

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
    cv2.drawContours(imge, contours, -1, (0, 255, 0), 2)

    #cv2.imshow('Original', imge)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

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
    rectificada = cv2.warpPerspective(imge, H,
                                        (int(1.5 * imge.shape[1]),
                                        int(1.5 * imge.shape[0])))

    #Se recorta la imagen a el área de interés
    rectificada = rectificada[100:900, 100:900]

    #cv2.imshow('Rectificada', rectificada)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    gray_rectificada = cv2.cvtColor(rectificada, cv2.COLOR_BGR2GRAY)
    _, bin_rectificada = cv2.threshold(gray_rectificada, 150, 200, cv2.THRESH_BINARY_INV)
    print(type(bin_rectificada))

    #cv2.imshow('Rectificada contornos', bin_rectificada)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

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

   # Pintar la imagen modelo en el guide:

    ModelToShow = imutils.resize(modelo, width=400)
    ModelToShow = Image.fromarray(ModelToShow)
    ModelToShow = ImageTk.PhotoImage(image=ModelToShow)

    lblOutputImage.configure(image=ModelToShow)
    lblOutputImage.img = ModelToShow

    lblInfo2 = Label(root, text="IMAGEN DE SALIDA")
    lblInfo2.grid(column=1, row=1, padx=20, pady=20)

    #Se guarda la imagen como archivo jpg, para luego poder insertarla en el PDF

    cv2.imwrite("img_modelo.jpg", modelo)

    #Se establece el tamaño del lienzo PDF
    pagesize = (800 * mm, 800 * mm)

    #Se crea el lienzo con el nombre Modelo.
    c = canvas.Canvas("modelo.pdf", pagesize=pagesize)

    #Se inserta la imagen y se redimensiona a 800X800 mm como la original
    c.drawImage("img_modelo.jpg", 0, 0, width=800*mm, height=800*mm)
    c.save()


def verificarOrdenes(self):
    return


def guardar_imagen():

    availableFormats = [('.jpg', '*.jpg'),
                        ('.png', '*.png')]
    filename = filedialog.asksaveasfilename(title='Save File', filetypes=availableFormats, defaultextension='.jpg')
    #file = filedialog.asksaveasfile(mode='w',  defaultextension=".png")

    cv2.imwrite(filename, modelo)
    filename_length = len(filename)
    pdffilename = filename[0:filename_length-3]+'pdf'
    print(pdffilename)

    # Se establece el tamaño del lienzo PDF
    pagesize = (800 * mm, 800 * mm)

    # Se crea el lienzo con el nombre Modelo.
    c = canvas.Canvas(pdffilename, pagesize=pagesize)

    # Se inserta la imagen y se redimensiona a 800X800 mm como la original
    c.drawImage(filename, 0, 0, width=800 * mm, height=800 * mm)
    c.save()

    return

img = None
modelo = None

# Creamos la ventana principal

root = Tk()
root.title("CASA SOLME")

# label donde se presentará la imagen de entrada y de salida

lblInputImage = Label(root)
lblInputImage.grid(column=0, row=2)

lblOutputImage = Label(root)
lblOutputImage.grid(column=1, row=2, rowspan=6)

# Botón para elegir imágen de entrada

btn1 = Button(root, text="Elegir imágen", width=50, command=elegir_imagen)
btn1.grid(column=0, row=0, padx=5, pady=5)

# Botón para procesar la imagen

btn2 = Button(root, text="Procesar imágen", width=50, command=procesar)
btn2.grid(column=1, row=0, padx=5, pady=5)

# Botón para guardar imágen

btn3 = Button(root, text="Guardar Imágen", width=50, command=guardar_imagen)
btn3.grid(column=0, row=3, padx=5, pady=5)

root.mainloop()