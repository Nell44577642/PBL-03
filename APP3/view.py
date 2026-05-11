import tkinter as tk
from tkinter import ttk, messagebox

class MetroGUI:
    def __init__(self, root, cities, calc_callback):
        self.root = root
        self.root.title("ESME Metro Route Planner 2026")
        self.root.geometry("500x650")
        self.calc_callback = calc_callback

        # Main Layout Container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. City Selection
        ttk.Label(main_frame, text="Select City:", font=('Helvetica', 10, 'bold')).pack(pady=5)
        self.city_combo = ttk.Combobox(main_frame, values=cities, state="readonly")
        self.city_combo.set(cities[0] if cities else "")
        self.city_combo.pack(fill=tk.X, pady=5)

        # 2. Station Inputs
        ttk.Label(main_frame, text="Departure Station:").pack(pady=5)
        self.start_ent = ttk.Entry(main_frame)
        self.start_ent.pack(fill=tk.X, pady=5)

        ttk.Label(main_frame, text="Arrival Station:").pack(pady=5)
        self.end_ent = ttk.Entry(main_frame)
        self.end_ent.pack(fill=tk.X, pady=5)

        # 3. Action Button
        self.calc_btn = ttk.Button(
            main_frame, 
            text="Find Best Route", 
            command=self._on_click
        )
        self.calc_btn.pack(pady=20)

        # 4. Results Area (Itinerary)
        ttk.Label(main_frame, text="Itinerary:", font=('Helvetica', 10, 'bold')).pack(pady=5)
        self.results_area = tk.Text(main_frame, height=15, state='disabled', wrap='word', bg="#f8f9fa")
        self.results_area.pack(fill=tk.BOTH, expand=True)

    def _on_click(self):
        # Trigger the calculation in the Controller
        self.calc_callback(
            self.city_combo.get(),
            self.start_ent.get(),
            self.end_ent.get()
        )

    def update_results(self, text):
        """Clears the previous path and displays the new one[cite: 2]."""
        self.results_area.config(state='normal')
        self.results_area.delete('1.0', tk.END)  # This deletes the previous research[cite: 2]
        self.results_area.insert(tk.END, text)
        self.results_area.config(state='disabled')

    def show_error(self, message):
        messagebox.showerror("Error", message)