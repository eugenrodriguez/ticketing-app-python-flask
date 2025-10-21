# dijkstra_ctypes.py
import ctypes
from ctypes import CDLL, c_int, POINTER

# --- CONFIGURACIÓN DE LA DLL ---

# Asegúrate de que este path sea correcto y que 'dijkstra.dll' exista en la misma carpeta.
DLL_PATH = './dijkstra.dll' 

try:
    # Carga la DLL.
    dijkstra_dll = CDLL(DLL_PATH)
except FileNotFoundError:
    print(f"ERROR: No se encontró la DLL en {DLL_PATH}.")
    print("Asegúrate de haber compilado 'dijkstra_dll.cpp' y que 'dijkstra.dll' esté aquí.")
    exit()
except Exception as e:
    print(f"ERROR al cargar la DLL: {e}")
    exit()

# 1. Configuración de Argumentos (argtypes)
# Le decimos a ctypes qué tipos de datos espera la función C++
# La función es: int* ejecutar_dijkstra_dll(int V, int E, int* aristas_flat, int inicial)
dijkstra_dll.ejecutar_dijkstra_dll.argtypes = [
    c_int,                  # num_vertices (V)
    c_int,                  # num_aristas (E)
    POINTER(c_int),         # aristas_flat (el puntero a nuestro arreglo plano de C++)
    c_int                   # vertice_inicial
]

# 2. Configuración del Retorno (restype)
# Le decimos a ctypes qué tipo de dato retorna la función C++
# Retorna un puntero a un entero (el arreglo de distancias)
dijkstra_dll.ejecutar_dijkstra_dll.restype = POINTER(c_int)

# --- FUNCIÓN DE TRADUCCIÓN PYTHON <-> C++ ---

def calcular_ruta_mas_corta(V: int, E: int, lista_aristas: list, inicial: int) -> dict:
    """
    Llama a la función de Dijkstra en la DLL y procesa los resultados.
    
    Args:
        V: Número de vértices.
        E: Número de aristas.
        lista_aristas: Lista plana de Python (origen, destino, peso, ...).
        inicial: Vértice inicial.
        
    Returns:
        Un diccionario donde la clave es el vértice y el valor es la distancia más corta.
    """
    
    # Convierte la lista de Python (lista_aristas) a un arreglo de C (c_int * longitud)
    # Esto es esencial para que la DLL reciba un puntero válido.
    array_c = (c_int * len(lista_aristas))(*lista_aristas)
    
    # Llama a la función C++ exportada de la DLL
    puntero_resultado = dijkstra_dll.ejecutar_dijkstra_dll(
        c_int(V),
        c_int(E),
        array_c,
        c_int(inicial)
    )
    
    # El puntero_resultado apunta al arreglo de C++ de tamaño V+1.
    resultados = {}
    
    # Recorremos desde 1 hasta V para obtener las distancias
    for i in range(1, V + 1):
        # Accedemos al valor en la dirección de memoria apuntada por el puntero
        resultados[i] = puntero_resultado[i]

    # *NOTA IMPORTANTE SOBRE LA MEMORIA*
    # Como en el código C++ usamos 'new' para crear el arreglo de retorno,
    # en un entorno de producción deberíamos liberar esa memoria. 
    # Por simplicidad en este ejemplo, lo omitimos, pero es una buena práctica.

    return resultados

# --- EJEMPLO DE PRUEBA (Opcional) ---
if __name__ == '__main__':
    print("--- Probando la conexión con la DLL ---")
    
    # Datos del ejemplo original: 5 vértices, 9 aristas, inicio en 1
    V_ejemplo = 5
    E_ejemplo = 9
    ARISTAS_ejemplo = [
        1, 2, 7, 1, 4, 2, 2, 3, 1, 2, 4, 2, 3, 5, 4,
        4, 2, 3, 4, 3, 8, 4, 5, 5, 5, 3, 5
    ]
    INICIAL_ejemplo = 1

    try:
        distancias = calcular_ruta_mas_corta(V_ejemplo, E_ejemplo, ARISTAS_ejemplo, INICIAL_ejemplo)
        print(f"\nDistancias calculadas por la DLL (desde el Vértice {INICIAL_ejemplo}):")
        
        # El valor de INF (Infinito) en C++ es un número grande (~1073741824)
        INF_LIMITE = 1000000 
        
        for vertice, dist in distancias.items():
            if dist > INF_LIMITE:
                 print(f"Vértice {vertice}: No accesible (Distancia: INF)")
            else:
                 print(f"Vértice {vertice}: Distancia = {dist}")

    except Exception as e:
        print(f"\nERROR durante la ejecución: {e}")