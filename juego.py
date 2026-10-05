from enum import Enum

import random

from config import FILAS, COLUMNAS, FICHAS_PARA_GANAR

ROJO = "#ff0000"
AZUL = "#0000ff"

class Ficha(Enum):
    X = ROJO
    O = AZUL
    
    def siguiente(self):
        if self == self.X:
            return self.O
        if self == self.O:
            return self.X
        return None
    
class Tablero:
    
    def __init__(self):
        self.tablero = [[None] * COLUMNAS for _ in range(FILAS)]
            
    def jugar(self, ficha, fila, columna):
        if self.tablero[fila][columna] == None:
            self.tablero[fila][columna] = ficha
            return True
        return False
    
    def deshacer(self, fila, columna):
        """Deshace el movimiento en la posición especificada.
        
        Args:
            fila (int): La fila de la ficha a deshacer.
            columna (int): La columna de la ficha a deshacer.
        """
        self.tablero[fila][columna] = None
    
    def jugar_columna(self, ficha, columna):
        """Juega una ficha en la columna especificada, colocándola en la primera posición disponible desde abajo hacia arriba.
        
        Args:
            ficha (Ficha): La ficha que se va a colocar.
            columna (int): La columna en la que se desea colocar la ficha.
        
        Returns:
            tuple: La posición (fila, columna) donde se colocó la ficha, o None si la columna está llena o es inválida.
        """
        if not self.tablero or columna < 0 or columna >= len(self.tablero[0]):
            return None
        
        for fila in range(len(self.tablero) - 1, -1, -1):
            if self.tablero[fila][columna] is None:
                self.tablero[fila][columna] = ficha
                return fila, columna
            
        return None
    
    def jugar_acciones(self, fila, columna):
        if self.tablero[fila][columna] == None:
            if fila == FILAS - 1:
                return True
            if self.tablero[fila + 1][columna] is None:
                return False
            return True
        return False
    
    def esta_lleno(self):
        for linea in self.tablero:
            for ficha in linea:
                if ficha == None:
                    return False
        return True
    
    def gana(self, jugador):
        return self.gana_horizontal(jugador) or self.gana_vertical(jugador) or self.gana_diagonal_directa(jugador) or self.gana_diagonal_inversa(jugador)
    
    def gana_horizontal(self, jugador):
        """Determina si el jugador especificado ha ganado horizontalmente.

        Args:
            jugador (Ficha): El jugador a verificar.

        Returns:
            bool: True si el jugador ha ganado horizontalmente, False en caso contrario.
        """
        for indice_fila, linea in enumerate(self.tablero):
            consecutivas = []
            
            for indice_columna, ficha in enumerate(linea):
                if ficha == jugador:
                    consecutivas.append((indice_fila, indice_columna))
                    
                    if len(consecutivas) == FICHAS_PARA_GANAR:
                        self.fichas_ganadoras = consecutivas.copy()
                        return True
                else:
                    consecutivas = []
                    
        self.fichas_ganadoras = []
        return False
    
    def gana_vertical(self, jugador):
        """Determina si el jugador especificado ha ganado verticalmente.

        Args:
            jugador (Ficha): El jugador a verificar.

        Returns:
            bool: True si el jugador ha ganado verticalmente, False en caso contrario.
        """
        for columna in range(COLUMNAS):
            consecutivas = []
            
            for fila in range(FILAS):
                if self.tablero[fila][columna] == jugador:
                    consecutivas.append((fila, columna))
                    
                    if len(consecutivas) == FICHAS_PARA_GANAR:
                        self.fichas_ganadoras = consecutivas.copy()
                        return True
                else:
                    consecutivas = []
                    
        self.fichas_ganadoras = []
        return False
    
    def gana_diagonal_directa(self, jugador):
        """Determina si el jugador especificado ha ganado en una diagonal directa (de arriba a la izquierda a abajo a la derecha).

        Args:
            jugador (Ficha): El jugador a verificar.

        Returns:
            bool: True si el jugador ha ganado en una diagonal directa, False en caso contrario.
        """
        for fila in range(FILAS - FICHAS_PARA_GANAR + 1):
            for columna in range(COLUMNAS - FICHAS_PARA_GANAR + 1):
                celdas = [(fila + k, columna + k) for k in range(FICHAS_PARA_GANAR)]
                if all(self.tablero[f][c] == jugador for f, c in celdas):
                    self.fichas_ganadoras = celdas
                    return True
        self.fichas_ganadoras = []
        return False
    
    def gana_diagonal_inversa(self, jugador):
        """Determina si el jugador especificado ha ganado en una diagonal inversa (de abajo a la izquierda a arriba a la derecha).

        Args:
            jugador (Ficha): El jugador a verificar.

        Returns:
            bool: True si el jugador ha ganado en una diagonal inversa, False en caso contrario.
        """
        for fila in range(FICHAS_PARA_GANAR - 1, FILAS):
            for columna in range(COLUMNAS - FICHAS_PARA_GANAR + 1):
                celdas = [(fila - k, columna + k) for k in range(FICHAS_PARA_GANAR)]
                if all(self.tablero[f][c] == jugador for f, c in celdas):
                    self.fichas_ganadoras = celdas
                    return True
                
        self.fichas_ganadoras = []
        return False
    
    
class Partida:
    
    def __init__(self):
        self.tablero = Tablero()
        self.turno = random.choice(list(Ficha))
        
    def jugar(self, columna):
        """Juega una ficha en la columna especificada para el jugador cuyo turno es actual.
    
        Args:
            columna (int): La columna en la que se desea colocar la ficha.
    
        Returns:
            tuple: La posición (fila, columna) donde se colocó la ficha, o None si la columna está llena o es inválida.
        """
        movimiento = self.tablero.jugar_columna(self.turno, columna)
        if movimiento is not None:
            self.turno = self.turno.siguiente()
                
        return movimiento
                
    def terminada(self):
        """Determina si la partida ha terminado.

        Returns:
            bool: True si la partida ha terminado (ya sea por un ganador o porque el tablero está lleno), False en caso contrario.
        """
        return self.tablero.esta_lleno() or self.ganador() != None
        
    def ganador(self):
        """Determina el jugador ganador de la partida.

        Returns:
            Ficha: El jugador ganador, o None si no hay ganador.
        """
        for jugador in list(Ficha):
            if self.tablero.gana(jugador):
                return jugador
        return None