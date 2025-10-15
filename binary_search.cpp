#include <iostream>
#include <vector>
#include <limits>
#include <utility>
#include <queue>

// Dijkstra's algorithm to find the shortest path in a graph
std::vector<int> dijkstra(int start, const std::vector<std::vector<std::pair<int, int>>>& graph) {
    int n = graph.size();
    std::vector<int> dist(n, std::numeric_limits<int>::max());
    dist[start] = 0;
    
    using PII = std::pair<int, int>;
    std::priority_queue<PII, std::vector<PII>, std::greater<PII>> pq;
    pq.push({0, start});
    
    while (!pq.empty()) {
        int d = pq.top().first;
        int u = pq.top().second;
        pq.pop();
        
        if (d > dist[u]) continue; // Skip if we have found a better path
        
        for (auto& edge : graph[u]) {
            int v = edge.first;
            int weight = edge.second;
            
            if (dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
                pq.push({dist[v], v});
            }
        }
    }
    
    return dist;
}

int main() {
    // Example graph represented as an adjacency list
    std::vector<std::vector<std::pair<int, int>>> graph = {
        {{1, 4}, {2, 1}}, // edges from vertex 0
        {{0, 4}, {2, 2}, {3, 2}}, // edges from vertex 1
        {{0, 1}, {1, 2}, {3, 5}}, // edges from vertex 2
        {{1, 2}, {2, 5}}  // edges from vertex 3
    };
    
    int start = 0;
    std::vector<int> distances = dijkstra(start, graph);
    
    std::cout << "Vertex Distance from Start\n";
    for (int i = 0; i < distances.size(); ++i) {
        std::cout << i << ": " << distances[i] << std::endl;
    }
    return 0;
}