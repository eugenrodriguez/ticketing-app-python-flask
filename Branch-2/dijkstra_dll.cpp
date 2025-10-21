// dijkstra_dll.cpp - Archivo Único para generar la DLL
#include <stdio.h> // Se mantiene solo por si se usa alguna definición básica
#include <vector>
#include <queue>
#include <algorithm> // Incluimos para std::fill si fuera necesario, pero mantenemos init()
using namespace std;

// Definición para exportar la función (Windows - MinGW/g++)
#define DLL_EXPORT __declspec(dllexport)

// --- Constantes y Estructuras Originales ---
#define MAX 10005 
#define Node pair< int , int > 
#define INF 1<<30 

struct cmp {
    bool operator() ( const Node &a , const Node &b ) {
        return a.second > b.second;
    }
};

// --- Variables Globales Originales ---
vector< Node > ady[ MAX ]; 
int distancia[ MAX ];       
bool visitado[ MAX ];      
priority_queue< Node , vector<Node> , cmp > Q; 
int V;                      
int previo[ MAX ]; 


// --- Funciones del Algoritmo Original (Modificadas sin printf/scanf) ---

// Función de inicialización
void init(){
    // Limpiamos la cola de prioridad antes de cada ejecución
    while( !Q.empty() ) Q.pop();
    
    // Limpiamos las estructuras del grafo
    // Nota: La lista ady[i] se limpiará en la función de exportación
    for( int i = 0 ; i <= V ; ++i ){
        distancia[ i ] = INF;
        visitado[ i ] = false;
        previo[ i ] = -1;
    }
}

// Paso de relajación (Se mantiene igual)
void relajacion( int actual , int adyacente , int peso ){
    if( distancia[ actual ] + peso < distancia[ adyacente ] ){
        distancia[ adyacente ] = distancia[ actual ] + peso;
        previo[ adyacente ] = actual; 
        Q.push( Node( adyacente , distancia[ adyacente ] ) ); 
    }
}

// Función principal de Dijkstra (Modificada: solo ejecuta la lógica)
void dijkstra( int inicial ){
    init(); // Inicializar y limpiar
    Q.push( Node( inicial , 0 ) );
    distancia[ inicial ] = 0; 
    
    int actual , adyacente , peso;
    while( !Q.empty() ){
        actual = Q.top().first;
        Q.pop();
        if( visitado[ actual ] ) continue; 
        visitado[ actual ] = true; 

        for( int i = 0 ; i < ady[ actual ].size() ; ++i ){
            adyacente = ady[ actual ][ i ].first;
            peso = ady[ actual ][ i ].second;
            if( !visitado[ adyacente ] ){
                relajacion( actual , adyacente , peso ); 
            }
        }
    }
    // NOTA: Los printf y scanf del final han sido eliminados.
}

// --- FUNCIÓN DE INTERFAZ EXPORTADA (El "Puente" a Python) ---

/* * Recibe:
 * - num_vertices (V)
 * - num_aristas (E)
 * - aristas_flat: Arreglo de enteros plano [origen1, dest1, peso1, origen2, dest2, peso2, ...]
 * - vertice_inicial: El nodo de inicio (S)
 * * Retorna:
 * - int*: Un puntero a un nuevo arreglo de enteros con las distancias más cortas (índice 1 a V).
 */
extern "C" DLL_EXPORT int* ejecutar_dijkstra_dll(
    int num_vertices,
    int num_aristas,
    int* aristas_flat, 
    int vertice_inicial)
{
    // 1. Configurar y Limpiar el Grafo
    V = num_vertices;
    
    // Limpiamos las listas de adyacencia (es crucial si se llama más de una vez)
    for(int i = 0; i <= V; ++i) ady[i].clear();

    // 2. Cargar el Grafo desde el arreglo plano de Python
    for (int i = 0; i < num_aristas * 3; i += 3) {
        int origen = aristas_flat[i];
        int destino = aristas_flat[i+1];
        int peso = aristas_flat[i+2];

        // Se mantiene la lógica de grafo no dirigido (bidireccional) del original
        ady[origen].push_back(Node(destino, peso));
        ady[destino].push_back(Node(origen, peso));
    }

    // 3. Ejecutar el Algoritmo
    dijkstra(vertice_inicial);

    // 4. Preparar la Salida
    // Creamos un nuevo arreglo dinámico para devolver los resultados.
    int tamano = V + 1; // Usamos V+1 para indexar de 1 a V
    int* resultados_distancia = new int[tamano];
    
    // Copiamos los resultados del arreglo global 'distancia' al nuevo arreglo de retorno
    for (int i = 1; i <= V; ++i) {
        resultados_distancia[i] = distancia[i];
    }

    // Retornamos el puntero. Python debe saber liberarlo después.
    return resultados_distancia;
}