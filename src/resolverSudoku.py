# Alberto Pérez Álvarez
# Diego García Díaz
import sys

def getRuta():
    if len(sys.argv) < 2:
        print("NOTA: Puede pasarse la ruta al sudoku como parametro: python3 resolverSudoku.py <ruta/al/sudoku>\nSe usará el sudoku predefinido")
        return "sudokus/ejemplo.txt"
    return sys.argv[1]

def getSudoku(ruta):
    '''
    Devuelve un string del contenido del fichero en la ruta.
    '''
    try:
        f = open(ruta, "r")
        sudoku = f.read()
        f.close()
    except FileNotFoundError:
        print("No se ha podido leer el sudoku en ",ruta)
        sys.exit(1)
    return sudoku

def getListaSudoku(ruta):
    '''
    Devuelve una lista de listas con el sudoku[fila][columna].
    '''
    sudoku = getSudoku(ruta)
    sudoku = sudoku.split("\n")
    sudoku = [list(x) for x in sudoku if len(list(x)) == 9]
    if len(sudoku) != 9:
        print("ERROR: El sudoku dado no tiene el formato adecuado (9x9)")
        sys.exit(2)
    return sudoku

def compruebaFilas(numero, conjuntos, fila):
    """
    Devuelve true si el numero no existe en la fila dada.
    """
    return numero not in conjuntos[0][fila]

def compruebaColumnas(numero, conjuntos, columna):
    """
    Devuelve true si el numero no existe en la columna dada.
    """
    return numero not in conjuntos[1][columna]

def getCuadrante(fila, columna):
    """
    Devuelve el cuadrante de 0 a 8 en el que se esta.
    Las posiciones [0][0] a [0][2], [1][0] a [1][2] y [2][0] a [2][2] son del primer cuadrante
    Etc...
    """
    # Si el sudoku estuviese dividido por cuadrantes, seria un 3x3
    fila_cuadrante = fila // 3
    columna_cuadrante = columna // 3

    return fila_cuadrante * 3 + columna_cuadrante 

def compruebaCuadrantes(numero, conjuntos, cuadrante_index):
    """
    Devuelve true si el numero no existe en el cuadrante dado.
    """
    return numero not in conjuntos[2][cuadrante_index]

def creaConjuntos(sudoku):
    """
    Recorre el sudoku, devolviendo una lista con 3 listas, dentro de las cuales hay 9 sets.
    Correspondiendose con las filas, columnas y cuadrantes.
    """
    filas = [set() for _ in range(9)]
    columnas = [set() for _ in range(9)]
    cuadrantes = [set() for _ in range(9)]

    for fila_index, fila in enumerate(sudoku):
        for columna_index, elemento in enumerate(fila):
            if elemento != " ":
                filas[fila_index].add(elemento)
                columnas[columna_index].add(elemento)
                cuadrante_index = getCuadrante(fila_index, columna_index)
                cuadrantes[cuadrante_index].add(elemento)
    return [filas, columnas, cuadrantes]

def actualizaConjuntos(conjuntos, numero, fila, columna, cuadrante_index):
    """
    Actualiza el sudoku con el nuevo numero.
    """
    conjuntos[0][fila].add(numero)
    conjuntos[1][columna].add(numero)
    conjuntos[2][cuadrante_index].add(numero)
    return conjuntos

def borraElemConjunto(conjuntos, numero, fila, columna, cuadrante_index):
    """
    Borra el elemento de los conjuntos que correspondan.
    """
    conjuntos[0][fila].remove(numero)
    conjuntos[1][columna].remove(numero)
    conjuntos[2][cuadrante_index].remove(numero)
    return conjuntos

def getSolucionSudoku(sudoku, conjuntos, fila=0, columna=0):
    '''
    Devuelve el sudoku resuelto. Función recursiva de backtracking.
    '''
    siguiente_columna = (columna+1)%9
    if siguiente_columna == 0:
        siguiente_fila = (fila+1)%9
    else:
        siguiente_fila = fila
    
    if sudoku[fila][columna] != " ":    # Comprobamos que no hay ningún número donde queremos
        if fila == 8 and columna == 8:  # Si hay algún número y es el ultimo se devuelve tal cual
            return sudoku
        
        return getSolucionSudoku(sudoku, conjuntos, siguiente_fila, siguiente_columna) # Si no se continua

    else:
        numeros = ["1","2","3","4","5","6","7","8","9"]

        for numero in numeros:
            if (compruebaFilas(numero, conjuntos, fila) and compruebaColumnas(numero, conjuntos, columna)): # Comprobamos que no esté en filas, columnas
                cuadrante_index = getCuadrante(fila, columna)                   # Para evitar volver a calcular innecesariamente el cuadrante
                if compruebaCuadrantes(numero, conjuntos, cuadrante_index):     # Si tampoco está en los cuadrantes es un numero valido
                    sudoku[fila][columna] = numero                              # Actualizamos el sudoku y los conjuntos
                    actualizaConjuntos(conjuntos, numero, fila, columna, cuadrante_index)

                    if fila == 8 and columna == 8:                              # Si es el último elemento terminamos
                        return sudoku
                    
                    sol = getSolucionSudoku(sudoku, conjuntos, siguiente_fila, siguiente_columna)
                    
                    if sol != None:                                             # Si devuelve None es que no se ha encontrado solución
                        return sol
                    
                    sudoku[fila][columna] = " "                                 # Borramos el número pues no es posible llegar a una solución con él      
                    conjuntos = borraElemConjunto(conjuntos, numero, fila, columna, cuadrante_index)

        return None # Si termina el bucle es que no se ha encontrado solución para ningún número del 1 al 9

def printSudoku(sudoku):
    print("\n----------------------------------------------------")
    n_fila = 0
    for fila in sudoku:
        n_elemento = 0
        for elemento in fila:
            print(elemento, end="")
            n_elemento += 1
            if n_elemento % 3 == 0:
                print("  |  ", end="")
            else:
                print("  .  ", end="")
        if n_elemento != 9:
            print("ERROR: La fila no tiene 9 elementos")
            sys.exit(2)
        print("\n")
        n_fila += 1
        if n_fila % 3 == 0:
            print("----------------------------------------------------")
    if n_fila != 9:
        print("ERROR: El sudoku no tiene 9 filas")
        sys.exit(2)

def main():
    print("\n### Resolvedor de sudoku ###\n")
    print("Hecho por:\n -Alberto Pérez Álvarez\n -Diego García Díaz\n")

    ruta = getRuta()
    sudoku = getListaSudoku(ruta)
    print("\nSudoku a resolver en ", ruta, ":")
    printSudoku(sudoku)

    print("\nResolviendo sudoku...\n")
    conjuntos = creaConjuntos(sudoku)
    sudoku_resuelto = getSolucionSudoku(sudoku,conjuntos)
    if sudoku_resuelto == None:
        print("\nERROR: No se ha podido resolver el sudoku o no tiene solución")
        sys.exit(3)
    print("Sudoku resuelto:")
    printSudoku(sudoku_resuelto)

if __name__ == "__main__":
    main()