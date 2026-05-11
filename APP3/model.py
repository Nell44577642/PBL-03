import json
import heapq
import unicodedata

class MetroGraph:
    def __init__(self, transfer_time=120):
        self.graph = {}
        self.name_map = {}
        self.transfer_time = transfer_time 

    def _normalize(self, text):
        if not text: return ""
        text = str(text).replace('\xa0', ' ').strip()
        normalized = "".join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
        return normalized.lower()

    def build_from_json(self, file_path):
        self.graph = {}
        self.name_map = {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Strategy: Build connections from the 'lignes' structure
        # visible in Capture d’écran 2026-05-06 111922.png[cite: 1]
        lines_data = data.get('lignes', {})
        
        for line_id, line_info in lines_data.items():
            stations = line_info.get('stations', [])
            # Get the average travel time for this city
            avg_time = data.get('temps_moyen', 120) 
            
            # Create a link between each consecutive station in the list[cite: 2]
            for i in range(len(stations) - 1):
                raw_u = stations[i]
                raw_v = stations[i+1]
                
                u, v = self._normalize(raw_u), self._normalize(raw_v)
                
                self.name_map[u] = raw_u
                self.name_map[v] = raw_v

                if u not in self.graph: self.graph[u] = {}
                if v not in self.graph: self.graph[v] = {}
                
                # Assign the connection[cite: 2]
                self.graph[u][v] = {'time': avg_time, 'line': line_id}
                self.graph[v][u] = {'time': avg_time, 'line': line_id}
        
        print(f"Graph initialized with {len(self.graph)} stations.")

    def find_shortest_path(self, start_raw, end_raw):
        start = self._normalize(start_raw)
        end = self._normalize(end_raw)

        if start not in self.graph or end not in self.graph:
            return None, None

        queue = [(0, start, [], None)]
        visited = {}

        while queue:
            (time, current, path, last_line) = heapq.heappop(queue)

            if current not in visited or time < visited[current]:
                visited[current] = time
                new_path = path + [(self.name_map[current], last_line)]

                if current == end:
                    return time, new_path

                for neighbor, info in self.graph.get(current, {}).items():
                    travel_time = info['time']
                    line = info['line']
                    total_cost = time + travel_time
                    
                    if last_line is not None and line != last_line:
                        total_cost += self.transfer_time
                    
                    heapq.heappush(queue, (total_cost, neighbor, new_path, line))
        
        return None, None