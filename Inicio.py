import random
import cv2


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


def opcion2():
    juego = input('Escribe a qué modalidad de juego deseas jugar: secuencia de cinco números (N) o palabra de ocho'
                  'caracteres (L). Escribe N o L: ')
    while juego != 'N' and juego != 'L':
        juego = input('Escribe a qué modalidad de juego deseas jugar: secuencia de cinco números (N) o palabra de ocho'
                      'caracteres (L). Escribe N o L: ')
    if juego == 'N':
        numero = random.randint(1000, 9999)
        print(numero)
    else:
        palabra_ale = random.choice
        with open('palabras.dat', 'r', encoding='utf-8') as archivo:
            palabras = [linea.strip() for linea in archivo]
        palabragenerada = palabra_ale(palabras)
        print(palabragenerada)

def opcion3():
    print('\t\t\t\t\033[1mAPLICACIÓN MASTERMIND\033[0m')

    print('\t\tSe ha recuperado la combinación')
    nombre = input('\t\tTu nickname, por favor: ')
    print(f'\t\t¡Comienza el juego para {nombre}!')


salir = False

while not salir:
    print('\t\t\t\t\033[1mAPLICACIÓN MASTERMIND\033[0m')
    print('\t1) Cración del logo de equipo')
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
        opcion2()
    elif opcion == 3:
        print('\n\t\t\t\t\tOpción: 3\n')
        opcion3()

    elif opcion == 4:
        salir = True
