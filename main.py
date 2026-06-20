import tkinter as tk

#La ventana es un objeto que creamos 
ventana = tk.Tk()
ventana.title("Mi ventana")
ventana.geometry("400x300")
ventana.resizable(False, False) #Si colocamos ambos false no se puede estirar la ventana

ventana.configure(bg="#e0e0e0")


def saludar():
    nombre = entrada_texto.get().strip()
    valorStr.set(f"Hola, {nombre}")

#variable de control
valorStr= tk.StringVar()
valorStr.set("Esperando...")


#nuevo objeto // aqui podemos borrar la variable letreto trabajar sin ello
tk.Label(
    ventana, 
    text="Hola Mundo", 
    padx=20, pady=30, 
    font=("Gothic", 16, "bold"),
    anchor=('center') #centrado (default es center)

).pack(side = "top") #side es para alinear el paquete //pero tambien anchor

#ENTRADA DE TEXTO 
entrada_texto = tk.Entry(ventana)
entrada_texto.pack(pady=20)


#BOTON 
boton = tk.Button(
    ventana, 
    text="Aceptar",
    cursor= "hand2",
    command = saludar
    )
boton.pack()

#OUTPUT
letrero_salida = tk.Label(
    ventana,
    textvariable=valorStr,
    font=("Arial", 14)
)
letrero_salida.pack()



#mainloop va AL FINAL 
ventana.mainloop() #es para que no se cierre de inmediato hasta que se presione el boton de exit


