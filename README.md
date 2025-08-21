

# 🧳 AI Virtual Travel Planner

An interactive **Travel Planning Application** built with **Python (Tkinter GUI)**.
It helps users choose destinations, plan routes, estimate costs, and generate itineraries using **AI algorithms (A\* Search + Genetic Algorithm)**.

---

## 🚀 Features

* **GUI Interface** (Tkinter) for easy input of preferences.
* **Destination Selection**: Choose from major world cities.
* **Budget & Duration**: Enter your travel budget and number of days.
* **Interests Filtering**: Culture, Food, Adventure, History, Museums, etc.
* **Optimal Route Calculation** using **A\*** search algorithm.
* **Itinerary Generation** using a **Genetic Algorithm** (optimized for budget, time, and interests).
* **Cost Estimation** (transport, accommodation, food, activities, misc).
* **Result Summary** with route, itinerary, and budget analysis.

---

## 🖥️ Tech Stack

* **Language:** Python 3
* **Libraries:**

  * `tkinter` (GUI framework)
  * `math`, `random` (algorithms & calculations)

---

## 📸 GUI Preview

*(Add a screenshot of your running app here — e.g., `assets/screenshot.png`)*

---

## 📂 Project Structure

```
project-AI.py       # Main source code (GUI + AI algorithms)
README.md           # Documentation (this file)
assets/             # (Optional) Screenshots or demo GIFs
```

---

## ⚙️ How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```
2. Run the app:

   ```bash
   python project-AI.py
   ```

---

## 🧠 Algorithms Used

* **A\* Search**: Finds the optimal travel route between destinations.
* **Genetic Algorithm**: Evolves multiple itineraries to suggest the best one based on fitness (budget, distance, interests, ratings).
* **Haversine Formula**: Calculates distances between cities using latitude/longitude.

---

## 📊 Example Output

```
Destinations: Paris, Rome, Barcelona
Start: Paris
Budget: $2000
Days: 7
Interests: Culture, Food

OPTIMAL ROUTE:
Paris -> Rome -> Barcelona
Distance: 2800 km
Time: 46.7 hrs

ITINERARY:
Day 1: Paris
Day 2: Rome
Day 3: Barcelona
Fitness: 456.78

COSTS:
Transportation: $300
Accommodation: $200
Activities: $450
Food: $350
Misc: $210
Total: $1510
Budget Status: Within budget
```

---

## 📝 Future Improvements

* Add real-world API integration (Google Maps, Skyscanner).
* Allow saving itineraries as PDF/Excel.
* Multi-user comparison & collaboration.
* Dark mode GUI.



