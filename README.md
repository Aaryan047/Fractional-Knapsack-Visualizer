# 🎒 Fractional Knapsack Visualizer

An interactive **Streamlit app** that brings the *Fractional Knapsack Problem* to life with live charts, custom themes, and step-by-step algorithm tracing.

---

## Features

- **Greedy Algorithm Visualization**  
  Watch the algorithm sort, pick, and pack items dynamically.

- **Interactive Data Entry**  
  Add your own items or generate random ones instantly.

- **Dynamic Plotly Charts**  
  Bar graphs update in real time to show which items are fully, partially, or not taken.

- **Multiple Aesthetic Themes**
  Choose from:
  - 🕶️ Dark  
  - 🌊 Ocean  
  - 🧛 Dracula  
  - ⚡ Cyberpunk  
  - 💜 Purble Palace  
  - ☕ Solar Ember

- **Algorithm Walkthrough**  
  Step-by-step markdown explanation for learning and debugging.

---

## 🧠 What It Solves

The **Fractional Knapsack Problem** is a classic optimization challenge:  
> “Given a set of items, each with a weight and a value, determine the most valuable combination of items you can carry, where you can take *fractions* of items.”

This app visually demonstrates how the **greedy approach** sorts by `value/weight ratio` and fills the knapsack for maximum efficiency.

---

## 🧩 Tech Stack

- [Streamlit](https://streamlit.io/) for UI and interactivity  
- [Plotly](https://plotly.com/python/) for visualization  
- [Pandas](https://pandas.pydata.org/) for data handling  
- [NumPy](https://numpy.org/) for random generation and computation  

---

## ⚙️ Installation

```bash
git clone https://github.com/<your-username>/fractional-knapsack-visualizer.git
cd fractional-knapsack-visualizer
pip install -r requirements.txt
````

Or if you are using `pyproject.toml`:

```bash
pip install .
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open your browser at:

```
http://localhost:5000
```

---

## 🔮 Future Enhancements

* Add **0/1 Knapsack** mode toggle
* Export results as **PDF or CSV**
* Add **animation** for gradual item filling
* Include **efficiency heatmaps** or **value-per-capacity plots**

---

## 👨‍💻 Author

**Aaryan**
Engineering Student at NSUT
Passionate about algorithms, visualization, and bringing math to life.

📫 [LinkedIn](https://linkedin.com/in/aaryanvk047) • [GitHub](https://github.com/Aaryan047)

---

> “Algorithms are only as beautiful as the way we understand them.”
> :- Aaryan

```
