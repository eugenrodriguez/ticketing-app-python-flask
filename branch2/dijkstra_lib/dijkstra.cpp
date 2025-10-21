\
        // C++ library exposing a C API for Dijkstra.
        // Compile as shared library:
        // Linux: g++ -O2 -shared -fPIC dijkstra.cpp -o libdijkstra.so
        // Windows (MinGW): g++ -O2 -shared -static-libgcc -static-libstdc++ -o dijkstra.dll dijkstra.cpp

        #include <vector>
        #include <queue>
        #include <limits>
        #include <cstring>
        extern "C" {

        // computes shortest paths; arrays src,dst,wt length = E
        // out_dist and out_prev must be preallocated with size V (int*).
        // returns 0 on success.
        int dijkstra_c(int V, int E, const int* src, const int* dst, const int* wt, int source, int* out_dist, int* out_prev) {
            if (V <= 0) return -1;
            const int INF = 1<<30;
            std::vector<std::vector<std::pair<int,int>>> adj(V+1);
            for (int i=0;i<E;i++) {
                int u = src[i];
                int v = dst[i];
                int w = wt[i];
                if (u<1 || u>V || v<1 || v>V) return -2;
                adj[u].push_back({v,w});
                adj[v].push_back({u,w});
            }
            std::vector<int> dist(V+1, INF), prev(V+1, -1);
            typedef std::pair<int,int> Node;
            struct Cmp { bool operator()(const Node&a,const Node&b) const { return a.second > b.second; } };
            std::priority_queue<Node, std::vector<Node>, Cmp> pq;
            dist[source]=0;
            pq.push({source,0});
            while(!pq.empty()) {
                int u = pq.top().first; pq.pop();
                for(auto &p: adj[u]) {
                    int v = p.first; int w = p.second;
                    if (dist[u] + w < dist[v]) {
                        dist[v] = dist[u] + w;
                        prev[v] = u;
                        pq.push({v, dist[v]});
                    }
                }
            }
            // copy to out arrays (index 1..V)
            for(int i=1;i<=V;i++){
                out_dist[i-1] = dist[i]==INF ? -1 : dist[i];
                out_prev[i-1] = prev[i];
            }
            return 0;
        }

        } // extern C
