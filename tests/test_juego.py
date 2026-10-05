import pytest

from juego import Ficha, Partida, Tablero

def tablero_con(fichas, ficha):
    """Crea un tablero con las fichas especificadas para el jugador dado."""
    t= Tablero()
    for fila, columna in fichas:
        t.tablero[fila][columna] = ficha
        
    return t

def test_tablero_vacio():
    """Prueba que un tablero recién creado esté vacío."""
    t = Tablero()
    
    assert len(t.tablero) == 6
    assert all(len(fila) == 7 for fila in t.tablero)
    assert not t.esta_lleno()
    
def test_gravedad():
    """Prueba que las fichas caen correctamente en la columna más baja disponible."""
    t = Tablero()
    
    assert t.jugar_columna(Ficha.X, 3) == (5, 3)
    assert t.jugar_columna(Ficha.O, 3) == (4, 3)
    
@pytest.mark.parametrize("columna", [7, -1])
def test_columna_invalida(columna):
    """Prueba que se devuelve None al intentar jugar en una columna inválida."""
    assert Tablero().jugar_columna(Ficha.X, columna) is None
    
def test_columna_llena():
    """Prueba que se devuelve None al intentar jugar en una columna llena."""
    t = Tablero()
    for _ in range(6):
        t.jugar_columna(Ficha.X, 0)
        
    assert t.jugar_columna(Ficha.X, 0) is None
    
def test_victoria_horizontal():
    """Prueba que se detecta correctamente una victoria horizontal."""
    t = Tablero()
    t.tablero[5] = [Ficha.X, None, Ficha.X, Ficha.X, Ficha.X, Ficha.X, None]
    
    assert t.gana_horizontal(Ficha.X)
    assert t.fichas_ganadoras == [(5, 2), (5, 3), (5, 4), (5, 5)]
    
def test_victoria_vertical():
    """Comprueba que se detecta correctamente una victoria vertical"""
    t = tablero_con([(1, 3), (2, 3), (3, 3), (4, 3)], Ficha.O)
    
    assert t.gana_vertical(Ficha.O)
    assert t.fichas_ganadoras == [(1, 3), (2, 3), (3, 3), (4, 3)]
    
def test_victoria_diagonal_directa():
    """Comprueba que se detecta correctamente una victoria en diagonal derecha"""
    t = tablero_con([(0, 0), (1, 1), (2, 2), (3, 3)], Ficha.X)
    
    assert t.gana_diagonal_directa(Ficha.X)
    assert t.fichas_ganadoras == [(0, 0), (1, 1), (2, 2), (3, 3)]
    
def test_victoria_diagonal_inversa():
    """Prueba que se detecta correctamente una victoria en diagonal izquierda"""
    t = tablero_con([(5, 0), (4, 1), (3, 2), (2, 3)], Ficha.O)
    
    assert t.gana_diagonal_inversa(Ficha.O)
    assert t.fichas_ganadoras == [(5, 0), (4, 1), (3, 2), (2, 3)]
    
def test_sin_victoria():
    """Prueba que no se detecta una victoria cuando el tablero está vacío."""
    assert not Tablero().gana(Ficha.X)
    
def test_empate():
    """Prueba que se detecta correctamente un empate cuando el tablero está lleno."""

    t = Tablero()
    t.tablero = [[Ficha.X] * 7 for _ in range(6)]
    
    assert t.esta_lleno()
    
def test_alternancia_de_turnos():
    """Prueba que el turno alterna correctamente entre los jugadores después de cada jugada."""
    p = Partida()
    p.turno = Ficha.X
    p.jugar(0)
    
    assert p.turno == Ficha.O
    p.jugar(1)
    assert p.turno == Ficha.X
    
def test_jugada_invalida_no_cambia_turno():
    """Prueba que una jugada inválida no cambia el turno del jugador."""
    p = Partida()
    p.turno = Ficha.X
    
    assert p.jugar(9) is None
    assert p.turno == Ficha.X
    
def test_ganador_y_partida_terminada():
    """Prueba que se detecta correctamente el ganador y que la partida se marca como terminada."""
    p = Partida()
    for fila in (2, 3, 4, 5):
        p.tablero.tablero[fila][0] = Ficha.X
        
    assert p.ganador() == Ficha.X
    assert p.terminada()
    