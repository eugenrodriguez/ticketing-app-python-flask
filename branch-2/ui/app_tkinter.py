import sys 
import os 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from dijkstra_wrapper import DijkstraWrapper



class DijkstraApp(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.title("Algoritmo de Dijkstra - C++ DLL con Python Tkinter")
        self.geometry("900x700")
        self.configure(bg="#f0f0f0")
        
        try:
            self.dijkstra = DijkstraWrapper("dijkstra.dll")
            self.dll_cargada = True
        except FileNotFoundError:
            self.dll_cargada = False
            messagebox.showerror(
                "Error - DLL no encontrada",
                "No se encontró dijkstra.dll\n\n"
                "Compila el archivo C++ primero:\n"
                "g++ -shared -o dijkstra.dll dijkstra.cpp -O2 -std=c++11"
            )
        
        self._crear_interfaz()
        
        if self.dll_cargada:
            self.cargar_grafo_ejemplo()
    
    def _crear_interfaz(self):        
        frame_titulo = tk.Frame(self, bg="#2c3e50", height=60)
        frame_titulo.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            frame_titulo,
            text=" Algoritmo de Dijkstra - Caminos Más Cortos",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=15
        ).pack()
        
        frame_principal = tk.Frame(self, bg="#f0f0f0")
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._crear_panel_configuracion(frame_principal)
        
        self._crear_panel_resultados(frame_principal)
        
        self._crear_panel_acciones()
    
    def _crear_panel_configuracion(self, parent):
        frame_config = ttk.LabelFrame(
            parent,
            text="Configuración del Grafo",
            padding=10
        )
        frame_config.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        ttk.Label(frame_config, text="Número de vértices:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_vertices = ttk.Entry(frame_config, width=10)
        self.entry_vertices.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.entry_vertices.insert(0, "5")
        
        ttk.Button(
            frame_config,
            text="Inicializar Grafo",
            command=self.inicializar_grafo
        ).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Separator(frame_config, orient=tk.HORIZONTAL).grid(
            row=1, column=0, columnspan=3, sticky="ew", pady=10
        )
        
        ttk.Label(frame_config, text="Agregar Arista", font=("Arial", 10, "bold")).grid(
            row=2, column=0, columnspan=3, sticky=tk.W, pady=5
        )
        
        ttk.Label(frame_config, text="Origen:").grid(row=3, column=0, sticky=tk.W)
        self.entry_origen = ttk.Entry(frame_config, width=10)
        self.entry_origen.grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(frame_config, text="Destino:").grid(row=4, column=0, sticky=tk.W)
        self.entry_destino = ttk.Entry(frame_config, width=10)
        self.entry_destino.grid(row=4, column=1, sticky=tk.W)
        
        ttk.Label(frame_config, text="Peso:").grid(row=5, column=0, sticky=tk.W)
        self.entry_peso = ttk.Entry(frame_config, width=10)
        self.entry_peso.grid(row=5, column=1, sticky=tk.W)
        
        self.var_dirigida = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame_config,
            text="Arista dirigida",
            variable=self.var_dirigida
        ).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Button(
            frame_config,
            text="Agregar Arista",
            command=self.agregar_arista
        ).grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Separator(frame_config, orient=tk.HORIZONTAL).grid(
            row=8, column=0, columnspan=3, sticky="ew", pady=10
        )
        
        ttk.Label(frame_config, text="Vértice inicial:").grid(row=9, column=0, sticky=tk.W)
        self.entry_inicial = ttk.Entry(frame_config, width=10)
        self.entry_inicial.grid(row=9, column=1, sticky=tk.W)
        self.entry_inicial.insert(0, "1")
        
        ttk.Button(
            frame_config,
            text="Ejecutar Dijkstra",
            command=self.ejecutar_dijkstra,
            style="Accent.TButton"
        ).grid(row=10, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame_config, text="Log de Acciones:").grid(
            row=11, column=0, columnspan=3, sticky=tk.W, pady=(10, 5)
        )
        
        self.log_text = scrolledtext.ScrolledText(
            frame_config,
            height=10,
            width=40,
            font=("Consolas", 9)
        )
        self.log_text.grid(row=12, column=0, columnspan=3, sticky="nsew", pady=5)
        frame_config.rowconfigure(12, weight=1)
    
    def _crear_panel_resultados(self, parent):
        frame_resultados = ttk.LabelFrame(
            parent,
            text="Resultados - Distancias y Caminos",
            padding=10
        )
        frame_resultados.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        parent.columnconfigure(1, weight=1)
        
        self.tree = ttk.Treeview(
            frame_resultados,
            columns=("vertice", "distancia", "camino"),
            show="headings",
            height=20
        )
        
        self.tree.heading("vertice", text="Vértice Destino")
        self.tree.heading("distancia", text="Distancia")
        self.tree.heading("camino", text="Camino Más Corto")
        
        self.tree.column("vertice", width=100, anchor=tk.CENTER)
        self.tree.column("distancia", width=100, anchor=tk.CENTER)
        self.tree.column("camino", width=300, anchor=tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _crear_panel_acciones(self):
        frame_acciones = tk.Frame(self, bg="#ecf0f1", height=60)
        frame_acciones.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        ttk.Button(
            frame_acciones,
            text="Cargar Grafo de Ejemplo",
            command=self.cargar_grafo_ejemplo,
            width=25
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        ttk.Button(
            frame_acciones,
            text="Limpiar Todo",
            command=self.limpiar_todo,
            width=20
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        ttk.Button(
            frame_acciones,
            text="Salir",
            command=self.quit,
            width=15
        ).pack(side=tk.RIGHT, padx=10, pady=10)
    
    def log(self, mensaje):
        self.log_text.insert(tk.END, f"{mensaje}\n")
        self.log_text.see(tk.END)
    
    def inicializar_grafo(self):
        if not self.dll_cargada:
            messagebox.showerror("Error", "DLL no cargada")
            return
        
        try:
            num_vertices = int(self.entry_vertices.get())
            if num_vertices <= 0:
                raise ValueError
            
            self.dijkstra.inicializar(num_vertices)
            self.log(f"Grafo inicializado con {num_vertices} vértices")
            self.tree.delete(*self.tree.get_children())
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de vértices")
    
    def agregar_arista(self):
        if not self.dll_cargada:
            return
        
        try:
            origen = int(self.entry_origen.get())
            destino = int(self.entry_destino.get())
            peso = int(self.entry_peso.get())
            dirigida = self.var_dirigida.get()
            
            if origen <= 0 or destino <= 0 or peso < 0:
                raise ValueError
            
            self.dijkstra.agregar_arista(origen, destino, peso, dirigida)
            
            tipo = "dirigida" if dirigida else "bidireccional"
            self.log(f"Arista agregada: {origen} → {destino} (peso: {peso}, {tipo})")
            
            self.entry_origen.delete(0, tk.END)
            self.entry_destino.delete(0, tk.END)
            self.entry_peso.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos")
    
    def ejecutar_dijkstra(self):
        if not self.dll_cargada:
            return
        
        try:
            inicial = int(self.entry_inicial.get())
            
            if inicial <= 0:
                raise ValueError
            
            self.dijkstra.ejecutar_dijkstra(inicial)
            self.log(f"Dijkstra ejecutado desde vértice {inicial}")
            
            self.tree.delete(*self.tree.get_children())
            
            num_vertices = int(self.entry_vertices.get())
            
            for vertice in range(1, num_vertices + 1):
                distancia = self.dijkstra.obtener_distancia(vertice)
                camino = self.dijkstra.obtener_camino(vertice)
                
                if distancia == -1:
                    self.tree.insert("", tk.END, values=(
                        vertice,
                        "∞ (Sin camino)",
                        "No alcanzable"
                    ))
                else:
                    camino_str = " → ".join(map(str, camino))
                    self.tree.insert("", tk.END, values=(
                        vertice,
                        distancia,
                        camino_str
                    ))
            
            self.log(f"Resultados mostrados para {num_vertices} vértices")
            messagebox.showinfo(
                "Éxito",
                f"Dijkstra ejecutado exitosamente\nDesde vértice: {inicial}"
            )
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un vértice inicial válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar Dijkstra: {e}")
    
    def cargar_grafo_ejemplo(self):
        if not self.dll_cargada:
            return
        
        try:
            self.dijkstra.crear_grafo_ejemplo()
            self.entry_vertices.delete(0, tk.END)
            self.entry_vertices.insert(0, "5")
            self.entry_inicial.delete(0, tk.END)
            self.entry_inicial.insert(0, "1")
            
            self.log("Grafo de ejemplo cargado:")
            self.log("   Vértices: 5")
            self.log("   Aristas:")
            aristas = [
                (1, 2, 7), (1, 4, 2), (2, 3, 1), (2, 4, 2),
                (3, 5, 4), (4, 2, 3), (4, 3, 8), (4, 5, 5), (5, 3, 5)
            ]
            for origen, destino, peso in aristas:
                self.log(f"      {origen} ↔ {destino} (peso: {peso})")
            
            messagebox.showinfo(
                "Grafo de Ejemplo",
                "Grafo cargado exitosamente\n\n"
                "5 vértices\n"
                "9 aristas bidireccionales\n\n"
                "Presiona 'Ejecutar Dijkstra' para ver resultados"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar grafo: {e}")
    
    def limpiar_todo(self):
        if not self.dll_cargada:
            return
        
        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Desea limpiar todo el grafo y resultados?"
        )
        
        if respuesta:
            self.dijkstra.limpiar()
            self.tree.delete(*self.tree.get_children())
            self.log_text.delete(1.0, tk.END)
            self.log("Todo limpiado")
            
            self.entry_vertices.delete(0, tk.END)
            self.entry_vertices.insert(0, "5")
            self.entry_inicial.delete(0, tk.END)
            self.entry_inicial.insert(0, "1")


def main():
    print("=" * 60)
    print("Iniciando aplicación Tkinter - Dijkstra con DLL C++")
    print("=" * 60)
    
    if not os.path.exists("dijkstra.dll"):
        print("\nADVERTENCIA: No se encontró dijkstra.dll")
    else:
        print("dijkstra.dll encontrada")
    
    app = DijkstraApp()
    app.mainloop()


if __name__ == "__main__":
    main()
