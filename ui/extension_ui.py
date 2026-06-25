import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class HorasExtensionUI:
    def __init__(self, root, dao_horas, alumno_id_logueado): #estas variables tienen que ser entregadas desde el main, pueden cambiar luego
        self.root = root
        self.dao_horas = dao_horas
        self.alumno_id = alumno_id_logueado
        
        self.root.title("Registro de Horas de Extensión")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        
        # Estos son datos de ejemplo para que pueda ejecutarse y mirar el aspecto

        #self.materias = {"Programación II": 1, "Base de Datos I": 2, "Matemática Discreta": 3}
        #self.profesores = {"Ing. Juan Pérez": 4, "Dra. Ana Gómez": 5, "Lic. Carlos Ruiz": 6}
        #self.actividades = {"EXTRA-MURO (cat1)": 1, "INTRA-MURO (cat2)": 2, "INTRA-MURO (cat3)": 3}
        
        #aqui termina

        
        self.crear_componentes()

    def crear_componentes(self):
        # El contenedor principal con margen padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # El título principal
        titulo = ttk.Label(main_frame, text="Registrar Horas de Extensión", font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Estos son los semestre (Spinner del 1 al 12)
        ttk.Label(main_frame, text="Semestre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.spin_semestre = ttk.Spinbox(main_frame, from_=1, to=12, width=10, state="readonly")
        self.spin_semestre.set(1)
        self.spin_semestre.grid(row=1, column=1, sticky=tk.W, pady=5)

        # Esto es la ubicación (Estoy cansado jefe)
        ttk.Label(main_frame, text="Ubicación/Lugar:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_ubicacion = ttk.Entry(main_frame, width=30)
        self.entry_ubicacion.grid(row=2, column=1, sticky=tk.W, pady=5)

        # La Materia (Desplegable - lastimosamente no pude ponerle el triangulito)
        ttk.Label(main_frame, text="Materia asociada:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.combo_materia = ttk.Combobox(main_frame, values=list(self.materias.keys()), state="readonly", width=28)
        self.combo_materia.grid(row=3, column=1, sticky=tk.W, pady=5)

        # El profesor Tutor (Desplegable - lo mismo)
        ttk.Label(main_frame, text="Profesor tutor:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.combo_profesor = ttk.Combobox(main_frame, values=list(self.profesores.keys()), state="readonly", width=28)
        self.combo_profesor.grid(row=4, column=1, sticky=tk.W, pady=5)

        # El tipo de Actividad (Desplegable)
        ttk.Label(main_frame, text="Actividad:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.combo_actividad = ttk.Combobox(main_frame, values=list(self.actividades.keys()), state="readonly", width=28)
        self.combo_actividad.grid(row=5, column=1, sticky=tk.W, pady=5)

        # La cantidad de Horas
        ttk.Label(main_frame, text="Horas acumuladas:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.entry_horas = ttk.Entry(main_frame, width=10)
        self.entry_horas.grid(row=6, column=1, sticky=tk.W, pady=5)

        # y la descripción
        ttk.Label(main_frame, text="Descripción:").grid(row=7, column=0, sticky=tk.NW, pady=5)
        self.txt_descripcion = tk.Text(main_frame, width=28, height=4, font=("Arial", 10))
        self.txt_descripcion.grid(row=7, column=1, sticky=tk.W, pady=5)

        # ah y el boton guardar
        btn_guardar = ttk.Button(main_frame, text="Guardar Registro", command=self.procesar_guardado)
        btn_guardar.grid(row=8, column=0, columnspan=2, pady=(20, 0))

    def procesar_guardado(self):
        # Validar campos obligatorios de texto
        ubicacion = self.entry_ubicacion.get().strip()
        horas_str = self.entry_horas.get().strip()
        descripcion = self.txt_descripcion.get("1.0", tk.END).strip()
        
        if not ubicacion or not horas_str:
            messagebox.showwarning("Campos vacíos", "Por favor, completa la ubicación y las horas.")
            return

        # Validar selección de desplegables
        if not self.combo_materia.get() or not self.combo_profesor.get() or not self.combo_actividad.get():
            messagebox.showwarning("Selección incompleta", "Debes seleccionar una materia, profesor y actividad.")
            return

        try:
            horas = int(horas_str)
        except ValueError:
            messagebox.showerror("Error de datos", "La cantidad de horas debe ser un número entero.")
            return

        # Convertimos los textos seleccionados en pantalla a los IDs reales usando nuestros diccionarios
        materia_id = self.materias[self.combo_materia.get()]
        profesor_id = self.profesores[self.combo_profesor.get()]
        actividad_id = self.actividades[self.combo_actividad.get()]
        
        semestre = int(self.spin_semestre.get())
        fecha_actual = date.today().strftime("%Y-%m-%d") # Usamos la fecha de hoy por defecto

        # llamada al Dao
        exito = self.dao_horas.agregar_horas(
            alumno_id=self.alumno_id,
            semestre=semestre,
            ubicacion=ubicacion,
            materia_id=materia_id,
            profesor_id=profesor_id,
            actividad_id=actividad_id,
            fecha=fecha_actual,
            horas=horas,
            descripcion=descripcion
        )

        if exito:
            messagebox.showinfo("¡Guardado!", "Las horas de extensión se registraron correctamente.")
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "Hubo un problema al guardar en la base de datos.")

    def limpiar_campos(self):
        self.entry_ubicacion.delete(0, tk.END)
        self.entry_horas.delete(0, tk.END)
        self.txt_descripcion.delete("1.0", tk.END)
        self.combo_materia.set('')
        self.combo_profesor.set('')
        self.combo_actividad.set('')
        self.spin_semestre.set(1)
        


# Esto es para mirar el aspecto final del tkinter y todo ese pedo
#if __name__ == "__main__":
#    root = tk.Tk()    
#    app = HorasExtensionUI(root, dao_horas=None, alumno_id_logueado=1)   
#    root.mainloop()