# Alberto Pérez Álvarez
# Diego García Díaz
import sys

def getRuta():
    if len(sys.argv) < 2:
        print("NOTA: Puede pasarse la ruta como parametro: python3 main.py <ruta/al/sudoku>\nSe usará el sudoku predefinido")
        return "sudokus/test.txt"
    return sys.argv[1]

def getSudoku(ruta):
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
    Devuelve una lista de listas con el sudoku[fila][columna]
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
    Devuelve true si el numero no existe en la fila dada
    """
    return numero not in conjuntos[0][fila]

def compruebaColumnas(numero, conjuntos, columna):
    """
    Devuelve true si el numero no existe en la columna dada
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

def compruebaCuadrantes(numero, conjuntos, fila, columna, cuadrante_index):
    """
    Devuelve true si el numero no existe en el cuadrante dado
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
    Actualiza el sudoku con el nuevo numero
    """
    conjuntos[0][fila].add(numero)
    conjuntos[1][columna].add(numero)
    conjuntos[2][cuadrante_index].add(numero)
    return conjuntos

def borraElemConjunto(conjuntos, numero, fila, columna, cuadrante_index):
    """
    Borra el elemento de los conjuntos que correspondan
    """
    conjuntos[0][fila].remove(numero)
    conjuntos[1][columna].remove(numero)
    conjuntos[2][cuadrante_index].remove(numero)
    return conjuntos


def getSolucionSudoku(sudoku, conjuntos, fila=0, columna=0):
    nueva_columna = (columna+1)%9
    if nueva_columna == 0:
        nueva_fila = (fila+1)%9
    else:
        nueva_fila = fila
    
    if sudoku[fila][columna] != " ": # Comprobamos que no hay nada donde queremos
        if fila == 8 and columna == 8: # Si hay algo y es el ultimo se devuelve tal cual
            return sudoku
        
        return getSolucionSudoku(sudoku, conjuntos, nueva_fila, nueva_columna) # Si no se continua

    else:
        numeros = ["1","2","3","4","5","6","7","8","9"]

        for numero in numeros:
            if (compruebaFilas(numero, conjuntos, fila) and compruebaColumnas(numero, conjuntos, columna)):
                cuadrante_index = getCuadrante(fila, columna)
                if compruebaCuadrantes(numero, conjuntos, fila, columna, cuadrante_index): #Es un numero valido
                    sudoku[fila][columna] = numero #Actualizamos el sudoku
                    actualizaConjuntos(conjuntos, numero, fila, columna, cuadrante_index)

                    if fila == 8 and columna == 8:
                        return sudoku
                    
                    sol = getSolucionSudoku(sudoku, conjuntos, nueva_fila, nueva_columna)
                    
                    if sol != None:
                        return sol
                    
                    sudoku[fila][columna] = " "
                    conjuntos = borraElemConjunto(conjuntos, numero, fila, columna, cuadrante_index)

        return None

def printSudoku(sudoku):
    if sudoku == None:
        print("\nERROR: No se ha podido resolver el sudoku o No tiene solución")
        return 3
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
            return 1
        print("\n")
        n_fila += 1
        if n_fila % 3 == 0:
            print("----------------------------------------------------")
    if n_fila != 9:
        print("ERROR: El sudoku no tiene 9 filas")
        return 2

def main():
    print("\n### Resolvedor de sudoku ###\n")
    print("Hecho por:\n -Alberto Pérez Álvarez\n -Diego García Díaz\n")

    ruta = getRuta()
    sudoku = getListaSudoku(ruta)
    printSudoku(sudoku)

    conjuntos = creaConjuntos(sudoku)
    sudoku_resuelto = getSolucionSudoku(sudoku,conjuntos)
    printSudoku(sudoku_resuelto)

if __name__ == "__main__":
    main()