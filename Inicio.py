import random
import cv2
from stegano import lsb
import numpy as np
import pytesseract

def opcion1():
    img = cv2.imread('mastermind_logorigin.png')

    texto = "Equipo 1"
    position = (105, 50)
    font = cv2.FONT_HERSHEY_DUPLEX
    tamaño = 2
    color = (29, 152, 248)
    grosor = 3

    cv2.putText(img, texto, position, font, tamaño, color, grosor)

    texto = "1DAM Curso 2023/24"
    position = (70, 310)
    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    tamaño = 1.05
    color = (37, 40, 219)
    grosor = 2

    cv2.putText(img, texto, position, font, tamaño, color, grosor)

    cv2.imshow("Imagen con Texto", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def ocultar_texto_en_imagen(img, texto):
    # Convertir la imagen a formato RGB (stegano requiere RGB)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Guardar la imagen temporalmente para ocultar el texto
    temp_image_path = "temp_image.png"
    cv2.imwrite(temp_image_path, img_rgb)

    # Ocultar el texto en la imagen
    img_con_texto_oculto = lsb.hide(temp_image_path, texto)
    img_con_texto_oculto.save("imagen_con_texto_oculto.png")

    # Eliminar la imagen temporal
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img_con_texto_oculto

def mostrar_imagen(ruta_imagen):
    # Leer la imagen y mostrarla
    img = cv2.imread(ruta_imagen)
    cv2.imshow("Imagen con Texto Oculto", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def extraer_texto_de_imagen(ruta_imagen):
    # Leer la imagen con texto oculto
    img_con_texto_oculto = lsb.reveal(ruta_imagen)

    # Convertir la imagen a formato NumPy array
    img_con_texto_oculto = np.array(img_con_texto_oculto)

    # Convertir la imagen a escala de grises
    img_con_texto_oculto_gris = cv2.cvtColor(img_con_texto_oculto, cv2.COLOR_BGR2GRAY)

    # Binarizar la imagen para obtener solo el texto oculto
    _, binarizada = cv2.threshold(img_con_texto_oculto_gris, 128, 255, cv2.THRESH_BINARY)

    # Mostrar la imagen binarizada
    cv2.imshow("Texto Oculto", binarizada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # OCR (reconocimiento óptico de caracteres) para extraer el texto
    texto_extraido = pytesseract.image_to_string(binarizada)

    print("Texto Extraído:", texto_extraido)


def opcion2():
    juego = input('Escribe a qué modalidad de juego deseas jugar: secuencia de cinco números (N) o palabra de ocho'
                  'caracteres (L). Escribe N o L: ')
    while juego != 'N' and juego != 'L':
        juego = input('Escribe a qué modalidad de juego deseas jugar: secuencia de cinco números (N) o palabra de ocho'
                      'caracteres (L). Escribe N o L: ')
    if juego == 'N':
        palabragenerada = str(random.randint(1000, 9999))
        print("Número generado:", palabragenerada)
    else:
        with open('palabras.dat', 'r', encoding='utf-8') as archivo:
            palabras = [linea.strip() for linea in archivo]
        palabragenerada = random.choice(palabras)
        print("Palabra generada:", palabragenerada)

    print("Ocultando el texto en la imagen...")
    # Cargar la imagen original
    img = cv2.imread('mastermind_logorigin.png')

    # Ocultar el texto en la imagen y guardar la nueva imagen
    img_con_texto_oculto = ocultar_texto_en_imagen(img, palabragenerada)

    print("Mostrando la imagen con el texto oculto...")
    # Mostrar la imagen con el texto oculto
    mostrar_imagen("imagen_con_texto_oculto.png")
    return palabragenerada, img_con_texto_oculto
def opcion3():
 print(palabragenerada)
salir = False

while not salir:
    print('\t\t\t\t\033[1mAPLICACIÓN MASTERMIND\033[0m')
    print('\t1) Creación del logo de equipo')
    print('\t2) Generación y ocultado de la combinación')
    print('\t3) Juego Mastermind')
    print('\t4) Ranking de récords')
    print('\t5) Informe de las partidas (PDF)')
    print('\t6) Salir')
    opcion = int(input('\tOpción:__ '))

    if opcion == 1:
        print('\n\t\t\t\t\tOpción: 1\n')
        opcion1()
    elif opcion == 2:
        print('\n\t\t\t\t\tOpción: 2\n')
        valores = opcion2()
        palabragenerada = valores[0]
        img_con_texto_oculto = valores[1]
    elif opcion == 3:
        print('\n\t\t\t\t\tOpción: 3\n')
        opcion3()
    elif opcion == 4:
        salir = True