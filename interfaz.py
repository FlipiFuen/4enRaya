import tkinter as tk
import random

from tkinter import messagebox

from juego import Ficha, Partida
from ia import InteligenciaArtificial
from config import(
    MSG_EMPATADO as EMPATADO,
    MSG_EMPATE as EMPATE,
    MSG_GANADOR as GANADOR,
    MSG_INICIO as INICIO,
    MSG_OCUPADA as OCUPADA,
    MSG_TERMINADA as TERMINADA,
    MSG_TURNO as TURNO,
    TITULO,
    FILAS,
    COLUMNAS,
    COLOR_TABLERO,
    COLOR_HUECO,
    COLOR_FICHA_X,
    COLOR_FICHA_O,
    COLOR_GANADOR,
    COLOR_FONDO,
    COLOR_TEXTO,
    COLOR_TEXTO_SECUNDARIO,
    FUENTE_TITULO,
    FUENTE_ESTADO,
    TAM_CASILLA,
    MARGEN_FICHA,
    VELOCIDAD_CAIDA,
    FPS_CAIDA,
)

class Ventana(tk.Frame):
    def __init__(self, ventana):
        super().__init__(ventana)
        self.ventana = ventana
        self.partida = None
        self.tablero_grafico = None
        self.menu = tk.Menu(self.ventana)
        self.ventana.config(menu=self.menu)
        self.menu.add_command(label="Salir", command=self.ventana.quit)
        self.menu.add_command(label="Nueva Partida", command=self.partida_nueva)
        self.ventana.config(bg=COLOR_FONDO)
        self.config(bg=COLOR_FONDO)
        self.bienvenida = tk.Label(self, text=TITULO, font=FUENTE_TITULO,
                                   fg=COLOR_TEXTO, bg=COLOR_FONDO)
        self.bienvenida.pack(pady=(20, 5))
        self.jugar = tk.Button(
            self, text="Jugar", font=FUENTE_ESTADO, fg=COLOR_TEXTO,
            bg=COLOR_TABLERO, activebackground=COLOR_TABLERO,
            activeforeground=COLOR_TEXTO, relief="flat",
            padx=24, pady=6, cursor="hand2",
            command=self.partida_nueva
        )
        self.jugar.pack(pady=(0, 10))
        self.pack(fill="both", expand=True)
        
    def partida_nueva(self):
        if self.tablero_grafico is not None:
            self.tablero_grafico.destroy()
            
        self.partida = Partida()
        self.tablero_grafico = Tablero_grafico(self.partida, self)
        self.tablero_grafico.juego_pc = JugadasPC(self.tablero_grafico, self.partida)
         
    
class Tablero_grafico(tk.Frame):
    
    def __init__(self, partida, ventana):
        self.partida = partida
        self.ventana = ventana
        super().__init__(ventana)
        self.config(bg=COLOR_FONDO)
        self.pack()
        self.listener = JugadasListener(partida, self)
        self.tablero_canvas = TableroCanvas(self, partida, self.listener)
        self.ocupado = False
        self.barra_estado = tk.Label(self, font=FUENTE_ESTADO, fg=COLOR_TEXTO, bg=COLOR_FONDO)
        if self.partida.turno == Ficha.X:
            self.barra_estado.config(text= INICIO.format(partida.turno.name))
        else:
            aleatorio = random.randint(0, COLUMNAS - 1)
            movimiento = self.partida.jugar(aleatorio)
            if movimiento is not None:
                self.jugar(movimiento[0], movimiento[1], Ficha.O)
            self.barra_estado.config(text= TURNO.format(Ficha.X.name))
        self.barra_estado.pack()
        self.barra_pensar = tk.Label(self, font=FUENTE_ESTADO, fg=COLOR_TEXTO_SECUNDARIO, bg=COLOR_FONDO)
        self.barra_pensar.pack()
        
    def actualizar_estado(self, mensaje):
        self.barra_estado.config(text = mensaje)
        
    def mostrar_resultado(self, jugador):
        """Muestra el resultado de la partida."""
        partida = self.partida
        if partida.ganador() is not None:
            self.actualizar_estado(GANADOR.format(jugador.name))
            self.mostrar_fichas_ganadoras()
        elif partida.terminada():
            self.actualizar_estado(EMPATE)
            messagebox.showinfo("Fin del Juego", EMPATADO)
        else:
            self.actualizar_estado(TURNO.format(partida.turno.name))
        
    def jugar(self, fila, columna, jugador, al_terminar=None):
        """Realiza una jugada en el tablero gráfico.

        Args:
            fila: La fila donde se coloca la ficha.
            columna: La columna donde se coloca la ficha.
            jugador: El jugador que realiza la jugada.
            al_terminar: Función a ejecutar al terminar la animación de la jugada.
        """
        self.ocupado = True
        
        def terminar():
            self.ocupado = False
            if al_terminar:
                al_terminar()
                
        self.tablero_canvas.animar_caida(fila, columna, jugador, terminar)
        
    def mostrar_fichas_ganadoras(self):
        self.tablero_canvas.dibujar()
        
class TableroCanvas(tk.Canvas):
    
    def __init__(self, master, partida, listener):
        self.partida = partida
        self.listener = listener
        ancho = COLUMNAS * TAM_CASILLA
        alto = FILAS * TAM_CASILLA
        
        super().__init__(
            master,
            width=ancho,
            height=alto,
            bg=COLOR_FONDO,
            highlightthickness=0,
        )
        self.pack(padx=12, pady=12)
        self.bind("<Button-1>", self.pulsar)
        self.bind("<Motion>", self.mover_raton)
        self.bind("<Leave>", self.salir_raton)
        self.columna_hover = None
        self.animado = None
        self.dibujar()
        
    def dibujar(self):
        """Dibuja el tablero y las fichas en el canvas."""
        self.delete("all")
        ancho = COLUMNAS * TAM_CASILLA
        alto = FILAS * TAM_CASILLA
        self.create_rectangle(
            0, 0, ancho, alto,
            fill=COLOR_TABLERO,
            outline=COLOR_TABLERO
        )
        if self.columna_hover is not None and self.partida.turno == Ficha.X and not self.partida.terminada():
            self.create_rectangle(
                self.columna_hover * TAM_CASILLA, 0,
                (self.columna_hover + 1) * TAM_CASILLA, alto,
                fill="#2a6fe0", outline="",
            )
        ganadoras = getattr(self.partida.tablero, "fichas_ganadoras", [])
        
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                x = columna * TAM_CASILLA + TAM_CASILLA / 2
                y = fila * TAM_CASILLA + TAM_CASILLA / 2
                radio = TAM_CASILLA / 2 - MARGEN_FICHA
                ficha = self.partida.tablero.tablero[fila][columna]
                
                if (fila, columna) == self.animado:
                    ficha = None
                
                if ficha == Ficha.X:
                    color = COLOR_FICHA_X
                elif ficha == Ficha.O:
                    color = COLOR_FICHA_O
                else:
                    color = COLOR_HUECO
                    
                ganadora = (fila, columna) in ganadoras
                self.create_oval(
                    x - radio,
                    y - radio,
                    x + radio,
                    y + radio,
                    fill=color,
                    outline=COLOR_GANADOR if ganadora else COLOR_HUECO,
                    width=5 if ganadora else 1,
                )
                
    def animar_caida(self, fila, columna, ficha, al_terminar=None):
        """Anima la caída de una ficha hasta su casilla y llama a al_terminar"""
        self.animado = (fila, columna)
        self.dibujar()
        radio = TAM_CASILLA / 2 - MARGEN_FICHA
        x = columna * TAM_CASILLA + TAM_CASILLA / 2
        y_final = fila * TAM_CASILLA + TAM_CASILLA / 2
        color = COLOR_FICHA_X if ficha == Ficha.X else COLOR_FICHA_O
        y = -radio
        id_ficha = self.create_oval(
            x - radio, y - radio, x + radio, y + radio,
            fill=color, outline=COLOR_HUECO,
        )
        
        def paso():
            if not self.winfo_exists():
                return
            
            centro = (self.coords(id_ficha)[1] + self.coords(id_ficha)[3]) / 2
            avance = min(VELOCIDAD_CAIDA, y_final - centro)
            if avance <= 0:
                self.animado = None
                self.dibujar()
                if al_terminar:
                    al_terminar()
                return
            
            self.move(id_ficha, 0, avance)
            self.after(FPS_CAIDA, paso)
            
        paso()
                
    def pulsar(self, evento):
        """Maneja el evento de pulsar el mouse en el canvas.
        
        Args:
            evento: El evento de pulsar el mouse.
        """
        ancho = COLUMNAS * TAM_CASILLA
        if 0 <= evento.x < ancho:
            columna = int(evento.x // TAM_CASILLA)
            self.listener.pulsar(FILAS - 1, columna)
            
    def mover_raton(self, evento):
        """Actualiza la columna sobre la que está el ratón"""
        columna = int(evento.x // TAM_CASILLA)
        if not 0 <= columna < COLUMNAS:
            columna = None
            
        if columna != self.columna_hover:
            self.columna_hover = columna
            if self.animado is None:
                self.dibujar()
            
    def salir_raton(self, evento):
        self.columna_hover = None
        if self.animado is None:
            self.dibujar()
        
class JugadasListener:
    """Clase que maneja las jugadas del jugador humano."""
    def __init__(self, partida, gui):
        self.partida = partida
        self.gui = gui
        
    def pulsar(self, fila, columna):
        """Realiza la jugada del jugador humano en la partida.

        Args:
            fila: La fila donde se intenta colocar la ficha.
            columna: La columna donde se intenta colocar la ficha.
        """
        if self.partida.terminada():
            if self.partida.ganador() == None:
                self.gui.actualizar_estado(EMPATE)
            else:
                self.gui.actualizar_estado(TERMINADA.format(self.partida.ganador().name))
            return
        
        if self.partida.turno != Ficha.X or self.gui.ocupado:
            return
        
        jugador = self.partida.turno
        movimiento = self.partida.jugar(columna)
        
        if movimiento is not None:
            self.gui.jugar(movimiento[0], movimiento[1], jugador, lambda: self.tras_jugada(jugador))
        else:
            self.gui.actualizar_estado(OCUPADA.format(jugador.name))
            
    def tras_jugada(self, jugador):
        """Maneja las acciones a realizar después de que el jugador humano realiza una jugada.

        Args:
            jugador: El jugador que realizó la jugada.
        """
        self.gui.mostrar_resultado(jugador)
        if not self.partida.terminada():
            self.gui.barra_pensar.config(text="Pensando...")
            self.gui.after(100, self.gui.juego_pc.jugar)
            
class JugadasPC:
    
    def __init__(self, gui, partida):
        self.partida = partida
        self.gui = gui
        self.ia = InteligenciaArtificial(partida.tablero)
        
    def jugar(self):
        movimiento = self.ia.mejor_movimiento()
        self.gui.barra_pensar.config(text="")
        if self.partida.terminada():
            return
        jugador = Ficha.O
        posicion = self.partida.jugar(movimiento[1])
        if posicion is not None:
            self.gui.jugar(posicion[0], posicion[1], jugador, lambda: self.gui.mostrar_resultado(jugador))
        else:
            self.gui.actualizar_estado(OCUPADA.format(jugador.name))
