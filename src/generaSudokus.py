import os
import random

def obtener_siguiente_nombre_sudoku(carpeta, nombre_base="sudoku", extension=".txt"):
    numero = 1
    while True:
        nombre_archivo = f"{nombre_base}{numero}{extension}"
        ruta_archivo = os.path.join(carpeta, nombre_archivo)
        if not os.path.exists(ruta_archivo):
            return ruta_archivo
        numero += 1

def es_valido(tablero, fila, col, num):
    # Comprueba fila y columna
    for i in range(9):
        if tablero[fila][i] == num or tablero[i][col] == num:
            return False

    # Comprueba subcuadro 3x3
    inicio_fila = (fila // 3) * 3
    inicio_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if tablero[inicio_fila + i][inicio_col + j] == num:
                return False

    return True

def resolver_sudoku(tablero):
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                numeros = list(range(1, 10))
                random.shuffle(numeros)
                for num in numeros:
                    if es_valido(tablero, fila, col, num):
                        tablero[fila][col] = num
                        if resolver_sudoku(tablero):
                            return True
                        tablero[fila][col] = 0
                return False
    return True

def generar_sudoku_completo():
    tablero = [[0]*9 for _ in range(9)]
    resolver_sudoku(tablero)
    return tablero

def eliminar_casillas(tablero, cantidad=40):
    posiciones = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(posiciones)
    eliminadas = 0
    for i, j in posiciones:
        if eliminadas >= cantidad:
            break
        tablero[i][j] = 0
        eliminadas += 1
    return tablero

def guardar_sudoku_en_archivo(carpeta, cantidad_vacias=40):
    tablero = generar_sudoku_completo()
    tablero = eliminar_casillas(tablero, cantidad_vacias)

    ruta_archivo = obtener_siguiente_nombre_sudoku(carpeta)

    with open(ruta_archivo, "w") as f:
        for fila in tablero:
            linea = "".join(str(num) if num != 0 else " " for num in fila)
            f.write(linea + "\n")

    print(f"Sudoku incompleto válido guardado en: {ruta_archivo}")

# === Ejemplo de uso ===
carpeta_destino = "/Users/diego/Documents/GitHub/Resolucionador-Sudoku/sudokus"
guardar_sudoku_en_archivo(carpeta_destino)
