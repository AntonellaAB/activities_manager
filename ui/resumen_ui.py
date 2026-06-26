import tkinter as tk
from tkinter import ttk, messagebox
from dao.extension_dao import HorasExtensionDAO

class ResumenUI:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        
        self.root.title("Historial de Actividades")
        self.root.geometry("700x450")
        
        lbl_titulo = tk.Label(self.root, text=f"Resumen de Actividades de {self.usuario.nombre}", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=15)
        
        # Estructura del Treeview para simular tabla informativa
        self.tree = ttk.Treeview(self.root, columns=("Fecha", "Semestre", "Ubicación", "Materia", "Profesor", "Horas"), show="headings")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Semestre", text="Sem.")
        self.tree.heading("Ubicación", text="Ubicación")
        self.tree.heading("Materia", text="Materia")
        self.tree.heading("Profesor", text="Profesor Tutor")
        self.tree.heading("Horas", text="Horas")
        
        self.tree.column("Fecha", width=90, anchor="center")
        self.tree.column("Semestre", width=50, anchor="center")
        self.tree.column("Ubicación", width=130)
        self.tree.column("Materia", width=130)
        self.tree.column("Profesor", width=130)
        self.tree.column("Horas", width=60, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        
        btn_informe = tk.Button(btn_frame, text="Generar Informe (.TXT)", font=("Arial", 11, "bold"), bg="#28a745", fg="white", padx=15, pady=5, command=self.generar_informe_txt)
        btn_informe.pack()
        
        self.cargar_datos()

    def cargar_datos(self):
        # Limpiar filas existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.datos_informe = HorasExtensionDAO.obtener_resumen_alumno(self.usuario.id_user)
        for fila in self.datos_informe:
            # fila viene con: (fecha, semestre, ubicacion, materia, profesor, horas, informe/descripcion)
            self.tree.insert("", tk.END, values=(fila[0], fila[1], fila[2], fila[3] if fila[3] else "N/A", fila[4] if fila[4] else "N/A", fila[5]))

    def generar_informe_txt(self):
        if not self.datos_informe:
            messagebox.showwarning("Sin datos", "No tienes actividades registradas para reportar.")
            return
            
        nombre_archivo = f"Informe_Horas_{self.usuario.nombre.replace(' ', '_')}.txt"
        
        try:
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write("=========================================================\n")
                f.write("         UNIVERSIDAD AMERICANA - INFORME DE EXTENSIÓN     \n")
                f.write("=========================================================\n\n")
                f.write(f"ESTUDIANTE: {self.usuario.nombre.upper()}\n")
                f.write(f"ID USUARIO: {self.usuario.id_user}\n")
                total_horas = sum(fila[5] for fila in self.datos_informe)
                f.write(f"TOTAL HORAS ACUMULADAS: {total_horas} Horas\n")
                f.write("---------------------------------------------------------\n\n")
                f.write(f"{'FECHA':<12} | {'SEM':<4} | {'HORAS':<5} | {'UBICACIÓN':<20} | {'MATERIA':<20}\n")
                f.write("-" * 75 + "\n")
                
                for fila in self.datos_informe:
                    fecha_str = str(fila[0])
                    sem_str = str(fila[1])
                    horas_str = str(fila[5])
                    ubi_str = fila[2][:18]
                    mat_str = (fila[3] if fila[3] else "N/A")[:18]
                    f.write(f"{fecha_str:<12} | {sem_str:<4} | {horas_str:<5} | {ubi_str:<20} | {mat_str:<20}\n")
                    if fila[6]: # Si tiene descripción/informe de detalles
                        f.write(f"   -> Detalle: {fila[6]}\n")
                
                f.write("\n=========================================================\n")
                f.write(" Firma del Estudiante                    Visto Bueno Dirección\n")
                
            messagebox.showinfo("¡Informe Creado!", f"Se ha generado el archivo '{nombre_archivo}' exitosamente en la raíz del proyecto.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo escribir el archivo de texto: {e}")