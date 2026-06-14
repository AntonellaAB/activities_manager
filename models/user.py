import tkinter as tk
from tkinter import messagebox

#==========================
# LOGIN
#==========================

def ir_login():
    limpiar_ventana()

    tk.Label(ventana, text="INICIAR SESION").pack()

    tk.Label(ventana, text="Correo electronico o telefono:").pack()
    entrada_correo = tk.Entry(ventana)
    entrada_correo.pack()

    tk.Label(ventana, text="Contraseña:").pack()
    entrada_password = tk.Entry(ventana, show="*")
    entrada_password.pack()
    
    def conmutar_ver_password_login():
        if var_ver_pass_login.get() == 1:
            entrada_password.config(show="")
        else:
            entrada_password.config(show="*")

    var_ver_pass_login = tk.IntVar()
    check_ver_pass = tk.Checkbutton(ventana, text="Ver contraseña", variable=var_ver_pass_login, command=conmutar_ver_password_login)
    check_ver_pass.pack()

    def procesar_login():
        correo = entrada_correo.get().strip()
        password = entrada_password.get().strip()

# ALERTAS DETALLADAS DE INICIO DE SESIÓN

        if correo == "" and password == "":
            messagebox.showerror("Error", "Debe completar los campos establecidos")
            return
        elif correo == "" and password != "":
            messagebox.showerror("Error", "Completo la contraseña, pero debe completar el correo electronico o telefono establecido")
            return
        elif password == "" and correo != "":
            messagebox.showerror("Error", "Completo el correo electronico o telefono, pero debe completar la contraseña establecida")
            return

        encontrado = False

        try:
            with open("usuarios.txt", "r") as archivo:
                for linea in archivo:
                    if not linea.strip():
                        continue
                    parts = linea.strip().split(",")
                    if len(parts) < 4: continue
                    tipo, nombre, correo_archivo, pass_archivo = parts

                    if correo.lower() == correo_archivo.lower() and password == pass_archivo:
                        encontrado = True
                        # ¡CORREGIDO! Ahora coincide exactamente con "Alumno" o "Docente"
                        if tipo == "Alumno":
                            panel_alumno(nombre)
                        else:
                            panel_profesor(nombre)
                        break

            if not encontrado:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")

        except FileNotFoundError:
            messagebox.showerror("Error", "No hay usuarios registrados")

    tk.Button(ventana, text="Ingresar", command=procesar_login).pack()
    tk.Button(ventana, text="Volver", command=pantalla_inicio).pack()

# =========================
# FUNCIONES GENERALES
# =========================

def limpiar_ventana():
    for widget in ventana.winfo_children():
        widget.destroy()

# =========================
# PANEL ALUMNO
# =========================

def panel_alumno(nombre):
    limpiar_ventana()
    tk.Label(ventana, text=f"Panel Alumno - Bienvenido {nombre}").pack()
    tk.Button(ventana, text="Cerrar sesión", command=pantalla_inicio).pack()

# =========================
# PANEL PROFESOR
# =========================

def panel_profesor(nombre):
    limpiar_ventana()
    tk.Label(ventana, text=f"Panel Profesor - Bienvenido {nombre}").pack()
    tk.Button(ventana, text="Cerrar sesión", command=pantalla_inicio).pack()

# =========================
# REGISTRO
# =========================

def ir_registro():
    limpiar_ventana()

    tk.Label(ventana, text="REGISTRO").pack()

    # Tipo de usuario
    tk.Label(ventana, text="Tipo de usuario:").pack()
    opciones = ["Soy Alumno", "Soy Docente"]
    seleccion_tipo = tk.StringVar(value=opciones[0])
    tk.OptionMenu(ventana, seleccion_tipo, *opciones).pack(pady=5)

    # Campos
    tk.Label(ventana, text="Nombre:").pack()
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack()

    tk.Label(ventana, text="Correo electronico o teléfono:").pack()
    entrada_correo = tk.Entry(ventana)
    entrada_correo.pack()

    tk.Label(ventana, text="Contraseña:").pack()
    entrada_password = tk.Entry(ventana, show="*")
    entrada_password.pack(pady=5)

    # Función para ver/ocultar contraseña
    def conmutar_ver_password_registro():
        if var_ver_pass.get() == 1:
            entrada_password.config(show="")
        else:
            entrada_password.config(show="*")

    var_ver_pass = tk.IntVar()
    check_ver_pass = tk.Checkbutton(ventana, text="Ver contraseña", variable=var_ver_pass, command=conmutar_ver_password_registro)
    check_ver_pass.pack()

    def procesar_registro():
        nombre = entrada_nombre.get().strip()
        correo = entrada_correo.get().strip()
        password = entrada_password.get().strip()
        tipo = seleccion_tipo.get()

        if nombre == "" or correo == "" or password == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # VERIFICAR DUPLICADOS
        try:
            with open("usuarios.txt", "r") as archivo:
                for linea in archivo:
                    if not linea.strip():
                        continue
                    parts = linea.strip().split(",")
                    if len(parts) < 4: continue  # Evita errores si hay una línea mal guardada
                    _, _, correo_archivo, _ = parts
                    if correo.lower() == correo_archivo.lower():
                        messagebox.showerror("Error", "Este correo o telefono ya esta registrado")
                        return
        except FileNotFoundError:
            pass 

        # GUARDAR
        with open("usuarios.txt", "a") as archivo:
            archivo.write(f"{tipo},{nombre},{correo},{password}\n")

        messagebox.showinfo("Exito", "Usuario registrado correctamente")
        pantalla_inicio() 

    tk.Button(ventana, text="Registrar", command=procesar_registro).pack()
    tk.Button(ventana, text="Volver", command=pantalla_inicio).pack()

    
# =========================
# INICIO
# =========================

def pantalla_inicio():
    limpiar_ventana()
    tk.Label(ventana, text="UA GESTION DE EXTENSION UNIVERSITARIA").pack()
    tk.Button(ventana, text="Iniciar Sesion", command=ir_login).pack()
    tk.Button(ventana, text="Registrarse", command=ir_registro).pack()

# =========================
# VENTANA PRINCIPAL
# =========================

ventana = tk.Tk()
ventana.title("Sistema de Extensión Universitaria")
ventana.geometry("350x350") 

pantalla_inicio()

ventana.mainloop()