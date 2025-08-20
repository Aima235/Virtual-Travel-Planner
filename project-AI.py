import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import math

class TravelPlannerGUI:
    def __init__(self, root):  #  Correct constructor name
        self.root = root
        self.root.title("AI Travel Planner")
        self.root.geometry("900x600")
        self.destinations = self.get_destinations()
        self.distances = self.calc_distances()
        self.create_widgets()

    def get_destinations(self):
        return {
            "New York": {"coordinates": [40.71, -74.00], "categories": ["Culture", "Museums", "Nightlife", "Food"], "base_cost": 200, "rating": 4.5},
            "Paris": {"coordinates": [48.85, 2.35], "categories": ["Culture", "Museums", "Food", "History"], "base_cost": 180, "rating": 4.7},
            "Tokyo": {"coordinates": [35.67, 139.65], "categories": ["Culture", "Food", "Nightlife", "Museums"], "base_cost": 220, "rating": 4.6},
            "London": {"coordinates": [51.50, -0.12], "categories": ["Culture", "History", "Museums", "Nightlife"], "base_cost": 190, "rating": 4.4},
            "Rome": {"coordinates": [41.90, 12.49], "categories": ["History", "Culture", "Food", "Museums"], "base_cost": 150, "rating": 4.5},
            "Barcelona": {"coordinates": [41.38, 2.17], "categories": ["Culture", "Beach", "Food", "Museums"], "base_cost": 140, "rating": 4.3},
            "Sydney": {"coordinates": [-33.86, 151.20], "categories": ["Beach", "Culture", "Adventure", "Nightlife"], "base_cost": 170, "rating": 4.4},
            "Bangkok": {"coordinates": [13.75, 100.50], "categories": ["Culture", "Food", "Adventure", "Nightlife"], "base_cost": 80, "rating": 4.2},
            "Dubai": {"coordinates": [25.20, 55.27], "categories": ["Adventure", "Culture", "Nightlife", "Beach"], "base_cost": 250, "rating": 4.3},
            "Bali": {"coordinates": [-8.34, 115.09], "categories": ["Beach", "Nature", "Culture", "Adventure"], "base_cost": 100, "rating": 4.6}
        }

    def calc_distances(self):
        d = {}
        for k1, v1 in self.destinations.items():
            d[k1] = {}
            for k2, v2 in self.destinations.items():
                if k1 == k2:
                    d[k1][k2] = 0
                else:
                    d[k1][k2] = self.haversine(v1["coordinates"], v2["coordinates"])
        return d

    def haversine(self, c1, c2):
        lat1, lon1, lat2, lon2 = map(math.radians, [*c1, *c2])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2  # ✅ fixed formula
        return 6371 * 2 * math.asin(math.sqrt(a))

    def create_widgets(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=1)

        left = ttk.LabelFrame(main, text="Preferences", padding=10)
        left.pack(side="left", fill="y")

        right = ttk.LabelFrame(main, text="Results", padding=10)
        right.pack(side="right", fill="both", expand=1)

        ttk.Label(left, text="Destinations:").pack(anchor="w")
        self.dest_list = tk.Listbox(left, selectmode=tk.MULTIPLE, height=6)
        for d in self.destinations:
            self.dest_list.insert(tk.END, d)
        self.dest_list.pack(fill="x")

        ttk.Label(left, text="Start:").pack(anchor="w")
        self.start_var = tk.StringVar()
        self.start_combo = ttk.Combobox(left, textvariable=self.start_var, values=list(self.destinations))
        self.start_combo.pack(fill="x")

        ttk.Label(left, text="Budget ($):").pack(anchor="w")
        self.budget_var = tk.StringVar(value="2000")
        ttk.Entry(left, textvariable=self.budget_var).pack(fill="x")

        ttk.Label(left, text="Duration (days):").pack(anchor="w")
        self.duration_var = tk.StringVar(value="7")
        ttk.Entry(left, textvariable=self.duration_var).pack(fill="x")

        ttk.Label(left, text="Interests:").pack(anchor="w")
        self.interest_vars = {}
        cats = sorted({c for v in self.destinations.values() for c in v["categories"]})
        for c in cats:
            v = tk.BooleanVar()
            self.interest_vars[c] = v
            ttk.Checkbutton(left, text=c, variable=v).pack(anchor="w")

        ttk.Button(left, text="Generate Plan", command=self.generate_plan).pack(pady=10, fill="x")

        self.results = scrolledtext.ScrolledText(right, wrap=tk.WORD, width=60, height=30)
        self.results.pack(fill="both", expand=1)

    def get_selected(self):
        idxs = self.dest_list.curselection()
        return [self.dest_list.get(i) for i in idxs]

    def get_interests(self):
        return [k for k, v in self.interest_vars.items() if v.get()]

    def generate_plan(self):
        try:
            dests = self.get_selected()
            start = self.start_var.get()
            budget = float(self.budget_var.get())
            days = int(self.duration_var.get())
            ints = self.get_interests()

            if len(dests) < 2:
                messagebox.showerror("Error", "Select at least 2 destinations")
                return
            if start not in dests:
                messagebox.showerror("Error", "Start must be in destinations")
                return
            if budget <= 0 or days <= 0:
                messagebox.showerror("Error", "Budget/days must be positive")
                return

            self.results.delete(1.0, tk.END)

            route = self.astar_route(dests, start)
            itinerary = self.genetic_itinerary(dests, start, budget, days, ints)
            costs = self.calc_costs(dests, days, ints)
            total = sum(costs.values())
            self.display_results(dests, start, budget, days, ints, route, itinerary, costs, total)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def astar_route(self, dests, start):
        path = [start]
        unvisited = set(dests) - {start}
        curr = start
        dist = 0
        while unvisited:
            nxt = min(unvisited, key=lambda d: self.distances[curr][d])
            dist += self.distances[curr][nxt]
            path.append(nxt)
            curr = nxt
            unvisited.remove(nxt)
        return {"path": path, "distance": dist, "time": dist/60, "count": len(path)}

    def genetic_itinerary(self, dests, start, budget, days, ints):
        pop = [[start] + random.sample([d for d in dests if d != start], len(dests)-1) for _ in range(10)]
        for _ in range(30):
            pop.sort(key=lambda ind: -self.fitness(ind, budget, days, ints))
            pop = pop[:5] + [self.mutate(ind[:]) for ind in pop[:5]]
        best = max(pop, key=lambda ind: self.fitness(ind, budget, days, ints))
        return {"itinerary": best, "fitness": self.fitness(best, budget, days, ints)}

    def fitness(self, ind, budget, days, ints):
        dist = sum(self.distances[ind[i]][ind[i+1]] for i in range(len(ind)-1))
        cost = dist*0.5 + (len(ind)-1)*100 + sum(self.destinations[d]['base_cost'] for d in ind)
        interest = sum(len(set(self.destinations[d]['categories']) & set(ints))*10 + self.destinations[d]['rating']*5 for d in ind)
        penalty = max(0, (cost - budget)/budget) * 100
        return 1000/(1 + dist/100) + interest - penalty

    def mutate(self, ind):
        if len(ind) > 2:
            i, j = random.sample(range(1, len(ind)), 2)
            ind[i], ind[j] = ind[j], ind[i]
        return ind

    def calc_costs(self, dests, days, ints):
        t = (len(dests)-1) * 150
        a = (len(dests)-1) * 100
        act = sum(self.destinations[d]['base_cost'] * max(1, len(set(ints) & set(self.destinations[d]['categories'])) * 0.5) for d in dests)
        f, m = days * 50, days * 30
        return {'Transportation': t, 'Accommodation': a, 'Activities': act, 'Food': f, 'Misc': m}

    def display_results(self, dests, start, budget, days, ints, route, itinerary, costs, total):
        r = self.results
        r.insert(tk.END, f"Destinations: {', '.join(dests)}\nStart: {start}\nBudget: ${budget}\nDays: {days}\nInterests: {', '.join(ints)}\n\n")
        r.insert(tk.END, f"OPTIMAL ROUTE:\n{' -> '.join(route['path'])}\nDistance: {route['distance']:.1f} km\nTime: {route['time']:.1f} hrs\n\n")
        r.insert(tk.END, "ITINERARY:\n" + "\n".join(f"Day {i+1}: {d}" for i, d in enumerate(itinerary['itinerary'])) + "\nFitness: %.2f\n\n" % itinerary['fitness'])
        r.insert(tk.END, "COSTS:\n" + "\n".join(f"{k}: ${v:.2f}" for k, v in costs.items()) + f"\nTotal: ${total:.2f}\n")
        r.insert(tk.END, "Budget Status: " + ("Within budget" if total <= budget else "Over budget") + "\n")

def main():
    root = tk.Tk()
    app = TravelPlannerGUI(root)
    root.mainloop()

if __name__ == "__main__":  #  correct check
    main()
