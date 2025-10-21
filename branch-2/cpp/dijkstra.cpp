/*****************************************************
 * Algoritmo: Dijkstra (One Source Shortest Path)
 * Adaptado para DLL exportable a Python via ctypes
 * Autor: Jhosimar George Arias Figueroa (adaptado)
 *****************************************************/

#include <vector>
#include <queue>
#include <cstring>

#define MAX 10005
#define INF 1073741824  // 2^30

using namespace std;

typedef pair<int, int> Node;

// Variables globales para el grafo
vector<Node> ady[MAX];
int distancia[MAX];
bool visitado[MAX];
int previo[MAX];
int V = 0;

// Comparador para min-heap
struct cmp {
    bool operator()(const Node &a, const Node &b) {
        return a.second > b.second;
    }
};

// Inicialización
void init() {
    for (int i = 0; i <= V; ++i) {
        distancia[i] = INF;
        visitado[i] = false;
        previo[i] = -1;
    }
}

// Relajación
void relajacion(int actual, int adyacente, int peso) {
    if (distancia[actual] + peso < distancia[adyacente]) {
        distancia[adyacente] = distancia[actual] + peso;
        previo[adyacente] = actual;
    }
}

// Algoritmo de Dijkstra
void dijkstra_internal(int inicial) {
    init();
    priority_queue<Node, vector<Node>, cmp> Q;
    Q.push(Node(inicial, 0));
    distancia[inicial] = 0;
    
    while (!Q.empty()) {
        int actual = Q.top().first;
        Q.pop();
        
        if (visitado[actual]) continue;
        visitado[actual] = true;
        
        for (size_t i = 0; i < ady[actual].size(); ++i) {
            int adyacente = ady[actual][i].first;
            int peso = ady[actual][i].second;
            
            if (!visitado[adyacente]) {
                relajacion(actual, adyacente, peso);
                Q.push(Node(adyacente, distancia[adyacente]));
            }
        }
    }
}

// Reconstruir camino
int reconstruir_camino(int destino, int* camino) {
    if (distancia[destino] == INF) {
        return 0;  // No hay camino
    }
    
    vector<int> temp;
    int actual = destino;
    
    while (actual != -1) {
        temp.push_back(actual);
        actual = previo[actual];
    }
    
    int longitud = temp.size();
    for (int i = 0; i < longitud; ++i) {
        camino[i] = temp[longitud - 1 - i];
    }
    
    return longitud;
}

// ========================================
// FUNCIONES EXPORTADAS PARA PYTHON
// ========================================

extern "C" {

// Inicializar el grafo con N vértices
__declspec(dllexport) void inicializar_grafo(int num_vertices) {
    V = num_vertices;
    for (int i = 0; i <= V; ++i) {
        ady[i].clear();
    }
}

// Agregar arista al grafo (grafo no dirigido)
__declspec(dllexport) void agregar_arista(int origen, int destino, int peso) {
    ady[origen].push_back(Node(destino, peso));
    ady[destino].push_back(Node(origen, peso));
}

// Agregar arista dirigida
__declspec(dllexport) void agregar_arista_dirigida(int origen, int destino, int peso) {
    ady[origen].push_back(Node(destino, peso));
}

// Ejecutar Dijkstra desde un vértice inicial
__declspec(dllexport) void ejecutar_dijkstra(int inicial) {
    dijkstra_internal(inicial);
}

// Obtener la distancia más corta a un vértice destino
__declspec(dllexport) int obtener_distancia(int destino) {
    if (destino < 0 || destino > V) return -1;
    if (distancia[destino] == INF) return -1;
    return distancia[destino];
}

// Obtener el camino más corto (devuelve longitud del camino)
__declspec(dllexport) int obtener_camino(int destino, int* buffer_camino) {
    return reconstruir_camino(destino, buffer_camino);
}

// Obtener todas las distancias (para matriz completa)
__declspec(dllexport) void obtener_todas_distancias(int* buffer_distancias) {
    for (int i = 1; i <= V; ++i) {
        buffer_distancias[i - 1] = (distancia[i] == INF) ? -1 : distancia[i];
    }
}

// Limpiar el grafo
__declspec(dllexport) void limpiar_grafo() {
    for (int i = 0; i <= MAX; ++i) {
        ady[i].clear();
    }
    V = 0;
}

// Función de prueba simple
__declspec(dllexport) int prueba_suma(int a, int b) {
    return a + b;
}

// Obtener número de vértices
__declspec(dllexport) int obtener_num_vertices() {
    return V;
}

}  // extern "C"