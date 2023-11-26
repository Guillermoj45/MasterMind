import random
import cv2
from stegano import lsb
import numpy as np
import pytesseract
import time
import datetime
import pickle


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


def aleatorio(juego):
    if juego == 'N':
        palabragenerada = str(random.randint(10000, 99999))
        print("Número generado:", palabragenerada)
    else:
        with open('palabras.dat', 'r', encoding='utf-8') as archivo:
            palabras = [linea.strip() for linea in archivo]
            palabragenerada = random.choice(palabras)
            print("Palabra generada:", palabragenerada)
    return palabragenerada


def opcion2():
    juego = ()
    while juego != 'N' and juego != 'L':
        juego = input('Escribe a qué modalidad de juego deseas jugar: secuencia de cinco números (N) o palabra de ocho'
                      'caracteres (L). Escribe N o L: ')
        juego = juego.upper()
    palabragenerada = aleatorio(juego)
    esconder(palabragenerada)
    mostrar()
    return palabragenerada, juego


def ranksave(fecha, repeticiones, combinacion, intentos, tiempo, conseguido):
    partidas = []
    dataplay = {"fecha": fecha,
                "repeticiones": repeticiones,
                "combinacion": combinacion,
                "intentos": intentos,
                "tiempo": tiempo,
                "conseguido": conseguido}
    try:
        ranking = open("ranking.dat", "rb")
        partidas = pickle.load(ranking)

    except:
        ranking = open("ranking.dat", "wb")

    ranking.close()
    ranking = open("ranking.dat", "wb")

    if len(partidas) == 0:
        partidas.append(dataplay)
    else:
        for a in range(len(partidas)):
            b = partidas[a]
            intentoslist = b.get("intentos")
            if intentos < intentoslist:
                partidas.into(dataplay, b)
            else:
                partidas.append(dataplay)
                del partidas[10:]
    pickle.dump(partidas, ranking)
    ranking.close()


def guardartxt(fecha, repeticiones, combinacion, intentos, tiempo, conseguido):
    try:
        registrotxt = open("partidas.txt", "r")
        registro = registrotxt.read()
        registrotxt.close()
    except:
        pass
    registrotxt = open("partidas.txt", "a+")
    datos = (f"|{fecha}|{repeticiones}|{combinacion}|{intentos}|{tiempo}|{conseguido}|\n")
    '''datos = (f"fecha y hora\t\tnúmero\tconbinacián\tintentos\ttiempo (secs)\t\tconseguido\n"
             f"{fecha}\t{repeticiones}\t{combinacion}\t\t{intentos}\t\t{tiempo}\t\t{conseguido}\n"
             f"__________________________________________________________________________________")'''
    registrotxt.write(datos)
    registrotxt.close()
    registrotxt = open("partidas.txt", "r")
    print(registrotxt.read())


def opcion3(palabragenerada):
    pista = []
    conseguido = False
    cerrando = ""
    repetir = "S"
    repeticiones = 0
    fecha = datetime.datetime.now()
    fechacon = f"{fecha.day}/{fecha.month}/{fecha.year} {fecha.hour}:{fecha.minute}"

    registrotxt= open('partidas.txt', 'w')
    cabezal = ("|fecha_hora|número|conbinación|intentos|tiempo(secs)|conseguido|\n"
               "|---|---|---|---|---|---|\n")
    registrotxt.write(cabezal)
    registrotxt.close()
    for a in range(len(palabragenerada)):
        cerrando += "o"
    if juego == "N":
        tipo = 4
    else:
        tipo = 7
    print('\t\t\t\t\033[1mAPLICACIÓN MASTERMIND\033[0m')
    print('\t\tSe ha recuperado la combinación')
    nombre = input('\t\tTu nickname, por favor: ')
    print(f'\t\t¡Comiza el juego para {nombre}!')
    while repetir.upper() == "S":
        print('\n\n\t\t\t\t\033[1mAPLICACIÓN MASTERMIND\033[0m')
        print(f'\n\t\t\t\t ¡Tienes {tipo} intentos!')
        print('\t\t\t\t     ¡Comenzamos!\n')
        inicio = time.time()

        vidas = 0
        cierre = True
        repeticiones += 1
        while cierre and vidas < tipo:
            pista = []
            numusuario = str(input('Introduce su número propuesto: '))
            if len(numusuario) != len(palabragenerada):
                print("!INTRODUZCA 5 NUMEROS¡")
            else:
                for a in range(len(numusuario)):
                    caracter = numusuario[a]
                    incogprin = palabragenerada[a]
                    esta = False
                    if caracter == incogprin:
                        pista.append("o")
                    else:
                        for incog in palabragenerada:
                            if caracter == incog:
                                esta = True
                        if esta:
                            pista.append("-")
                        elif esta == False:
                            pista.append("x")

                salida = ''.join(pista)
                print(salida)
                vidas += 1
                if salida == cerrando:
                    print("Combinación descubierta")
                    cierre = False
                    conseguido = True
                    print(f"¡En {vidas} intentos!")
                if vidas == tipo:
                    cierre = False
                    print("¡Has agotado los intentos!")
                final = time.time()
        palabragenerada = aleatorio(juego)
        alltime = final - inicio
        guardartxt(fechacon, repeticiones, palabragenerada, vidas, alltime, conseguido)
        repetir = input("¿Volvemos a jugar (S/N)? ")
    ranksave(fecha, repeticiones, palabragenerada, vidas, alltime, conseguido)


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
        opcion3(palabragenerada)

    elif opcion == 4:
        salir = True
