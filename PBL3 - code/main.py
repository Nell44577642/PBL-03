import sys, os
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
from model import MetroGraph
from view import MetroView

class MetroController:
    def __init__(self, model, view):
        self.model = model; self.view = view
        self.view.btn_calculate.clicked.connect(self.handle_search)
        self.view.btn_close_st.clicked.connect(self.close_station)
        self.view.btn_close_line.clicked.connect(self.close_line)
        self.view.btn_reset_disruptions.clicked.connect(self.reset_disruptions)
        self.draw_graph()

    def reset_disruptions(self):
        self.model.closed_stations.clear(); self.model.closed_lines.clear()
        self.view.console.append("<b>[SYSTEM] Disruptions cleared.</b>")

    def close_station(self):
        st = self.view.close_st_input.text().strip()
        if st: self.model.closed_stations.add(self.model._normalize(st))

    def close_line(self):
        ln = self.view.close_line_input.text().strip()
        if ln: self.model.closed_lines.add(ln)

    def draw_graph(self, itinerary_nodes=None):
        self.view.figure.clear()
        ax = self.view.figure.add_subplot(111)
        G = nx.MultiGraph() # MultiGraph allows multiple lines between same stations

        # Line coloring map
        lines = set()
        for u in self.model.graph:
            for v, info in self.model.graph[u].items():
                lines.add(info['line'])
        
        color_palette = plt.cm.get_cmap('tab20', len(lines))
        line_colors = {line: color_palette(i) for i, line in enumerate(lines)}

        for u, neighbors in self.model.graph.items():
            u_name = self.model.name_map[u]
            for v, info in neighbors.items():
                v_name = self.model.name_map[v]
                G.add_edge(u_name, v_name, line=info['line'], color=line_colors[info['line']])

        pos = nx.spring_layout(G, k=0.3, seed=42)
        
        # Draw background edges by color
        for u, v, data in G.edges(data=True):
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=[data['color']], 
                                   alpha=0.3, width=1, ax=ax)
        
        nx.draw_networkx_nodes(G, pos, node_size=10, node_color='lightgray', ax=ax)

        if itinerary_nodes:
            path_edges = list(zip(itinerary_nodes, itinerary_nodes[1:]))
            nx.draw_networkx_nodes(G, pos, nodelist=itinerary_nodes, node_color='black', node_size=40, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)
            labels = {itinerary_nodes[0]: itinerary_nodes[0], itinerary_nodes[-1]: itinerary_nodes[-1]}
            nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold', ax=ax)

        ax.set_axis_off()
        self.view.canvas.draw()

    def handle_search(self):
        self.view.console.clear()
        city_file = self.view.city_selector.currentData()
        start = self.view.start_input.text().strip(); end = self.view.end_input.text().strip()
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model.load_data(os.path.join(base_dir, "Resources", city_file))

        norm_time, _ = self.model.dijkstra(start, end, ignore_disruptions=True)
        
        if not self.model.bfs_check(start, end):
            self.view.console.append("<b style='color:red;'>[ERROR] Route unreachable.</b>")
            return

        act_time, itinerary = self.model.dijkstra(start, end)
        
        if itinerary:
            m, s = divmod(act_time, 60)
            self.view.console.append(f"<b>--- ITINERARY FOUND ---</b>")
            self.view.console.append(f"<i>Time: {m}m {s}s</i>")
            if act_time > norm_time: self.view.console.append(f"<b style='color:yellow;'>Delay: +{(act_time-norm_time)//60} min</b>")
            
            last_line = None
            for i, (st, line) in enumerate(itinerary):
                if i == 0:
                    self.view.console.append(f"<b>[START]</b> {st}")
                    self.view.console.append(f"   Take <b>Line {itinerary[1][1]}</b>")
                    last_line = itinerary[1][1]
                elif i == len(itinerary)-1: self.view.console.append(f"<b>[ARRIVE]</b> {st}")
                elif line != last_line and line is not None:
                    self.view.console.append(f"<b style='color:#00bcff;'> [TRANSFER] @ {st}</b>")
                    self.view.console.append(f"   Switch to <b>Line {line}</b>")
                    last_line = line
                else: self.view.console.append(f"  • {st}")
            
            self.draw_graph([step[0] for step in itinerary])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = MetroController(MetroGraph(), MetroView())
    c.view.show(); sys.exit(app.exec_())