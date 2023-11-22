import random
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

    elif opcion == 2:
        print('\n\t\t\t\t\tOpción: 2\n')
        opcion2()
    elif opcion == 3:
        print('\n\t\t\t\t\tOpción: 3\n')

    elif opcion == 4:
        salir = True
