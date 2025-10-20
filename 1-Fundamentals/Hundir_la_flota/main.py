class Constants:
    COLUMNAS_VALIDAS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    TAMANO_MINIMO_TABLERO = 6
    TAMANO_MAXIMO_TABLERO = len(COLUMNAS_VALIDAS)


class Disparo:
    columna:str = None
    fila:int = None

    def __init__(self, tamano_tablero:int, columna:str, fila:int):
        posibles_columnas_para_tamano_tablero = Constants.POSIBLES_COLUMNAS[0:len(tamano_tablero)]

        if not isinstance(tamano_tablero, int):
            raise Exception("tamano_tablero debe ser un valor entero")
        elif  Constants.TAMANO_MINIMO_TABLERO > tamano_tablero > Constants.TAMANO_MAXIMO_TABLERO:
            raise Exception(f"El tamaño del tablero debe estar comprendido entre {Constants.TAMANO_MINIMO_TABLERO} y {len(Constants.TAMANO_MAXIMO_TABLERO)}")
        elif not isinstance(columna, str):
            raise Exception("La columna debe ser numérica")
        ## TODO: añadir validaciones


        self.columna = columna
        self.fila = fila

tamano_tablero = input("Introduce el tamaño del tablero:")

tablero_jugador = Tablero() # Raise exception if not valid
tablero_jugador.crear_tablero(tamano_tablero)
tablero_jugador.colocar_barcos_aleatoriamente()

tablero_maquina = Tablero()
tablero_maquina.crear_tablero(tamano_tablero)
tablero_maquina.colocar_barcos_aleatoriamente()

partida_terminada = False

while not partida_terminada:
    ## Turno del jugador:
    casilla_a_disparar = input("Introduce la coordenada en la que disparar:")