from ia import InteligenciaArtificial
from juego import Ficha, Tablero

def copia(tablero):
    """Crea una copia del tablero dado."""
    return [fila[:] for fila in tablero.tablero]

def test_ia_elige_movimiento_legal():
    """Prueba que la IA elige un movimiento legal."""
    t = Tablero()
    ia = InteligenciaArtificial(t)
    fila, columna = ia.mejor_movimiento()
    
    assert t.jugar_acciones(fila, columna)
    
def test_ia_no_modifica_tablero():
    """Prueba que la IA no modifica el tablero al calcular el mejor movimiento."""
    t = Tablero()
    t.jugar_columna(Ficha.X, 3)
    antes = copia(t)
    InteligenciaArtificial(t).mejor_movimiento()
    
    assert t.tablero == antes
    
def test_ia_gana_si_puede():
    """Prueba que la IA elige el movimiento que le permite ganar si es posible."""
    t = Tablero()
    for _ in range(3):
        t.jugar_columna(Ficha.O, 2)
        
    t.jugar_columna(Ficha.X, 4)
    t.jugar_columna(Ficha.X, 5)
    
    assert InteligenciaArtificial(t).mejor_movimiento() == (2, 2)
    
def test_acciones_solo_devuelve_casillas_jugables():
    """Prueba que el método acciones de la IA solo devuelve casillas jugables."""
    t = Tablero()
    t.jugar_columna(Ficha.X, 0)
    ia = InteligenciaArtificial(t)
    acciones = ia.acciones()
    
    assert (4, 0) in acciones
    assert (5, 0) not in acciones
    assert len(acciones) == 7
    
def test_ia_bloquea_diagonal_inversa():
    tablero = Tablero()
    tablero.jugar(Ficha.X, 5, 0)
    tablero.jugar(Ficha.X, 4, 1)
    tablero.jugar(Ficha.X, 3, 2)
    tablero.jugar(Ficha.O, 5, 1)
    tablero.jugar(Ficha.O, 5, 2)
    tablero.jugar(Ficha.O, 4, 2)
    ia = InteligenciaArtificial(tablero)
    assert ia.valorar_diagonales(Ficha.X) != 0
    
        