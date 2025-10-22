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

class Casilla(Enum):
    AGUA = "O"
    TOCADO = "X"
    INCOGNITA = " "

class Barco:

    def __init__(self, eslora: int, letra_columna_top_left: str, numero_fila_top_left: int, orientacion: Orientacion):
        # En caso de ser necesario, podemos hacer primero la verificación de que los valores son válidos; asumiremos que este constructor se llama con valores válidos

        self.eslora = eslora
        # self.letra_columna_top_left = letra_columna_top_left
        # self.numero_fila_top_left = numero_fila_top_left
        # self.orientacion = orientacion

        indice_top_left = [Utils.get_indice_fila(numero_fila_top_left), Utils.get_indice_columna(letra_columna_top_left)]
        tupla_indice_top_left = tuple(indice_top_left)

        self.posiciones_en_tablero = [tupla_indice_top_left]
        self.posiciones_tocadas_en_tablero = [False]

        for i in range(1, eslora):
            if orientacion == Orientacion.HORIZONTAL:
                nueva_tupla_indice = ((indice_top_left[0] + i, indice_top_left[1]))
                self.posiciones_en_tablero.append(nueva_tupla_indice)

            elif orientacion == Orientacion.VERTICAL:
                nueva_tupla_indice = ((indice_top_left[0], indice_top_left[1] + i))
                self.posiciones_en_tablero.append(nueva_tupla_indice)
                
            self.posiciones_tocadas_en_tablero.append(False) # En la creación ningún barco está tocado



        # Convertir letra_columna_top_left y numero_fila_top_left en índices indexados a cero, y casillas en modo índice

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
    tablero: np.array
    barcos: list[Barco]
    tamano_tablero: int

    def __init__(self, tamano_tablero: int):
        ## TODO: first check int type

        # Check valid size
        if Constants.TAMANO_MINIMO_TABLERO > tamano_tablero > Constants.TAMANO_MAXIMO_TABLERO:
            raise Exception(f"El tamaño del tablero debe estar comprendido entre {Constants.TAMANO_MINIMO_TABLERO} y {Constants.TAMANO_MAXIMO_TABLERO} (ambos incluidos)")
        
        self.tamano_tablero = tamano_tablero
        self.tablero = np.full((tamano_tablero,tamano_tablero), " ", dtype=object)

    def get_coordenadas_sin_disparo(self):
        pass

    def set_disparo(self, disparo: Disparo):
        return "AGUA!!" # TOCADO!! / HUNDIDO!!

    def set_barcos_aleatoriamente(self):
        ## Nos aseguramos de añadir primero los barcos de mayor eslora; si los dejamos para el final puede que no nos entren
        eslora_de_barcos_a_crear = sorted(Constants.ESLORA_DE_LOS_BARCOS_DE_UNA_PARTIDA, reverse = True)

        for eslora in eslora_de_barcos_a_crear:
            while True: ## Repetir hasta encontrar un barco que entre en el tablero
                barco_aleatorio = Utils.get_barco_aleatorio(eslora, self.tamano_tablero)

                try:
                    self.add_barco(barco_aleatorio)
                    break ## Salir del bucle while para 
                except:
                    pass

    def get_quedan_barcos_por_hundir(self) -> bool:
        return True # TODO
    
    def get_representacion_tablero_para_el_oponente(self) -> np.array:
        pass

    def get_representacion_tablero_defendido(self) -> np.array:
        pass

    def get_representacion_tablero_original(self) -> np.array:
        vector_letras_columnas = self.get_vector_letras_columnas()
        array_2d_numeros_fila = self.get_array_2d_numeros_filas()

        tablero_con_columnas = np.vstack([vector_letras_columnas, self.tablero])
        tablero_con_filas_y_columnas = np.hstack([array_2d_numeros_fila, tablero_con_columnas])

        return tablero_con_filas_y_columnas
    
    def get_vector_letras_columnas(self):
        return np.array(Constants.COLUMNAS_PERMITIDAS[0:self.tamano_tablero])
    
    def get_array_2d_numeros_filas(self):
        vector_numeros_fila = np.arange(0,self.tamano_tablero+1)
        vector_numeros_fila = vector_numeros_fila.astype(str) ## convierte el vector de int a vector de str
        if len(vector_numeros_fila) > 10:
            vector_numeros_fila = np.char.zfill(vector_numeros_fila, 2)  # Añade un 0 por la izquierda a las filas hasta el 9 para que todas las filas se muestren con 2 dígitos
            vector_numeros_fila[vector_numeros_fila == "00"] = "  " # Reemplaza el "00" por dos espacios (acabará siendo la casilla top_left)
        else:
            vector_numeros_fila[vector_numeros_fila == "0"] = " " # Reemplaza el "0" por un espacio (acabará siendo la casilla top_left)

        return vector_numeros_fila.reshape(-1,1) ## retorna los valores en un array bidimensional de 1 columna

    def add_barco(self, barco: Barco):
        tablero_temporal = self.tablero.copy()
        for fila_index,columna_index in barco.posiciones_en_tablero:
            try:
                contenido_casilla = tablero_temporal[fila_index][columna_index] ## elevará excepción si no existe en el tablero; puede ocurrir cuando se intenta meter un barco de eslora grande con un punto de origen muy debajo a la derecha
                if isinstance(contenido_casilla, type(Barco)):
                    raise Exception(f"Ya existe un barco en la posición ({fila_index},{columna_index})")
                    
                tablero_temporal[fila_index][columna_index] = barco

            except Exception as e:
                print ("sssssssssssssssssss:", e) # TODO: remove
                raise Exception('Este barco no entra en el tablero') # pasará habitualmente cuando estemos añadiendo barcos aleatorios

        # si llegamos hasta aquí es porque hemos podido añadir el barco entero, así que asignamos tablero_temporal al tablero real
        self.tablero = tablero_temporal
        


class Utils:
    import random

    def get_disparo_jugador(tamano_tablero: int):
        while True:
            columna_a_disparar = input("Introduce la letra de la columna a la que disparar (A, B, C, ...):")
            fila_a_disparar = input("Introduce el número de la fila a la que disparar (1, 2, 3, ...):")

            try:
                disparo = Disparo(tamano_tablero, columna_a_disparar, fila_a_disparar)
                return disparo
            except Exception as e:
                print(f"{e} - Por favor, inténtalo de nuevo")

    def get_disparo_maquina(tablero_jugador: Tablero):
        coordenadas_sin_disparo = tablero_jugador.get_coordenadas_sin_disparo()
        coordenada_disponible_random =  Utils.random.choice(coordenadas_sin_disparo)
        letra_columna, numero_fila = coordenada_disponible_random

        ## Asumimos que aquí no obtendremos una excepción ya que hemos elegido entre las coordenadas que el tablero nos indica están libres
        return Disparo(tablero_jugador.tamano_tablero, letra_columna, numero_fila)
    
    def get_indice_columna(letra_columna: str):
        return Constants.COLUMNAS_PERMITIDAS.index(letra_columna)
    
    def get_indice_fila(numero_fila: int):
        return numero_fila - 1
    
    def get_barco_aleatorio(eslora: int, tamano_tablero: int):
        valores_de_columna_posibles = Constants.COLUMNAS_PERMITIDAS[0:tamano_tablero]
        valores_de_fila_posibles = list(range(1,tamano_tablero+1))

        return Barco(
            eslora,
            random.choice(valores_de_columna_posibles),
            random.choice(valores_de_fila_posibles),
            random.choice(list(Orientacion))
        )


while True:
    tamano_tablero = input("Introduce el tamaño del tablero:")
    try:
        tamano_tablero_int = int(tamano_tablero) # Raises exception if can't be converted
        tablero_jugador = Tablero(tamano_tablero_int) # Raises exception if not valid
        break
    except Exception as e:
        print("Inténtalo de nuevo, el valor introducido no es válido:", e)

print(tablero_jugador.get_representacion_tablero_original())

tablero_jugador.set_barcos_aleatoriamente()

tablero_maquina = Tablero(tamano_tablero_int) # Raises exception if not valid
tablero_maquina.set_barcos_aleatoriamente()

partida_terminada = False
turno_count = 0

while True:
    turno_count += 1
    print(f"TURNO '{turno_count}'")
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

    ## Turno del jugador:
    disparo_jugador = Utils.get_disparo_jugador(tamano_tablero_int)
    resultado = tablero_maquina.set_disparo(disparo_jugador)
    print(f"{resultado} - Tu tablero de ataque queda así:")
    print(tablero_maquina.get_representacion_tablero_para_el_oponente())
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

