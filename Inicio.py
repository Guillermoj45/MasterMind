import random
import cv2
from stegano import lsb
import time
import datetime
import pickle
import pandas as pd


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
    return palabramostra


def aleatorio(juego):
    if juego == 'N':
        palabragenerada = str(random.randint(10000, 99999))
        print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tNúmero generado:", palabragenerada)
    else:
        with open('palabras.dat', 'r', encoding='utf-8') as archivo:
            palabras = [linea.strip() for linea in archivo]
            palabragenerada = random.choice(palabras)
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tPalabra generada:", palabragenerada)
    return palabragenerada


def opcion2():
    juego = ()
    while juego != 'N' and juego != 'L':
        juego = input('\t\t\t\t\tEscribe a qué modalidad de juego deseas jugar: secuencia de cinco números (N) o'
                      ' palabra de ocho caracteres (L). Escribe N o L: ')
        print()
        juego = juego.upper()
    palabragenerada = aleatorio(juego)
    esconder(palabragenerada)
    palabrafoto = mostrar()
    return palabrafoto, juego

def ranksave(nombre):
    registrotxt = open("partidas.txt", "r")
    registro = registrotxt.read()
    partidas = registro.split("\n")
    intentosmin = 999
    for a in range(len(partidas)):
        if partidas[a] != "":
            partida = partidas[a]
            datos1 = partida.split("#")
            datos1[3] = int(datos1[3])
            datos1[4] = float(datos1[4])
            if datos1[3] < intentosmin:
                fecha = datos1[0]
                repeticiones = datos1[1]
                combinacion = datos1[2]
                intentosmin = datos1[3]
                tiempomin = datos1[4]
                conseguido = datos1[5]
            elif datos1[3] == intentosmin and datos1[4] < tiempomin:
                fecha = datos1[0]
                repeticiones = datos1[1]
                combinacion = datos1[2]
                intentosmin = datos1[3]
                tiempomin = datos1[4]
                conseguido = datos1[5]

    registrotxt.close()

    partidas = []
    dataplay = {"fecha": fecha,
                "repeticiones": repeticiones,
                "combinacion": combinacion,
                "intentos": intentosmin,
                "tiempo": tiempomin,
                "conseguido": conseguido,
                "nombre": nombre}
    try:
        ranking = open("ranking.dat", "rb")
        partidas = pickle.load(ranking)
    except:
        ranking = open("ranking.dat", "wb")

    ranking.close()
    ranking = open("ranking.dat", "wb")
    if conseguido == "True":
        partidas.append(dataplay)
    pickle.dump(partidas, ranking)
    ranking.close()


def guardartxt(fecha, repeticiones, combinacion, intentos, tiempo, conseguido):
    registrotxt = open("partidas.txt", "a+")
    datos = (f"\n{fecha}#{repeticiones}#{combinacion}#{intentos}#{tiempo}#{conseguido}")
    '''datos = (f"fecha y hora\t\tnúmero\tconbinacián\tintentos\ttiempo (secs)\t\tconseguido\n"
             f"{fecha}\t{repeticiones}\t{combinacion}\t\t{intentos}\t\t{tiempo}\t\t{conseguido}\n"
             f"__________________________________________________________________________________")'''
    registrotxt.write(datos)
    registrotxt.close()

def opcion3(palabragenerada):
    f = open("partidas.txt", "w")
    f.close()
    pista = []
    conseguido = False
    cerrando = ""
    repetir = "S"
    repeticiones = 0
    fecha = datetime.datetime.now()
    fechacon = f"{fecha.day}/{fecha.month}/{fecha.year} {fecha.hour}:{fecha.minute}"

    for a in range(len(palabragenerada)):
        cerrando += "o"
    if juego == "N":
        tipo = 4
        menerror = "!INTRODUZCA 5 NUMEROS¡"
    else:
        tipo = 7
        menerror = "!INTRODUZCA 8 LETRAS¡"
    print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\033[1mAPLICACIÓN MASTERMIND\033[0m')
    print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tSe ha recuperado la combinación')
    nombre = input('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tTu nickname, por favor: ')
    print(f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t¡Comienza el juego para {nombre}!')
    while repetir.upper() == "S":
        print('\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\033[1mAPLICACIÓN MASTERMIND\033[0m')
        print(f'\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t ¡Tienes {tipo} intentos!')
        print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t     ¡Comenzamos!\n')
        inicio = time.time()

        vidas = 0
        cierre = True
        repeticiones += 1
        while cierre and vidas < tipo:
            pista = []
            numusuario = str(input('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tIntroduce su combinación propuesta: '))
            if len(numusuario) != len(palabragenerada):
                print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{menerror}")
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
                print()
                print(f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\033[4mPropuesto\033[0m\t\t\t\t\033[4mResultado\033[0m'
                      f'\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{numusuario}\t\t\t\t\t{salida}\n\n\n')
                vidas += 1
                if salida == cerrando:
                    print("Combinación descubierta")
                    cierre = False
                    conseguido = True
                    print(f"¡En {vidas} intentos!")
                if vidas == tipo:
                    cierre = False
                    print("\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t¡Has agotado los intentos!"
                          "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tCombinación no descubierta"
                          "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t",(palabragenerada))
                final = time.time()
        palabragenerada = aleatorio(juego)
        alltime = final - inicio
        guardartxt(fechacon, repeticiones, palabragenerada, vidas, alltime, conseguido)
        repetir = input("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t¿Volvemos a jugar (S/N)? ")
    ranksave(nombre)

def Rankins():
    datos_orden = ["nombre", "intentos", "tiempo", "repeticiones", "combinacion", "fecha"]
    archivo = open("ranking.dat", "rb")

    ranking = pickle.load(archivo)
    archivo.close()
    tabla = pd.DataFrame(ranking)

    # Configurar opciones para mostrar más filas y columnas
    pd.set_option('display.max_rows', None)  # Mostrar todas las filas
    pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
    pd.set_option('display.width', None)  # Ancho de la visualización
    tabla = tabla.sort_values(by=["intentos", "tiempo"])
    datosor = tabla[datos_orden]
    datosor = datosor.head(10)

    print(datosor.to_string(index=False, col_space=10, justify='center'))
    input()

def PDF():

salir = False

while not salir:
    print('\n\n')
    print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\033[1mAPLICACIÓN MASTERMIND\033[0m')
    print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t1) Creación del logo de equipo')
    print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t2) Generación y ocultado de la combinación')
    print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t3) Juego Mastermind')
    print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t4) Ranking de récords')
    print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t5) Informe de las partidas (PDF)')
    print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t6) Salir')
    opcion = int(input('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tOpción:__ '))
    print()

    if opcion == 1:
        print('\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tOpción: 1\n')
        opcion1()

    elif opcion == 2:
        valores = opcion2()
        palabragenerada = valores[0]
        juego = valores[1]

    elif opcion == 3:
        print('\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tOpción: 3\n')
        opcion3(palabragenerada)

    elif opcion == 4:
        Rankins()

    elif opcion == 6:
        salir = True
