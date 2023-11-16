import random
def aleat():
    dado = random.randint(1, 6)
    return dado

salir = False
lista = []
while not salir:
    a = int(input('¿Cuántos dados lanzamos? '))
    for a in range(a + 1):
        if a > 0:
            lanzar1 = aleat()
            print(f'\nEl dado número {a} ha generado aleatoriamente un:')

            if lanzar1 == 1:
                print('\n*\n')
                lista.append(1)
            elif lanzar1 == 2:
                print('\n\t*\n*\n')
                lista.append(2)
            elif lanzar1 == 3:
                print('\n\t*\n  *\n*\n')
                lista.append(3)
            elif lanzar1 == 4:
                print('\n*\t*\n\n*\t*\n')
                lista.append(4)
            elif lanzar1 == 5:
                print('\n*\t*\n  *\n*\t*\n')
                lista.append(5)
            elif lanzar1 == 6:
                print('\n*\t*\n*\t*\n*\t*\n')
                lista.append(6)
    if a == 0:
        conj = lista
        conj.sort()
        repe = set(conj)
        cadena = ", ".join(map(str, repe))
        print(f'\nLos valores de los dados lanzados fueron: {cadena}')
        print('\nFin del programa')
        salir = True