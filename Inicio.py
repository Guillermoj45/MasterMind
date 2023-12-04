import math
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
import itertools
from random import randint
from statistics import mean
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def opcion1():
    # Lee la imagen desde el archivo 'mastermind_logorigin.png'
    img = cv2.imread('mastermind_logorigin.png')

    # Define los parámetros para el primer conjunto de texto
    texto = "Equipo 1"
    position = (105, 50)
    font = cv2.FONT_HERSHEY_DUPLEX
    tamaño = 2
    color = (29, 152, 248)
    grosor = 3

    # Añade el primer conjunto de texto a la imagen
    cv2.putText(img, texto, position, font, tamaño, color, grosor)

    # Define los parámetros para el segundo conjunto de texto
    texto = "1DAM Curso 2023/24"
    position = (70, 310)
    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    tamaño = 1.05
    color = (37, 40, 219)
    grosor = 2

    # Añade el segundo conjunto de texto a la imagen
    cv2.putText(img, texto, position, font, tamaño, color, grosor)

    # Muestra la imagen con el texto añadido en una ventana
    cv2.imshow("Imagen con Texto", img)
    cv2.waitKey(0)
    # Guarda la imagen con el texto añadido como 'fotoconlogo.png'
    cv2.imwrite("fotoconlogo.png", img)
    cv2.destroyAllWindows()


def esconder(palabragenerada):
    # Utiliza la función hide de la biblioteca stegano para ocultar la palabra generada en la imagen
    fotosecret = lsb.hide("mastermind_logorigin.png", palabragenerada)
    # Utiliza la función hide de la biblioteca stegano para ocultar la palabra generada en la imagen
    fotosecret.save("Mastermind_secreto.png")


def mostrar():
    # Utiliza la función reveal de la biblioteca stegano para revelar la información oculta en la imagen
    palabramostra = lsb.reveal("Mastermind_secreto.png")
    # Retorna la información revelada (en este caso, la palabra oculta)
    return palabramostra


def aleatorio(juego):
    if juego == 'N':
        # Si el juego es de números, genera un número aleatorio de 5 dígitos
        palabragenerada = str(random.randint(10000, 99999))
        print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tNúmero generado:", palabragenerada)
    else:
        # Si el juego es de palabras, lee las palabras desde el archivo 'palabras.dat' y elige una al azar
        with open('palabras.dat', 'r', encoding='utf-8') as archivo:
            palabras = [linea.strip() for linea in archivo]
            palabragenerada = random.choice(palabras)
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tPalabra generada:", palabragenerada)
    # Retorna la palabra o número generado
    return palabragenerada


def opcion2():
    juego = () # Inicializa la variable juego como una tupla vacía
    while juego != 'N' and juego != 'L':
        # Solicita al usuario que elija la modalidad de juego (N para números o L para palabras)
        juego = input('\t\t\t\t\tEscribe a qué modalidad de juego deseas jugar: secuencia de cinco números (N) o'
                      ' palabra de ocho caracteres (L). Escribe N o L: ')
        print()
        juego = juego.upper() # Convierte la entrada del usuario a mayúsculas
    palabragenerada = aleatorio(juego) # Genera la palabra o número aleatorio según la modalidad de juego
    esconder(palabragenerada) # Oculta la palabra o número en una imagen utilizando esteganografía

    # Retorna la modalidad de juego elegida por el usuario
    return juego

def la_mejor_txt():
    registrotxt = open("partidas.txt", "r") # Abre el archivo "partidas.txt" en modo lectura
    registro = registrotxt.read() # Leetodo el contenido del archivo
    partidas = registro.split("\n") # Divide el contenido del archivo en líneas
    # Inicializa variables para almacenar los detalles de la mejor partida
    intentosmin = 999
    for a in range(len(partidas)):
        if partidas[a] != "":
            # Obtiene los datos de cada partida separados por el carácter '#'
            partida = partidas[a]
            datos1 = partida.split("#")
            # Convierte datos relevantes a tipos adecuados (intentos a entero, tiempo a flotante)
            datos1[3] = int(datos1[3])
            datos1[4] = float(datos1[4])
            # Compara con la mejor partida hasta ahora
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
        # Cierra el archivo después de leerlo
    registrotxt.close()
    # Retorna los detalles de la mejor partida
    return fecha, repeticiones, combinacion, intentosmin, tiempomin, conseguido


def ranksave(nombre):
    # Obtiene los detalles de la mejor partida desde el archivo "partidas.txt"
    fecha, repeticiones, combinacion, intentosmin, tiempomin, conseguido = la_mejor_txt()

    # Inicializa una lista vacía para almacenar las partidas
    partidas = []
    # Crea un diccionario con los detalles de la nueva partida
    dataplay = {"fecha": fecha,
                "repeticiones": repeticiones,
                "combinacion": combinacion,
                "intentos": intentosmin,
                "tiempo": tiempomin,
                "conseguido": conseguido,
                "nombre": nombre}
    try:
        # Intenta abrir el archivo "ranking.dat" en modo lectura binaria
        ranking = open("ranking.dat", "rb")
        # Carga las partidas existentes desde el archivo usando pickle
        partidas = pickle.load(ranking)
    except:
        # Si el archivo no existe, crea uno nuevo en modo escritura binaria
        ranking = open("ranking.dat", "wb")

    # Cierra el archivo después de leerlo o crearlo
    ranking.close()
    # Abre el archivo "ranking.dat" en modo escritura binaria
    ranking = open("ranking.dat", "wb")
    # Establece un límite de 90 intentos (esto podría ser una variable ajustable)
    intentos = 90
    if conseguido == "True":
        # Si la lista de partidas está vacía, añade la nueva partida
        if len(partidas) == 0:
            partidas.append(dataplay)
        else:
            # Si la lista de partidas está vacía, añade la nueva partida
            for a in range(len(partidas)):
                b = partidas[a]
                # Obtiene la cantidad de intentos de la partida existente
                intentoslist = b.get("intentos")
                if intentos < intentoslist:
                    partidas.insert(a, dataplay)
                    break
                elif intentosmin == intentoslist:
                    tiempolis = b.get("tiempo")
                    if tiempolis > tiempomin:
                        partidas.insert(a, dataplay)
                        break
                        # Si la lista aún no tiene 10 elementos, añade la nueva partida
                    elif len(partidas) < 10:
                        partidas.append(dataplay)
                        break
                else:
                    partidas.append(dataplay)
                    break

    # Limita la lista de partidas a un máximo de 10 elementos
    del partidas[10:]
    # Guarda la lista de partidas en el archivo "ranking.dat" usando pickle
    pickle.dump(partidas, ranking)
    # Cierra el archivo después de escribir en él
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
    f = open("partidas.txt", "w") # Abre el archivo "partidas.txt" en modo escritura para borrar su contenido
    f.close()
    pista = []
    conseguido = False
    cerrando = ""
    repetir = "S"
    repeticiones = 0
    palabragenerada = mostrar() # Genera la palabra o número aleatorio
    fecha = datetime.datetime.now()  # Obtiene la fecha y hora actual
    fechacon = f"{fecha.day}/{fecha.month}/{fecha.year} {fecha.hour}:{fecha.minute}"

    # Crea una cadena "cerrando" con el mismo tamaño que la palabra generada, llena de "o"
    for a in range(len(palabragenerada)):
        cerrando += "o"
        # Determina el tipo de juego (N para números, L para letras)
    if juego == "N":
        tipo = 4 #Determina el número de intentos para N
        menerror = "!INTRODUZCA 5 NUMEROS¡"
    else:
        tipo = 7 #Determina el número de intentos para L
        menerror = "!INTRODUZCA 8 LETRAS¡"
    print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\033[1mAPLICACIÓN MASTERMIND\033[0m')
    print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tSe ha recuperado la combinación')
    nombre = input('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tTu nickname, por favor: ')
    print(f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t¡Comienza el juego para {nombre}!')
    while repetir.upper() == "S": #Determina el inicio de una nueva partida
        print('\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\033[1mAPLICACIÓN MASTERMIND\033[0m')
        print(f'\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t ¡Tienes {tipo} intentos!')
        print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t     ¡Comenzamos!\n')
        inicio = time.time()  # Registra el tiempo de inicio del juego
        intentos = []  # Lista para almacenar los intentos del jugador
        pistas = []  # Lista para almacenar las pistas correspondientes a cada intento
        vidas = 0  # Contador de intentos realizados
        cierre = True  # Controla si el juego sigue en curso o no
        repeticiones += 1  # Incrementa el contador de repeticiones de juego
        while cierre and vidas < tipo: # Bucle interno del juego: el jugador tiene oportunidades hasta agotar vidas (intentos)
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

                salida = ''.join(pista)# Convierte la lista de pistas en una cadena

                intentos.append(numusuario)  # Agrega la combinación propuesta a la lista de intentos
                pistas.append(salida)  # Agrega la pista correspondiente a la lista de pistas

                print()
                print(f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\033[4mPropuesto\033[0m\t\t\t\t\033[4mResultado\033[0m')
                for a in range(len(intentos)):
                    b = intentos[a]
                    c = pistas[a]
                    print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{b}\t\t\t\t\t{c}")

                vidas += 1 #Añade 1 al contador de intentos
                # Verifica si la combinación propuesta es igual a la combinación generada
                if salida == cerrando:
                    print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tCombinación descubierta")
                    cierre = False
                    conseguido = True
                    print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t¡En {vidas} intentos!")
                    # Verifica si se han agotado los intentos
                if vidas == tipo:
                    cierre = False
                    print("\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t¡Has agotado los intentos!"
                          "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tCombinación no descubierta"
                          "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", (palabragenerada))
                final = time.time() # Registra el tiempo al finalizar el juego
        palabragenerada = aleatorio(juego) # Genera una nueva combinación para la siguiente partida
        alltime = final - inicio  #Calcula la duración total del juego
        guardartxt(fechacon, repeticiones, palabragenerada, vidas, alltime, conseguido)  # Guarda los resultados en el archivo de texto
        repetir = input("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t¿Volvemos a jugar (S/N)? ")
    ranksave(nombre)
    return nombre

def Rankins():
    # Definir el orden de las columnas para mostrar
    datos_orden = ["nombre", "intentos", "tiempo", "repeticiones", "combinacion", "fecha"]
    # Abrir el archivo "ranking.dat" en modo lectura binaria
    archivo = open("ranking.dat", "rb")

    # Cargar los datos del ranking desde el archivo usando pickle
    ranking = pickle.load(archivo)
    archivo.close() # Cerrar el archivo después de leerlo
    tabla = pd.DataFrame(ranking) # Crear un DataFrame de pandas con los datos del ranking

    # Configurar opciones para mostrar más filas y columnas
    pd.set_option('display.max_rows', None)  # Mostrar todas las filas
    pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
    pd.set_option('display.width', None)  # Ancho de la visualización
    tabla = tabla.sort_values(by=["intentos", "tiempo"]) # Ordenar el DataFrame por "intentos" y "tiempo"
    datosor = tabla[datos_orden]  # Seleccionar las columnas ordenadas según el orden definido
    datosor = datosor.head(10)  # Mostrar solo las 10 mejores filas
    datosor.rename(columns={'fecha': 'fecha y hora'}, inplace=True)  # Cambiar el nombre de la columna 'fecha' a 'fecha y hora'

    # Imprimir la tabla formateada sin índices y con espaciado y alineación personalizados
    print(datosor.to_string(index=False, col_space=10, justify='center'))


def sacar_datos_txt():
    archivo = open("partidas.txt", "r") # Abrir el archivo "partidas.txt" en modo lectura
    registro = archivo.read()  # Leer el contenido del archivo
    archivo.close() # Cerrar el archivo después de leerlo
    # Inicializar listas para almacenar los datos
    fecha = []
    repeticiones = []
    combinacion = []
    intentos = []
    tiempo = []
    conseguido = []
    partidas = registro.split("\n")
    for a in range(len(partidas)):
        if partidas[a] != "":
            partida = partidas[a]
            datos1 = partida.split("#")
            datos1[3] = int(datos1[3])
            datos1[4] = float(datos1[4])
            # Agregar los datos a las listas correspondientes
            fecha.append(datos1[0])
            repeticiones.append(datos1[1])
            combinacion.append(datos1[2])
            intentos.append(datos1[3])
            tiempo.append(datos1[4])
            conseguido.append(datos1[5])
    # Devolver las listas con los datos extraídos
    return fecha, repeticiones, combinacion, intentos, tiempo, conseguido

def posicion (timeuser, combinacionuser, fechauser, intetosuser, nombreuser):
    archivo = open("ranking.dat", "rb") # Abrir el archivo "ranking.dat" en modo lectura binaria
    registro = pickle.load(archivo)
    archivo.close()
    for a in range(len(registro)):
        b = registro[a]
        combinacion = b.get("combinacion")
        tiempo = b.get("tiempo")
        fecha = b.get("fecha")
        intentos = b.get("intentos")
        nombre = b.get("nombre")
        # Verificar si los datos de la partida coinciden con los proporcionados como argumentos
        if tiempo == timeuser and combinacion == combinacionuser and fecha == fechauser and intentos == intetosuser and nombre == nombreuser:
            # Devolver None si no se encuentra la partida en el ranking
            return a+1

def PDF():
    c = canvas.Canvas("partidas.pdf", pagesize=letter)

    # Cargar la imagen y obtener sus dimensiones
    img = utils.ImageReader("fotoconlogo.png")
    data = sacar_datos_txt()
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
    c.drawString(60, 530, f"El jugador pedro ha jugado las siguientes partidas {len(data[1])} partidas:")
    # Guardar el PDF

    # Creamos la tabla
    w, h = A4
    max_rows_per_page = 6

    Eje_x = 50
    Eje_y = 330

    separacion = 15
    fecha, repeticiones, combinaciones, intentos, tiempo, conseguido = data
    xlist = [x + Eje_x for x in [0, 100, 180, 260, 310, 400, 480]]
    ylist = [h - Eje_y - i * separacion for i in range(max_rows_per_page + 1)]

    # Agregar encabezados
    headers = ["Fecha", "Repeticiones", "Combinación", "Intentos", "Tiempo(secs)", "Conseguido"]

    for x, header in zip(xlist, headers):
        c.drawString(x + 2, ylist[0] - separacion + 3, header)

    # Incrementar el índice de y para comenzar con los datos
    y_index = 1
    for row in zip(fecha, repeticiones, combinaciones, intentos, tiempo, conseguido):
        c.grid(xlist, ylist[:2])
        for x, cell in zip(xlist, row):
            c.drawString(x + 2, ylist[y_index] - separacion + 3, str(cell))
        y_index += 1

        # Si alcanza el límite de filas por página, mostrar la siguiente página
        if y_index == max_rows_per_page:
            c.showPage()
            c.drawString(x + 2, ylist[y_index] - separacion + 3, str(cell))
            y_index = 0

    fecha, repeticiones, combinacion, intentosmin, tiempomin, conseguido = la_mejor_txt()
    c.drawString(60, 310, 'Su mejor partida ha sido:')
    c.drawString(60, 295, f"{fecha} --- {repeticiones} --- {combinacion} --- {intentosmin} --- {tiempomin} --- {'True' if conseguido else 'False'}")
    posicion1 = posicion(tiempomin, combinacion, fecha, intentosmin, nombre)
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
        input()

    elif opcion == 3:
        print(f'\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tOpción: {opcion}\n')
        nombre = opcion3()
        input()

    elif opcion == 4:
        print(f'\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tOpción: {opcion}\n')
        Rankins()
        input()

    elif opcion == 5:
        PDF()

    elif opcion == 6:
        print(sacar_datos_txt())
