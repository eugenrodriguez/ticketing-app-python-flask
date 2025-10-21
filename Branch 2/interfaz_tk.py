import tkinter as tk
from tkinter import messagebox, scrolledtext
# Importamos la función puente que llama a tu DLL
from dijkstra_ctypes import calcular_ruta_mas_corta

# Definimos el límite de "Infinito" para mostrar en la interfaz
# Debe coincidir con un valor muy grande de C++ para indicar "No accesible"
INF_LIMITE = 1000000 

# --- LÓGICA DE LA APLICACIÓN ---

def ejecutar_calculo():
    """
    Recupera los datos de la interfaz, llama a la DLL y muestra los resultados.
    """
    try:
        # 1. Recuperar los datos ingresados
        V = int(entry_v.get())
        E = int(entry_e.get())
        inicial = int(entry_inicial.get())
        
        # El usuario ingresa las aristas como texto: "1 2 7, 1 4 2, ..."
        aristas_texto = text_aristas.get("1.0", tk.END).strip().replace(',', ' ')
        
        # 2. Procesar las aristas
        # Convertimos el texto plano en una lista de enteros [o1, d1, p1, o2, d2, p2, ...]
        partes = aristas_texto.split()
        if len(partes) % 3 != 0:
            raise ValueError("El número total de valores de las aristas (origen, destino, peso) debe ser un múltiplo de 3.")
        
        lista_aristas = [int(p) for p in partes]
        
        # Verificación básica: El número de aristas debe coincidir
        if len(lista_aristas) / 3 != E:
             raise ValueError("El número de aristas (E) no coincide con la cantidad de datos ingresados.")

        # 3. Llamar a la DLL a través del puente ctypes
        distancias = calcular_ruta_mas_corta(V, E, lista_aristas, inicial)
        
        # 4. Formatear y Mostrar los Resultados
        resultado_str = f"--- Distancias Mínimas desde el Vértice {inicial} ---\n\n"
        
        for vertice, dist in distancias.items():
            if dist >= INF_LIMITE:
                dist_str = "No accesible (INF)"
            else:
                dist_str = str(dist)
            
            resultado_str += f"Vértice {vertice:^3}: {dist_str}\n"

        # Mostrar el resultado en el área de texto
        text_resultado.delete("1.0", tk.END)
        text_resultado.insert(tk.END, resultado_str)
        
    except ValueError as e:
        messagebox.showerror("Error de Entrada", f"Datos incorrectos o incompletos: {e}")
    except Exception as e:
        messagebox.showerror("Error de Ejecución", f"Ocurrió un error en el cálculo o la DLL: {e}")

# --- CONFIGURACIÓN DE LA INTERFAZ TKINTER ---

root = tk.Tk()
root.title("Solver Dijkstra (DLL + Tkinter)")

# Marco principal para organizar los inputs
frame_input = tk.Frame(root, padx=10, pady=10)
frame_input.pack(pady=10)

# Etiquetas y campos de entrada para V, E e Inicial
tk.Label(frame_input, text="Nº Vértices (V):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
entry_v = tk.Entry(frame_input, width=5)
entry_v.grid(row=0, column=1, padx=5, pady=5, sticky='w')
entry_v.insert(0, "5") # Valor de ejemplo

tk.Label(frame_input, text="Nº Aristas (E):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_e = tk.Entry(frame_input, width=5)
entry_e.grid(row=1, column=1, padx=5, pady=5, sticky='w')
entry_e.insert(0, "9") # Valor de ejemplo

tk.Label(frame_input, text="Vértice Inicial:").grid(row=0, column=2, padx=10, pady=5, sticky='w')
entry_inicial = tk.Entry(frame_input, width=5)
entry_inicial.grid(row=0, column=3, padx=5, pady=5, sticky='w')
entry_inicial.insert(0, "1") # Valor de ejemplo

# Área de texto para las Aristas
tk.Label(frame_input, text="Aristas (origen destino peso, sep. por coma o espacio):").grid(row=2, column=0, columnspan=4, pady=5, sticky='w')
text_aristas = scrolledtext.ScrolledText(frame_input, width=50, height=6, wrap=tk.WORD)
text_aristas.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
# Ejemplo de Input
ejemplo_input = "1 2 7, 1 4 2, 2 3 1, 2 4 2, 3 5 4, 4 2 3, 4 3 8, 4 5 5, 5 3 5"
text_aristas.insert(tk.END, ejemplo_input)


# Botón de Cálculo
btn_calcular = tk.Button(root, text="EJECUTAR DIJKSTRA (Usando DLL)", command=ejecutar_calculo, bg="lightblue", font=('Arial', 10, 'bold'))
btn_calcular.pack(pady=10, padx=10, fill=tk.X)

# Área de Resultados
tk.Label(root, text="RESULTADOS:").pack(pady=5)
text_resultado = scrolledtext.ScrolledText(root, width=60, height=10, state=tk.NORMAL)
text_resultado.pack(padx=10, pady=5)


root.mainloop()