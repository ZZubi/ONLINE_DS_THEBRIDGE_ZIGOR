
from enum import Enum
import random
import numpy as np

class Constants:
    COLUMNAS_PERMITIDAS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    TAMANO_MINIMO_TABLERO = 6
    TAMANO_MAXIMO_TABLERO = len(COLUMNAS_PERMITIDAS)
    ESLORA_DE_LOS_BARCOS_DE_UNA_PARTIDA = [4, 3, 3, 2, 2, 2]

class Orientacion(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class Barco:

    def __init__(self, eslora: int, letra_columna_top_left: str, numero_fila_top_left, orientacion: Orientacion):
        # En caso de ser necesario, podemos hacer primero la verificación de que los valores son válidos; asumiremos que este constructor se llama con valores válidos

        self.eslora = eslora
        self.letra_columna_top_left = letra_columna_top_left
        self.numero_fila_top_left = numero_fila_top_left
        self.orientacion = orientacion

class Disparo:
    letra_columna: str = None
    numero_fila: int = None

    def __init__(self, tamano_tablero: int, letra_columna: str, numero_fila: int):
        posibles_columnas_para_tamano_tablero = Constants.COLUMNAS_PERMITIDAS[0:len(tamano_tablero)]

        if not isinstance(tamano_tablero, int):
            raise Exception("tamano_tablero debe ser un valor entero")
        elif  Constants.TAMANO_MINIMO_TABLERO > tamano_tablero > Constants.TAMANO_MAXIMO_TABLERO:
            raise Exception(f"El tamaño del tablero debe estar comprendido entre {Constants.TAMANO_MINIMO_TABLERO} y {len(Constants.TAMANO_MAXIMO_TABLERO)}")
        elif not isinstance(letra_columna, str):
            raise Exception("La columna debe ser numérica")
        ## TODO: añadir validaciones

        self.letra_columna = letra_columna
        self.numero_fila = numero_fila

class Tablero:
    tablero: np._Array
    barcos: list[Barco]
    tamano_tablero: int

    def __init__(self, tamano_tablero: int):
        ## TODO: first check int type
        # Check valid size
        if Constants.TAMANO_MINIMO_TABLERO > tamano_tablero > Constants.TAMANO_MAXIMO_TABLERO:
            raise Exception(f"El tamaño del tablero debe estar comprendido entre {Constants.TAMANO_MINIMO_TABLERO} y {Constants.TAMANO_MAXIMO_TABLERO} (ambos incluidos)")
        
        self.tamano_tablero = tamano_tablero
        self.tablero = np.full((tamano_tablero,tamano_tablero), " ")

    def get_coordenadas_sin_disparo(self):
        pass

    def set_disparo(self, disparo: Disparo):
        return "AGUA!!" # TOCADO!! / HUNDIDO!!

    def set_barcos_aleatoriamente(self):
        ## Nos aseguramos de añadir primero los barcos de mayor eslora; si los dejamos para el final puede que no nos entren
        eslora_de_barcos_a_crear = sorted(Constants.ESLORA_DE_LOS_BARCOS_DE_UNA_PARTIDA, reverse = True)

        for eslora in eslora_de_barcos_a_crear:
            while True: ## Repetir hasta encontrar un barco que entre en el tablero
                barco_aleatorio = Utils.get_barco_aleatorio(eslora, tamano_tablero)

                try:
                    self.add_barco(barco_aleatorio)
                    break ## Salir del bucle while para 
                except:
                    pass

    def get_quedan_barcos_por_hundir(self) -> bool:
        return True # TODO
    
    def get_representacion_tablero_atacado(self) -> list:
        pass

    def get_representacion_tablero_defendido(self) -> list:
        pass

    def add_barco(self, barco: Barco):
        tablero_temporal = self.tablero.copy()
        columna_top_left_index = Utils.get_indice_columna(barco.letra_columna_top_left)
        fila_top_left_index = Utils.get_indice_fila(barco.numero_fila_top_left)

        contenido_coordenada_top_left = tablero_temporal[][] ## Elevará una excepción si la casilla no existe


    

class Utils:
    import random

    def get_disparo_jugador(self, tamano_tablero: int):
        while True:
            columna_a_disparar = input("Introduce la letra de la columna a la que disparar (A, B, C, ...):")
            fila_a_disparar = input("Introduce el número de la fila a la que disparar (1, 2, 3, ...):")

            try:
                disparo = Disparo(tamano_tablero, columna_a_disparar, fila_a_disparar)
                return disparo
            except Exception as e:
                print(f"{e} - Por favor, inténtalo de nuevo")

    def get_disparo_maquina(self, tablero_jugador: Tablero):
        coordenadas_sin_disparo = tablero_jugador.get_coordenadas_sin_disparo()
        coordenada_disponible_random =  Utils.random.choice(coordenadas_sin_disparo)
        letra_columna, numero_fila = coordenada_disponible_random

        ## Asumimos que aquí no obtendremos una excepción ya que hemos elegido entre las coordenadas que el tablero nos indica están libres
        return Disparo(tablero_jugador.tamano_tablero, letra_columna, numero_fila)
    
    def get_indice_columna(self, letra_columna: str):
        return Constants.COLUMNAS_PERMITIDAS.index(letra_columna)
    
    def get_indice_fila(self, numero_fila: int):
        return numero_fila - 1
    
    def get_barco_aleatorio(eslora: int, tamano_tablero: int):
        valores_de_columna_posibles = Constants.COLUMNAS_PERMITIDAS[0:tamano_tablero]
        valores_de_fila_posibles = list(range[1:tamano_tablero+1])

        return Barco(
            eslora,
            random.choice(valores_de_columna_posibles),
            random.choice(valores_de_fila_posibles),
            random.choice(list(Orientacion))
        )



tamano_tablero = input("Introduce el tamaño del tablero:")

tablero_jugador = Tablero(tamano_tablero) # Raises exception if not valid
tablero_jugador.set_barcos_aleatoriamente()

tablero_maquina = Tablero(tamano_tablero) # Raises exception if not valid
tablero_maquina.set_barcos_aleatoriamente()

partida_terminada = False
turno_count = 0

while True:
    turno_count += 1
    print(f"TURNO '{turno_count}'")
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

    ## Turno del jugador:
    disparo_jugador = Utils.get_disparo_jugador(tamano_tablero)
    resultado = tablero_maquina.set_disparo(disparo_jugador)
    print(f"{resultado} - Tu tablero de ataque queda así:")
    print(tablero_maquina.get_representacion_tablero_atacado())
    print('________________________________________________________________________________________________')

    if (not tablero_maquina.get_quedan_barcos_por_hundir()):
        print("HAS GANADO!!! Este era el tablero original de tu oponente:")
        print(tablero_maquina.get_representacion_tablero_original())
        break

    ## Turno de la máquina:
    disparo_maquina = Utils.get_disparo_maquina(tablero_jugador)
    resultado = tablero_jugador.set_disparo(disparo_maquina)
    print(f"Tu oponente ha disparado a la coordenada {disparo_maquina.letra_columna} {disparo_maquina.numero_fila}")
    print(f"El resultado ha sido {resultado} - Tu tablero de defensa queda así:")
    print(tablero_jugador.get_representacion_tablero_defendido())
    print('________________________________________________________________________________________________')

    if (not tablero_jugador.get_quedan_barcos_por_hundir()):
        print("HAS PERDIDO!!! Este era el tablero original de tu oponente:")
        print(tablero_maquina.get_representacion_tablero_original())
        break

