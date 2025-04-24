# Alberto Pérez Álvarez
# 
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
        print("El sudoku dado no tiene el formato adecuado (9x9)")
        sys.exit(2)
    return sudoku

def getSolucionSudoku():
    pass
# TODO: Hacer todas las funciones necesarias

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
        print("\n")
        n_fila += 1
        if n_fila % 3 == 0:
            print("----------------------------------------------------")


def main():
    print("\n### Resolvedor de sudoku ###\n")
    print("Hecho por:\n -Alberto Pérez Álvarez\n -\n")

    ruta = getRuta()
    sudoku = getListaSudoku(ruta)

    printSudoku(sudoku)

main()