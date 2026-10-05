"""
Created on Thu Mar 20 11:42:53 2025

@author: flipi
"""

import tkinter as tk

from interfaz import Ventana
from config import TITULO, VENTANA_GEOMETRIA
        
        
#main
def main():
    
    raiz = tk.Tk()
    raiz.title(TITULO)
    raiz.geometry(VENTANA_GEOMETRIA)
    Ventana(raiz)
    raiz.mainloop()
    
if __name__ == "__main__":
    main()