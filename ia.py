from juego import Ficha
from config import FILAS, COLUMNAS, FICHAS_PARA_GANAR, PROFUNDIDAD_APERTURA, PROFUNDIDAD_MAXIMA

POSICIONES = [
    (fila, columna) for fila in range(FILAS) for columna in range(COLUMNAS)
]
CASI_GANA = FICHAS_PARA_GANAR - 1

class InteligenciaArtificial:
    
    def __init__(self, tablero):
        self.tablero = tablero
        
    def ganador(self):
        """Determina el jugador ganador en el tablero actual.

        Returns:
            Ficha: El jugador ganador, o None si no hay ganador.
        """
        for jugador in Ficha:
            if self.tablero.gana(jugador):
                return jugador
            
        return None
    
    def terminada(self):
        """Determina si el juego ha terminado.

        Returns:
            bool: True si el juego ha terminado (ya sea por un ganador o porque el tablero está lleno), False en caso contrario.
        """
        return self.tablero.esta_lleno() or self.ganador() is not None
    
    def minmax(self, profundidad, maximo):
        """Implementación del algoritmo Minimax para determinar el mejor movimiento.

        Args:
            profundidad (int): La profundidad actual en el árbol de búsqueda.
            maximo (bool): True si es el turno del jugador máximo (IA), False si es el turno del jugador mínimo (humano).

        Returns:
            float: La puntuación evaluada del tablero.
        """
        fichas = 0
        # Contar el número de fichas en el tablero actual
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                if self.tablero.tablero[fila][col] is not None:
                    fichas += 1
        # Si el tablero está casi vacío y estamos en la profundidad de apertura, devolvemos 0.
        if fichas < COLUMNAS and profundidad == PROFUNDIDAD_APERTURA:
            return 0
        
        # Si hemos alcanzado la profundidad máxima, evaluamos el tablero.
        if profundidad == PROFUNDIDAD_MAXIMA:
            return self.valorar_tablero()
        
        # Si el juego ha terminado, devolvemos la puntuación correspondiente.
        if self.terminada():
            if self.ganador() == Ficha.O:
                return 1
            elif self.ganador() == Ficha.X:
                return -1
            return 0
        
        # Si no hemos alcanzado la profundidad máxima y el juego no ha terminado, continuamos con el algoritmo Minimax.
        if maximo:
            # Turno del jugador máximo (IA)
            mejorPuntuacion = float("-inf")
            # Iteramos sobre todas las acciones posibles para el jugador máximo.
            for movimiento in self.acciones():
                self.tablero.jugar(Ficha.O, movimiento[0], movimiento[1])
                # Realizamos el movimiento y evaluamos la puntuación resultante.
                puntuacion = self.minmax(profundidad + 1, False)
                self.tablero.deshacer(movimiento[0], movimiento[1])
                mejorPuntuacion = max(mejorPuntuacion, puntuacion)
                
                if puntuacion == 1:
                    return mejorPuntuacion
                
            return mejorPuntuacion
        # Turno del jugador mínimo (humano)
        else:
            mejorPuntuacion = float("inf")
            for movimiento in self.acciones():
                self.tablero.jugar(Ficha.X, movimiento[0], movimiento[1])
                puntuacion = self.minmax(profundidad + 1, True)
                self.tablero.deshacer(movimiento[0], movimiento[1])
                mejorPuntuacion = min(puntuacion, mejorPuntuacion)
                if puntuacion == -1:
                    return mejorPuntuacion
                
            return mejorPuntuacion
        
    def mejor_movimiento(self):
        """Devuelve el mejor movimiento posible para la IA utilizando el algoritmo Minimax."""
        mejor_valor = float("-inf")
        mejor_movimiento = None
        
        for movimiento in self.acciones():
            self.tablero.jugar(Ficha.O, movimiento[0], movimiento[1])
            valor = self.minmax(0, False)
            self.tablero.deshacer(movimiento[0], movimiento[1])
            
            if valor == 1:
                return movimiento
            
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento
        return mejor_movimiento
    
    def acciones(self):
        """Devuelve una lista de todas las acciones posibles (movimientos) para el jugador actual."""
        movimientos = []
        
        for posicion in POSICIONES:
            if self.tablero.jugar_acciones(posicion[0], posicion[1]):
                movimientos.append(posicion)
                
        movimientos.reverse() # Invertimos el orden de los movimientos para priorizar los últimos posibles.
        return movimientos
    
    def valorar_tablero(self):
        """Valora el tablero actual desde la perspectiva de la IA (Ficha.O)."""
        valor = 0
        
        for jugador in list(Ficha):
            valor += self.valorar_lineas(jugador)
            valor += self.valorar_columnas(jugador)
            valor += self.valorar_diagonales(jugador)
            
        return valor
        
    def valorar_lineas(self, jugador):
        """Valora las líneas del tablero para el jugador especificado.
        
            Args:
                jugador (Ficha): El jugador para el cual se valoran las líneas.
                
            Returns:
                float: La valoración de las líneas para el jugador especificado.
        
        """
        valor = 0
        resultado = 0
        
        for linea in self.tablero.tablero:
            valor = 0
            
            for idx, ficha in enumerate(linea):
                if ficha == jugador:
                    valor += 1
                    
                    if valor == CASI_GANA:
                        if idx + 1 < len(linea) and linea[idx + 1] == None:
                            resultado += 0.1
                            
                        if idx - CASI_GANA >= 0 and linea[idx - CASI_GANA] == None:
                            resultado += 0.1
                else:
                    valor = 0
                    
        if jugador == Ficha.O:
            return resultado
        
        else:
            return -resultado
            
    def valorar_columnas(self, jugador):
        """Valora las columnas del tablero para el jugador especificado.

            Args:
                jugador (Ficha): El jugador para el cual se valoran las columnas.
                
            Returns:
                float: La valoración de las columnas para el jugador especificado.
        
        """
        valor = 0
        resultado = 0
        tablero = self.tablero.tablero
        
        for col in range(COLUMNAS):
            valor = 0
            
            for fila in range(FILAS):
                if tablero[fila][col] == jugador:
                    valor += 1
                    
                    if valor == CASI_GANA:
                        if fila + 1 < FILAS and tablero[fila + 1][col] == None:
                            resultado += 0.1
                            
                        if fila - CASI_GANA >= 0 and tablero[fila - (CASI_GANA)][col] == None:
                            resultado += 0.1
                else:
                    valor = 0
                    
        if jugador == Ficha.O:
            return resultado
        
        else:
            return -resultado
                
    def valorar_diagonales(self, jugador):
        """Valora las diagonales del tablero para el jugador especificado.

            Args:
                jugador (Ficha): El jugador para el cual se valoran las diagonales.
                
            Returns:
                float: La valoración de las diagonales para el jugador especificado.
        
        """
        resultado = 0
        tablero = self.tablero.tablero
        
        for i in range(FILAS - CASI_GANA):
            for j in range(COLUMNAS - CASI_GANA):
                if (tablero[i][j] == jugador and tablero[i + 1][j + 1] == jugador
                    and tablero[i + 2][j + 2]):
                    if i + CASI_GANA < FILAS and j + CASI_GANA < COLUMNAS and tablero[i + CASI_GANA][j + CASI_GANA] == None:
                        resultado += 0.1
                        
                    if i - 1 >= 0 and j - 1 >= 0 and tablero[i - 1][j - 1] == None:
                        resultado += 0.1
                        
        for i in range(CASI_GANA, FILAS):
            for j in range(COLUMNAS - CASI_GANA):
                if (tablero[i][j] == jugador and tablero[i - 1][j + 1] == jugador
                    and tablero[i - 2][j + 2]):
                    if i - CASI_GANA >= 0 and j + (CASI_GANA) < COLUMNAS and tablero[i - CASI_GANA][j + CASI_GANA] == None:
                        resultado += 0.1
                        
                    if i + 1 < FILAS and j - 1 >= 0 and tablero[i + 1][j - 1] == None:
                        resultado += 0.1
                        
        if jugador == Ficha.O:
            return resultado
        
        else:
            return -resultado