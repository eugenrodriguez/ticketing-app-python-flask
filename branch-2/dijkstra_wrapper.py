"""
Wrapper Python para la DLL de Dijkstra en C++
Usa ctypes para llamar funciones de la DLL
"""

import ctypes
import os
from typing import List, Tuple, Optional


class DijkstraWrapper:
    """Clase wrapper para interactuar con la DLL de Dijkstra mediante ctypes."""
    
    def __init__(self, dll_path: str = "dijkstra.dll"):
        """
        Inicializa el wrapper cargando la DLL.
        
        Args:
            dll_path: Ruta al archivo dijkstra.dll
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
        posibles_rutas = [
            os.path.join(base_dir, dll_path),              
            os.path.join(base_dir, "cpp", dll_path),        
            os.path.join(os.getcwd(), dll_path),            
        ]
        
        dll_encontrada = None
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                dll_encontrada = ruta
                break
        
        if not dll_encontrada:
            raise FileNotFoundError(
                f"No se encontró la DLL: {dll_path}\n"
                f"Buscado en: {', '.join(posibles_rutas)}\n"
                f"Compílala primero con:\n"
                f"g++ -shared -o dijkstra.dll cpp/dijkstra.cpp -O2 -std=c++11"
            )
        
        self.dll = ctypes.CDLL(dll_encontrada)
        self._configurar_funciones()
        print(f"DLL cargada exitosamente: {dll_encontrada}")
        
        self._configurar_funciones()
        
        print(f"DLL cargada exitosamente: {dll_path}")
    
    def _configurar_funciones(self):
        """Configura los tipos de argumentos y retorno de las funciones de la DLL."""
        
        self.dll.inicializar_grafo.argtypes = [ctypes.c_int]
        self.dll.inicializar_grafo.restype = None
        
        self.dll.agregar_arista.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.dll.agregar_arista.restype = None
        
        self.dll.agregar_arista_dirigida.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.dll.agregar_arista_dirigida.restype = None
        
        self.dll.ejecutar_dijkstra.argtypes = [ctypes.c_int]
        self.dll.ejecutar_dijkstra.restype = None
        
        self.dll.obtener_distancia.argtypes = [ctypes.c_int]
        self.dll.obtener_distancia.restype = ctypes.c_int
        
        self.dll.obtener_camino.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        self.dll.obtener_camino.restype = ctypes.c_int
        
        self.dll.obtener_todas_distancias.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.dll.obtener_todas_distancias.restype = None
        
        self.dll.limpiar_grafo.argtypes = []
        self.dll.limpiar_grafo.restype = None
        
        self.dll.prueba_suma.argtypes = [ctypes.c_int, ctypes.c_int]
        self.dll.prueba_suma.restype = ctypes.c_int
        
        self.dll.obtener_num_vertices.argtypes = []
        self.dll.obtener_num_vertices.restype = ctypes.c_int
    
    def prueba_conexion(self, a: int = 5, b: int = 10) -> int:
        """Prueba simple para verificar que la DLL funciona."""
        resultado = self.dll.prueba_suma(a, b)
        print(f"Prueba: {a} + {b} = {resultado}")
        return resultado
    
    def inicializar(self, num_vertices: int):
        """Inicializa el grafo con N vértices."""
        self.dll.inicializar_grafo(num_vertices)
        print(f"Grafo inicializado con {num_vertices} vértices")
    
    def agregar_arista(self, origen: int, destino: int, peso: int, dirigida: bool = False):
        """
        Agrega una arista al grafo.
        
        Args:
            origen: Vértice origen
            destino: Vértice destino
            peso: Peso de la arista
            dirigida: Si True, agrega arista dirigida; si False, no dirigida (bidireccional)
        """
        if dirigida:
            self.dll.agregar_arista_dirigida(origen, destino, peso)
        else:
            self.dll.agregar_arista(origen, destino, peso)
    
    def ejecutar_dijkstra(self, vertice_inicial: int):
        """Ejecuta el algoritmo de Dijkstra desde un vértice inicial."""
        self.dll.ejecutar_dijkstra(vertice_inicial)
        print(f"Dijkstra ejecutado desde vértice {vertice_inicial}")
    
    def obtener_distancia(self, destino: int) -> int:
        """
        Obtiene la distancia más corta al vértice destino.
        
        Returns:
            Distancia más corta, o -1 si no hay camino
        """
        return self.dll.obtener_distancia(destino)
    
    def obtener_camino(self, destino: int) -> List[int]:
        """
        Obtiene el camino más corto al vértice destino.
        
        Returns:
            Lista de vértices que forman el camino, o lista vacía si no hay camino
        """
        buffer = (ctypes.c_int * 1000)()
        longitud = self.dll.obtener_camino(destino, buffer)
        
        if longitud == 0:
            return []
        
        return [buffer[i] for i in range(longitud)]
    
    def obtener_todas_distancias(self) -> List[int]:
        """
        Obtiene las distancias más cortas a todos los vértices.
        
        Returns:
            Lista con distancias (índice 0 = vértice 1, etc.)
        """
        num_vertices = self.dll.obtener_num_vertices()
        buffer = (ctypes.c_int * num_vertices)()
        self.dll.obtener_todas_distancias(buffer)
        return [buffer[i] for i in range(num_vertices)]
    
    def limpiar(self):
        """Limpia el grafo."""
        self.dll.limpiar_grafo()
        print("Grafo limpiado")
    
    def crear_grafo_ejemplo(self):
        """Crea el grafo del ejemplo del código original."""
        print("\nCreando grafo de ejemplo...")
        self.inicializar(5)
        
        self.agregar_arista(1, 2, 7)
        self.agregar_arista(1, 4, 2)
        self.agregar_arista(2, 3, 1)
        self.agregar_arista(2, 4, 2)
        self.agregar_arista(3, 5, 4)
        self.agregar_arista(4, 2, 3)
        self.agregar_arista(4, 3, 8)
        self.agregar_arista(4, 5, 5)
        self.agregar_arista(5, 3, 5)
        
        print("Grafo de ejemplo creado")
        print("   Vértices: 1, 2, 3, 4, 5")
        print("   Aristas: 9 aristas bidireccionales")


def ejemplo_uso():
    """Ejemplo de uso del wrapper."""
    print("=" * 60)
    print("Ejemplo de uso: Dijkstra con DLL de C++")
    print("=" * 60)
    
    try:
        dijkstra = DijkstraWrapper("dijkstra.dll")
        
        dijkstra.prueba_conexion(10, 20)
        
        dijkstra.crear_grafo_ejemplo()
        
        vertice_inicial = 1
        dijkstra.ejecutar_dijkstra(vertice_inicial)
        
        print(f"\nDistancias más cortas desde vértice {vertice_inicial}:")
        for vertice in range(1, 6):
            distancia = dijkstra.obtener_distancia(vertice)
            camino = dijkstra.obtener_camino(vertice)
            
            if distancia == -1:
                print(f"   Vértice {vertice}: Sin camino")
            else:
                camino_str = " → ".join(map(str, camino))
                print(f"   Vértice {vertice}: distancia = {distancia}, camino = {camino_str}")
        
        print("\n" + "=" * 60)
        print("Ejemplo completado exitosamente")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    ejemplo_uso()