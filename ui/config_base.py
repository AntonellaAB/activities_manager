#Configuraciones especificas sobre diseño de UI
import tkinter as tk


ANCHO = 1000
ALTO = 600
FONDO_PRINCIPAL = "#202934"
FONDO_TARJETA = "#50555d" 

#FUENTE.......
FUENTE_FAMILY = "Segoe UI"
FUENTE_TITULO = "Impact" 
FUENTE_COLOR = "#FFFFFF" 
FUENTE_COLOR_SECUNDARIO = "#ecbb21"   #claro #ede3c2

#BOTONES.........
BOTON_COLOR1 = "#d95d5a"  #hover #ebbab9 
BOTON_COLOR1_HOVER = "#ebbab9"
BOTON_COLOR2 = "#6b98a6"  #hover #abd6e4
BOTON_COLOR2_HOVER = "#abd6e4"
BOTON_COLOR3 = "#1800ad"  #hover #FFFFFF  
#Entry fields .........
ENTRY_BG = "#FFFFFF"            
BORDER_COLOR = "#CBD5E1"


def static_size(ventana):
    ventana.geometry(f"{ANCHO}x{ALTO}")
    ventana.resizable(False, False)
    ventana.configure(bg=FONDO_PRINCIPAL)

class PantallaBase(tk.Tk):
    def __init__(self, titulo="Sistema de Gestion"):
        super().__init__()
        self.title(titulo)
        static_size(self)


class SubPantallaBase(tk.Toplevel):
    def __init__(self, master, titulo="Sub-Pantalla"):
        super().__init__(master)
        self.title(titulo)
        static_size(self)



