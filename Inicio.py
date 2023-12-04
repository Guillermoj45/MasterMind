import random
import cv2
from stegano import lsb
import time
import datetime
import pickle
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib import utils, colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle


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
    cv2.imwrite("fotoconlogo.png", img)
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

    return juego

def la_mejor_txt():
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
    return fecha, repeticiones, combinacion, intentosmin, tiempomin, conseguido


def ranksave(nombre):
    fecha, repeticiones, combinacion, intentosmin, tiempomin, conseguido = la_mejor_txt()

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
    intentos = 90
    if conseguido == "True":
        if len(partidas) == 0:
            partidas.append(dataplay)
        else:
            for a in range(len(partidas)):
                b = partidas[a]
                intentoslist = b.get("intentos")
                if intentosmin < intentoslist:
                    partidas.insert(a, dataplay)
                    break
                elif intentosmin == intentoslist:
                    tiempolis = b.get("tiempo")
                    if tiempolis > tiempomin:
                        partidas.insert(a, dataplay)
                        break
                    elif len(partidas) < 10:
                        partidas.append(dataplay)
                        break
                else:
                    partidas.append(dataplay)
                    break

    del partidas[10:]
    pickle.dump(partidas, ranking)
    ranking.close()


def guardartxt(fecha, repeticiones, combinacion, intentos, tiempo, conseguido):
    registrotxt = open("partidas.txt", "a+")
    datos = (f"\n{fecha}#{repeticiones}#{combinacion}#{intentos}#{round(tiempo, 2)}#{conseguido}")
    '''datos = (f"fecha y hora\t\tnúmero\tconbinacián\tintentos\ttiempo (secs)\t\tconseguido\n"
             f"{fecha}\t{repeticiones}\t{combinacion}\t\t{intentos}\t\t{tiempo}\t\t{conseguido}\n"
             f"__________________________________________________________________________________")'''
    registrotxt.write(datos)
    registrotxt.close()

def opcion3():
    f = open("partidas.txt", "w")
    f.close()
    pista = []
    conseguido = False
    cerrando = ""
    repetir = "S"
    repeticiones = 0
    palabragenerada = mostrar()
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
        intentos = []
        pistas = []
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

                intentos.append(numusuario)
                pistas.append(salida)
                print()
                print(f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\033[4mPropuesto\033[0m\t\t\t\t\033[4mResultado\033[0m')
                for a in range(len(intentos)):
                    b = intentos[a]
                    c = pistas[a]
                    print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{b}\t\t\t\t\t{c}")

                vidas += 1
                if salida == cerrando:
                    print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tCombinación descubierta")
                    cierre = False
                    conseguido = True
                    print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t¡En {vidas} intentos!")
                if vidas == tipo:
                    cierre = False
                    print("\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t¡Has agotado los intentos!"
                          "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tCombinación no descubierta"
                          "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", (palabragenerada))
                final = time.time()
        palabragenerada = aleatorio(juego)
        alltime = final - inicio
        guardartxt(fechacon, repeticiones, palabragenerada, vidas, alltime, conseguido)
        repetir = input("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t¿Volvemos a jugar (S/N)? ")
    ranksave(nombre)
    return nombre

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
    datosor.rename(columns={'fecha': 'fecha y hora'}, inplace=True)

    print(datosor.to_string(index=False, col_space=10, justify='center'))


def sacar_datos_txt():
    archivo = open("partidas.txt", "r")
    registro = archivo.read()
    archivo.close()
    fecha = []
    repeticiones = []
    combinacion = []
    intentos = []
    tiempo = []
    conseguido = []
    todaspartidas = []
    partidas = registro.split("\n")
    for a in range(len(partidas)):
        if partidas[a] != "":
            partida = partidas[a]
            datos1 = partida.split("#")
            todaspartidas.append(datos1)
    return todaspartidas

def posicion (timeuser, combinacionuser, fechauser, intetosuser, nombreuser):
    archivo = open("ranking.dat", "rb")
    registro = pickle.load(archivo)
    archivo.close()
    for a in range(len(registro)):
        b = registro[a]
        combinacion = b.get("combinacion")
        tiempo = b.get("tiempo")
        fecha = b.get("fecha")
        intentos = b.get("intentos")
        nombre = b.get("nombre")
        if tiempo == timeuser and combinacion == combinacionuser and intentos == intetosuser:
            return a+1

def PDF(nombre):
    c = canvas.Canvas("partidas.pdf", pagesize=letter)

    # Cargar la imagen y obtener sus dimensiones
    img = utils.ImageReader("fotoconlogo.png")
    # Escalar la imagen según las dimensiones proporcionadas
    c.drawImage(img, 160, 580, 300, 180)
    primer = getSampleStyleSheet()
    negrita = primer['BodyText']
    negrita.fontName = "Helvetica-Bold"
    negrita.fontSize = 20
    c.setFont(negrita.fontName, negrita.fontSize)
    c.setFillColor(colors.lightgrey)
    c.rect(50, 545, 500, 25, fill=True)
    c.setFillColor(colors.black)
    c.drawString(180, 550, "INFORMES DE LAS PARTIDA")
    c.setFont("Helvetica", 12)
    data = sacar_datos_txt()
    fecha, repeticiones, combinacion, intentosmin, tiempomin, conseguido = la_mejor_txt()
    posicion1 = posicion(tiempomin, combinacion, fecha, intentosmin, nombre)
    c.drawString(60, 507, f"El jugador {nombre} ha jugado las siguientes partidas {len(data)} partidas:")

    # Creamos la tabla
    data.insert(0, ["Fecha", "Número", "Conbinación", "Intentos", "Tiempo(secs)", "Conseguido"])
    col_widths = [85, 85, 85, 85, 85, 85]
    tabla = Table(data, col_widths)
    styletable = TableStyle([
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('BACKGROUND', (0, 0), (-1, 0), colors.white),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.blue),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.orange),
    ])
    tabla.setStyle(styletable)
    tabla.wrapOn(c, 0, 0)
    tabla.drawOn(c, 50, 430)

    c.drawString(60, 310, 'Su mejor partida ha sido:')
    c.drawString(60, 295, f"{fecha} --- {repeticiones} --- {combinacion} --- {intentosmin} --- {tiempomin} --- {'True' if conseguido else 'False'}")
    c.drawString(60, 280, f'Actualmente {nombre} ocupraía la {posicion1} de nuestro ranking')
    c.save()


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
        print(f'\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tOpción: {opcion}\n')
        opcion1()


    elif opcion == 2:
        print(f'\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tOpción: {opcion}\n')
        juego = opcion2()
        input("Volver al menú...")

    elif opcion == 3:
        print(f'\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tOpción: {opcion}\n')
        nombre = opcion3()
        input("Volver al menú...")

    elif opcion == 4:
        print(f'\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tOpción: {opcion}\n')
        Rankins()
        input("Volver al menú...")

    elif opcion == 5:
        PDF(nombre)

    elif opcion == 6:
        salir = True
