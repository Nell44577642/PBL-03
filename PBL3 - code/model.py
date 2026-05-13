import json
import heapq
import unicodedata
from collections import deque

class MetroGraph:
    def __init__(self):
        self.graph = {}
        self.name_map = {}
        self.transfer_time = 120
        self.closed_stations = set()
        self.closed_lines = set()

    def _normalize(self, text):
        if not text: return ""
        return "".join(c for c in unicodedata.normalize('NFD', str(text).strip()) 
                       if unicodedata.category(c) != 'Mn').lower()

    def load_data(self, file_path):
        self.graph = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        avg_time = data.get('temps_moyen', 90)
        for line_id, info in data.get('lignes', {}).items():
            stations = info.get('stations', [])
            for i in range(len(stations) - 1):
                self.add_edge(stations[i], stations[i+1], avg_time, line_id)
        for conn in data.get('connexions', []):
            self.add_edge(conn['de'], conn['vers'], conn['temps'], conn.get('ligne', 'Unknown'))

    def add_edge(self, u_raw, v_raw, time, line):
        u, v = self._normalize(u_raw), self._normalize(v_raw)
        self.name_map[u], self.name_map[v] = u_raw, v_raw
        if u not in self.graph: self.graph[u] = {}
        if v not in self.graph: self.graph[v] = {}
        self.graph[u][v] = {'time': time, 'line': line}
        self.graph[v][u] = {'time': time, 'line': line}

    def dijkstra(self, start_raw, end_raw, ignore_disruptions=False):
        s, e = self._normalize(start_raw), self._normalize(end_raw)
        if s not in self.graph or e not in self.graph: return None, None
        queue = [(0, s, [], None)]
        visited = {}
        while queue:
            (time, curr, path, last_line) = heapq.heappop(queue)
            if curr in visited and visited[curr] <= time: continue
            visited[curr] = time
            new_path = path + [(self.name_map[curr], last_line)]
            if curr == e: return time, new_path
            for neighbor, info in self.graph[curr].items():
                if not ignore_disruptions:
                    if neighbor in self.closed_stations or info['line'] in self.closed_lines: continue
                cost = time + info['time']
                if last_line and info['line'] != last_line: cost += self.transfer_time
                heapq.heappush(queue, (cost, neighbor, new_path, info['line']))
        return None, None

    def bfs_check(self, start_node, end_node):
        s, e = self._normalize(start_node), self._normalize(end_node)
        if s not in self.graph or e not in self.graph: return False
        queue = deque([s]); visited = {s}
        while queue:
            curr = queue.popleft()
            if curr == e: return True
            for neighbor, info in self.graph[curr].items():
                if neighbor not in visited and neighbor not in self.closed_stations:
                    if info['line'] not in self.closed_lines:
                        visited.add(neighbor); queue.append(neighbor)
        return False