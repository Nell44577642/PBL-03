import os
import tkinter as tk
from model import MetroGraph
from view import MetroGUI

class AppController:
    def __init__(self):
        self.root = tk.Tk()
        self.model = MetroGraph()
        
        # Maps user-friendly names to the files found in PBL3 2026 data-20260506.zip[cite: 1]
        self.city_map = {
            "Paris": "paris.json",
            "Bordeaux": "bordeaux.json",
            "Lille": "lille.json",
            "Lyon": "lyon.json"
        }
        
        # Initialize the View with the list of cities
        self.view = MetroGUI(
            self.root, 
            list(self.city_map.keys()), 
            self.handle_calculation
        )

    def handle_calculation(self, city_name, start_st, end_st):
        # Basic validation: ensure inputs aren't empty
        if not start_st.strip() or not end_st.strip():
            self.view.show_error("Please enter both a departure and arrival station.")
            return

        try:
            # 1. Identify the correct file in the 'Resources' folder
            filename = self.city_map[city_name]
            file_path = os.path.join("Resources", filename)
            
            # 2. Build the graph for that city[cite: 2]
            self.model.build_from_json(file_path)
            
            # 3. Search for the fastest path[cite: 2]
            time, path = self.model.find_shortest_path(start_st, end_st)
            
            if not path:
                self.view.show_error(f"No path found between '{start_st}' and '{end_st}'.")
                return

            # 4. Format the result string
            formatted_output = self._format_itinerary(city_name, time, path)
            
            # 5. Send to View (which will clear old results first)[cite: 2]
            self.view.update_results(formatted_output)

        except Exception as e:
            self.view.show_error(f"System Error: {str(e)}")

    def _format_itinerary(self, city, total_seconds, path):
        # Converts seconds to min/sec[cite: 2]
        mins, secs = divmod(total_seconds, 60)
        
        res = f"--- BEST ROUTE: {city.upper()} ---\n"
        res += f"Travel Time: {mins} min {secs} sec\n"
        res += "="*35 + "\n\n"
        
        for i, (station, line) in enumerate(path):
            if i == 0:
                res += f"BOARD: {station} (Line {path[i+1][1]})\n"
            elif i == len(path) - 1:
                res += f"ARRIVE: {station}\n"
            else:
                # Detect and highlight transfers[cite: 2]
                if path[i][1] != path[i-1][1] and path[i-1][1] is not None:
                    res += f" >> TRANSFER at {station} to Line {path[i][1]}\n"
                else:
                    res += f"  • {station}\n"
                    
        return res

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Create and run the application
    app = AppController()
    app.run()