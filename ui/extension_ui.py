import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from dao.extension_dao import HorasExtensionDAO
from dao.materias_dao import SubjectDAO  
from models.horas_extension import HorasExtension

class HorasExtensionUI:
    def __init__(self, root, connection, alumno_id_logueado):
        self.root = root
        self.connection = connection
        self.alumno_id = alumno_id_logueado
        
        self.root.title("Registro de Horas de Extensión")
        self.root.geometry("460x580")
        self.root.resizable(False, False)
        
        self.materias_dict = {}
        self.profesores_dict = {}
        self.actividades_dict = {}

        # Cargamos los datos de las tablas y luego dibujamos la UI
        self.cargar_datos_desde_bd()
        self.crear_componentes()

    def cargar_datos_desde_bd(self):
        """Carga la informacio desde PostgreSQL y actualiza los Combobox."""
        if self.connection is None:
            print("Error: La conexión es None.")
            return

        # 1. Cargamos datos desde los DAOs
        subjects_lista = SubjectDAO.get_all(self.connection)
        self.materias_dict = {subj.name: subj.subject_id for subj in subjects_lista}

        self.profesores_dict = HorasExtensionDAO.obtener_profesores_dict(self.connection)
        self.actividades_dict = HorasExtensionDAO.obtener_actividades_dict(self.connection)

        # 2. Actualizamos los valores de los Combobox si ya existen
        if hasattr(self, 'combo_materia'):
            self.combo_materia['values'] = list(self.materias_dict.keys())
        if hasattr(self, 'combo_profesor'):
            self.combo_profesor['values'] = list(self.profesores_dict.keys())
        if hasattr(self, 'combo_actividad'):
            self.combo_actividad['values'] = list(self.actividades_dict.keys())

    def crear_componentes(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        titulo = ttk.Label(main_frame, text="Registrar Horas de Extensión", font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # 1. Semestre
        ttk.Label(main_frame, text="Semestre:").grid(row=1, column=0, sticky=tk.W, pady=6)
        self.spin_semestre = ttk.Spinbox(main_frame, from_=1, to=12, width=10, state="readonly")
        self.spin_semestre.set(1)
        self.spin_semestre.grid(row=1, column=1, sticky=tk.W, pady=6)

        # 2. Fecha (NUEVO CAMPO)
        ttk.Label(main_frame, text="Fecha (AAAA-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=6)
        self.entry_fecha = ttk.Entry(main_frame, width=20)
        self.entry_fecha.grid(row=2, column=1, sticky=tk.W, pady=6)

        # 3. Ubicación (Bajamos la fila a 3)
        ttk.Label(main_frame, text="Ubicación / Lugar:").grid(row=3, column=0, sticky=tk.W, pady=6)
        self.entry_ubicacion = ttk.Entry(main_frame, width=32)
        self.entry_ubicacion.grid(row=3, column=1, sticky=tk.W, pady=6)

        # 4. Materia (Bajamos a 4)
        ttk.Label(main_frame, text="Materia asociada:").grid(row=4, column=0, sticky=tk.W, pady=6)
        self.combo_materia = ttk.Combobox(main_frame, values=list(self.materias_dict.keys()), state="readonly", width=30)
        self.combo_materia.grid(row=4, column=1, sticky=tk.W, pady=6)

        # 5. Profesor Tutor (Bajamos a 5)
        ttk.Label(main_frame, text="Profesor tutor:").grid(row=5, column=0, sticky=tk.W, pady=6)
        self.combo_profesor = ttk.Combobox(main_frame, values=list(self.profesores_dict.keys()), state="readonly", width=30)
        self.combo_profesor.grid(row=5, column=1, sticky=tk.W, pady=6)

        # 6. Tipo Actividad (Bajamos a 6)
        ttk.Label(main_frame, text="Tipo Actividad:").grid(row=6, column=0, sticky=tk.W, pady=6)
        self.combo_actividad = ttk.Combobox(main_frame, values=list(self.actividades_dict.keys()), state="readonly", width=30)
        self.combo_actividad.grid(row=6, column=1, sticky=tk.W, pady=6)

        # 7. Horas (Bajamos a 7)
        ttk.Label(main_frame, text="Horas acumuladas:").grid(row=7, column=0, sticky=tk.W, pady=6)
        self.entry_horas = ttk.Entry(main_frame, width=12)
        self.entry_horas.grid(row=7, column=1, sticky=tk.W, pady=6)

        # 8. Descripción (Bajamos a 8)
        ttk.Label(main_frame, text="Descripción:").grid(row=8, column=0, sticky=tk.NW, pady=6)
        self.txt_descripcion = tk.Text(main_frame, width=30, height=4, font=("Arial", 10))
        self.txt_descripcion.grid(row=8, column=1, sticky=tk.W, pady=6)

        # Botón Guardar (Bajamos a 9)
        btn_guardar = ttk.Button(main_frame, text="Guardar Registro", command=self.procesar_guardado)
        btn_guardar.grid(row=9, column=0, columnspan=2, pady=(25, 0))

    def procesar_guardado(self):
        fecha = self.entry_fecha.get().strip() # Captura la fecha del campo nuevo
        ubicacion = self.entry_ubicacion.get().strip()
        horas_str = self.entry_horas.get().strip()
        descripcion = self.txt_descripcion.get("1.0", tk.END).strip()
        
        # Validamos que la fecha no esté vacía
        if not fecha or not ubicacion or not horas_str:
            messagebox.showwarning("Campos incompletos", "Fecha, Ubicación y Horas son obligatorios.")
            return

        if not self.combo_materia.get() or not self.combo_profesor.get() or not self.combo_actividad.get():
            messagebox.showwarning("Selección faltante", "Por favor selecciona Materia, Profesor y Actividad.")
            return

        try:
            horas = int(horas_str)
        except ValueError:
            messagebox.showerror("Error numérico", "Las horas deben ser un número entero.")
            return

        materia_id = self.materias_dict[self.combo_materia.get()]
        profesor_id = self.profesores_dict[self.combo_profesor.get()]
        actividad_id = self.actividades_dict[self.combo_actividad.get()]
        semestre = int(self.spin_semestre.get())

        # Creamos el objeto con la fecha escrita por el usuario
        nueva_solicitud = HorasExtension(
            alumno_id=self.alumno_id, semestre=semestre, ubicacion=ubicacion,
            materia_id=materia_id, profesor_id=profesor_id, actividad_id=actividad_id,
            fecha=fecha, horas=horas, informe=descripcion
        )

        exito = HorasExtensionDAO.agregar_horas(self.connection, nueva_solicitud, es_prueba=False)

        if exito:
            messagebox.showinfo("¡Correcto!", "Registrado con éxito.")
            self.limpiar_formulario()
        else:
            messagebox.showerror("Fallo", "Error al guardar en la BD.")

    def limpiar_formulario(self):
        self.entry_fecha.delete(0, tk.END) # Limpiamos el campo nuevo
        self.entry_ubicacion.delete(0, tk.END)
        self.entry_horas.delete(0, tk.END)
        self.txt_descripcion.delete("1.0", tk.END)
        self.combo_materia.set('')
        self.combo_profesor.set('')
        self.combo_actividad.set('')
        self.spin_semestre.set(1)

if __name__ == "__main__":
    from database.conection import obtener_conexion 
    conexion_db = obtener_conexion()
    root = tk.Tk()
    app = HorasExtensionUI(root, connection=conexion_db, alumno_id_logueado=1)
    root.mainloop()
    if conexion_db:
        conexion_db.close()