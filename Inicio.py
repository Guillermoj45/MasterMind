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

def esconder(palabragenerada):
    fotosecret = lsb.hide("mastermind_logorigin.png", palabragenerada)
    fotosecret.save("Mastermind_secreto.png")

def mostrar():
    palabramostra = lsb.reveal("Mastermind_secreto.png")
    print(palabramostra)
    return palabramostra

def opcion2():
    juego = input('Escribe a qué modalidad de juego deseas jugar: secuencia de cinco números (N) o palabra de ocho'
                  'caracteres (L). Escribe N o L: ')
    while juego != 'N' and juego != 'L':
        juego = input('Escribe a qué modalidad de juego deseas jugar: secuencia de cinco números (N) o palabra de ocho'
                      'caracteres (L). Escribe N o L: ')
    if juego == 'N':
        palabragenerada = str(random.randint(10000, 99999))
        print("Número generado:", palabragenerada)
    else:
        with open('palabras.dat', 'r', encoding='utf-8') as archivo:
            palabras = [linea.strip() for linea in archivo]
        palabragenerada = random.choice(palabras)
        print("Palabra generada:", palabragenerada)
    esconder(palabragenerada)
    mostrar()
    '''print("Ocultando el texto en la imagen...")
    # Cargar la imagen original
    img = cv2.imread('mastermind_logorigin.png')

    # Ocultar el texto en la imagen y guardar la nueva imagen
    img_con_texto_oculto = ocultar_texto_en_imagen(img, palabragenerada)

    print("Mostrando la imagen con el texto oculto...")
    # Mostrar la imagen con el texto oculto
    mostrar_imagen("imagen_con_texto_oculto.png")'''
    return palabragenerada, juego
def opcion3():

    print('\t\t\t\t\033[1mAPLICACIÓN MASTERMIND\033[0m')
    print('\t\tSe ha recuperado la combinación')
    nombre = input('\t\tTu nickname, por favor: ')
    print(f'\t\t¡Comiza el juego para {nombre}!')

    if 'N' == juego:
        print('\n\n\t\t\t\t\033[1mAPLICACIÓN MASTERMIND\033[0m')
        print('\n\t\t\t\t ¡Tienes 4 intentos!')
        print('\t\t\t\t     ¡Comenzamos!\n')
        numusuario = str(input('Introduce su número propuesto: '))
        for caracter in numusuario:
            esta = False
            noesta = False
            for incog in palabragenerada:


                if caracter == incog:
                    esta = True
                    break
                elif caracter != incog:
                    noesta = True
                    break
            if esta:
                print('SI ESTA', caracter)
            elif noesta:
                print('No esta ', caracter)

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
        valores = opcion2()
        palabragenerada = valores[0]
        juego = valores[1]

    elif opcion == 3:
        print('\n\t\t\t\t\tOpción: 3\n')
        opcion3()
    elif opcion == 4:
        salir = True