import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict

# Configure the page
st.set_page_config(
    page_title="Fractional Knapsack Visualizer",
    layout="wide"
)

# Theme definitions
THEMES = {
    # Dark themes
    "Dark": {
        "primary": "#D32F2F",
        "background": "#0E1117",
        "secondary_bg": "#262730",
        "text": "#FAFAFA",
        "button_text": "#FFFFFF",
        "plot_bg": "#1E1E1E",
        "paper_bg": "#0E1117",
        "grid": "#3E3E3E",
        "legend_bg": "rgba(38, 39, 48, 0.9)",
        "fully_taken": "#2E8B57",
        "partially_taken": "#FF8C00",
        "not_taken": "#A9A9A9",
        "type": "dark"
    },
    "Ocean": {
        "primary": "#00CED1",
        "background": "#0A192F",
        "secondary_bg": "#172A45",
        "text": "#CCD6F6",
        "button_text": "#0A192F",
        "plot_bg": "#0A192F",
        "paper_bg": "#0A192F",
        "grid": "#233554",
        "legend_bg": "rgba(23, 42, 69, 0.9)",
        "fully_taken": "#64FFDA",
        "partially_taken": "#FFA07A",
        "not_taken": "#8892B0",
        "type": "dark"
    },
    "Dracula": {
        "primary": "#BD93F9",
        "background": "#282A36",
        "secondary_bg": "#44475A",
        "text": "#F8F8F2",
        "button_text": "#F8F8F2",
        "plot_bg": "#282A36",
        "paper_bg": "#282A36",
        "grid": "#44475A",
        "legend_bg": "rgba(68, 71, 90, 0.9)",
        "fully_taken": "#50FA7B",
        "partially_taken": "#FFB86C",
        "not_taken": "#9A9A9A",
        "type": "dark"
    },
    "Cyberpunk": {
        "primary": "#00FFFF",
        "background": "#0A0A0A",
        "secondary_bg": "#212121",
        "text": "#E0E0E0",
        "button_text": "#0A0A0A",
        "plot_bg": "#0A0A0A",
        "paper_bg": "#0A0A0A",
        "grid": "#333333",
        "legend_bg": "rgba(33, 33, 33, 0.9)",
        "fully_taken": "#00FF7F",
        "partially_taken": "#FFD700",
        "not_taken": "#888888",
        "type": "dark"       
    },
    "Purple Palace": {
        "primary": "#C77DFF",
        "background": "#1A0E2E",
        "secondary_bg": "#2D1B4E",
        "text": "#E8D4F2",
        "button_text": "#1A0E2E",
        "plot_bg": "#1A0E2E",
        "paper_bg": "#1A0E2E",
        "grid": "#3E2A5C",
        "legend_bg": "rgba(45, 27, 78, 0.9)",
        "fully_taken": "#C77DFF",
        "partially_taken": "#FFAFCC",
        "not_taken": "#7B68A6",
        "type": "dark"
    },
    "Solar Ember": {
        "primary": "#FF7B00",
        "background": "#1B1A17",
        "secondary_bg": "#2C2A25",
        "text": "#F4EDE4",
        "button_text": "#1B1A17",
        "plot_bg": "#1B1A17",
        "paper_bg": "#1B1A17",
        "grid": "#3C3A35",
        "legend_bg": "rgba(44, 42, 37, 0.9)",
        "fully_taken": "#FFB347",
        "partially_taken": "#FF8C42",
        "not_taken": "#A68A64",
        "type": "dark"
    },
    # Light themes
    "Light Classic": {
        "primary": "#1976D2",
        "background": "#FFFFFF",
        "secondary_bg": "#F5F5F5",
        "text": "#212121",
        "button_text": "#FFFFFF",
        "plot_bg": "#FFFFFF",
        "paper_bg": "#FFFFFF",
        "grid": "#E0E0E0",
        "legend_bg": "rgba(245, 245, 245, 0.95)",
        "fully_taken": "#1B5E20",
        "partially_taken": "#E65100",
        "not_taken": "#757575",
        "type": "light"
    },
    "Mint Fresh": {
        "primary": "#00695C",
        "background": "#F2F7F5",
        "secondary_bg": "#E6F3F0",
        "text": "#212121",
        "button_text": "#FFFFFF",
        "plot_bg": "#F2F7F5",
        "paper_bg": "#F2F7F5",
        "grid": "#B2DFDB",
        "legend_bg": "rgba(230, 243, 240, 0.95)",
        "fully_taken": "#004D40",
        "partially_taken": "#E65100",
        "not_taken": "#607D8B",
        "type": "light"
    },
    "Rose Gold": {
        "primary": "#B71C1C",
        "background": "#FFF0F3",
        "secondary_bg": "#FFE4E8",
        "text": "#212121",
        "button_text": "#FFFFFF",
        "plot_bg": "#FFF0F3",
        "paper_bg": "#FFF0F3",
        "grid": "#FFCDD2",
        "legend_bg": "rgba(255, 228, 232, 0.95)",
        "fully_taken": "#880E4F",
        "partially_taken": "#BF360C",
        "not_taken": "#616161",
        "type": "light"
    },
    "Lavender Light": {
        "primary": "#4527A0",
        "background": "#F6F4FC",
        "secondary_bg": "#EDE7F6",
        "text": "#212121",
        "button_text": "#FFFFFF",
        "plot_bg": "#F6F4FC",
        "paper_bg": "#F6F4FC",
        "grid": "#D1C4E9",
        "legend_bg": "rgba(237, 231, 246, 0.95)",
        "fully_taken": "#311B92",
        "partially_taken": "#BF360C",
        "not_taken": "#616161",
        "type": "light"
    },
    "Sandy Beach": {
        "primary": "#E65100",
        "background": "#FDFBF3",
        "secondary_bg": "#F5F0E5",
        "text": "#212121",
        "button_text": "#FFFFFF",
        "plot_bg": "#FDFBF3",
        "paper_bg": "#FDFBF3",
        "grid": "#FFE0B2",
        "legend_bg": "rgba(245, 240, 229, 0.95)",
        "fully_taken": "#BF360C",
        "partially_taken": "#E65100",
        "not_taken": "#757575",
        "type": "light"
    }
}

class KnapsackItem:
    """Represents an item in the knapsack problem"""
    def __init__(self, item_id: int, value: float, weight: float):
        self.item_id = item_id
        self.value = value
        self.weight = weight
        self.ratio = value / weight if weight > 0 else 0
        self.fraction_taken = 0.0
        self.status = "not_taken"  # "fully_taken", "partially_taken", "not_taken"

def fractional_knapsack(items: List[KnapsackItem], capacity: float) -> Tuple[float, List[KnapsackItem], List[str]]:
    """
    Implements the Fractional Knapsack algorithm using greedy approach
    """
    # Reset all items
    for item in items:
        item.fraction_taken = 0.0
        item.status = "not_taken"
    
    # Sort items by value/weight ratio
    sorted_items = sorted(items, key=lambda x: x.ratio, reverse=True)
    
    total_value = 0.0
    remaining_capacity = capacity
    step_log = []
    
    return total_value, sorted_items, step_log

def create_visualization(items: List[KnapsackItem], capacity: float, total_value: float, theme: Dict):
    """
    Creates a Plotly bar chart visualization of the knapsack solution,
    showing the percentage taken for ALL items, sorted by ratio.
    """
    
    # --- THIS IS THE FIX ---
    # 1. We no longer filter. We use all items, already sorted by ratio
    #    from the 'processed_data'.
    
    item_ids = [f"Item {item.item_id}" for item in items]
    percentages = [item.fraction_taken * 100 for item in items] # Y-axis is now percentage
    
    # 2. Get full item details for hover data
    values = [item.value for item in items]
    weights = [item.weight for item in items]
    ratios = [item.ratio for item in items]
    
    # 3. Assign colors based on the *new* logic
    colors = []
    for item in items:
        if item.status == "fully_taken":
            colors.append(theme["fully_taken"])
        elif item.status == "partially_taken":
            colors.append(theme["partially_taken"])
        else:
            colors.append(theme["not_taken"]) # Add the "not_taken" color
    
    # Create the bar chart
    fig = go.Figure()
    
    # 4. Add bars, changing Y-axis to percentages
    fig.add_trace(go.Bar(
        x=item_ids,
        y=percentages, # Y-axis is now percentages
        name="Percentage Taken",
        marker_color=colors,
        # 5. Update text and hovertemplate for the new Y-axis
        text=[f"{p:.1f}%" for p in percentages],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>" +
                      "Percentage Taken: %{y:.1f}%<br>" +
                      "Ratio: %{customdata[0]:.2f}<br>" +
                      "Value: %{customdata[1]:.2f}<br>" +
                      "Weight: %{customdata[2]}<br>" +
                      "<extra></extra>",
        customdata=list(zip(ratios, values, weights))
    ))
    
    # 6. Update layout with new titles and theme colors
    fig.update_layout(
        title={
            'text': f"Fractional Knapsack Solution (Sorted by Ratio)<br><sub>Total Value: {total_value:.2f} | Capacity: {capacity}</sub>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': theme["text"], 'size': 20}
        },
        xaxis_title="Items (Sorted by Value/Weight Ratio)",
        yaxis_title="Percentage Taken (%)", # New Y-axis title
        yaxis_range=[0, 105], # Set Y-axis to go from 0 to 105 (for padding)
        xaxis={
            'title_font': {'color': theme["text"]}, 
            'tickfont': {'color': theme["text"]},
            'gridcolor': theme["grid"]
        },
        yaxis={
            'title_font': {'color': theme["text"]}, 
            'tickfont': {'color': theme["text"]},
            'gridcolor': theme["grid"]
        },
        height=500,
        showlegend=False,
        plot_bgcolor=theme["plot_bg"],
        paper_bgcolor=theme["paper_bg"],
        font={'color': theme["text"]}
    )
    
    # 7. Add the new "Not Taken" category to the legend
    fig.add_annotation(
        x=0.02, y=0.98,
        xref="paper", yref="paper",
        text="<b>Legend:</b><br>" +
             f"<span style='color:{theme['fully_taken']};'>■</span> Fully taken<br>" +
             f"<span style='color:{theme['partially_taken']};'>■</span> Partially taken<br>" +
             f"<span style='color:{theme['not_taken']};'>■</span> Not taken",
        showarrow=False,
        bgcolor=theme["legend_bg"],
        bordercolor=theme["grid"],
        borderwidth=1,
        align="left",
        font={'color': theme["text"]}
    )
    
    return fig


def apply_custom_css(theme: Dict):
    """Apply custom CSS based on selected theme"""
    css = f"""
    <style>
        /* Main app background */
        .stApp {{
            background-color: {theme["background"]};
            color: {theme["text"]};
        }}
        
        /* Sidebar background */
        section[data-testid="stSidebar"] {{
            background-color: {theme["secondary_bg"]} !important;
        }}
        
        /* Sidebar text elements */
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stRadio label {{
            color: {theme["text"]} !important;
        }}
        
        /* Main content headers */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            color: {theme["text"]} !important;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background-color: {theme["secondary_bg"]} !important;
            color: {theme["text"]} !important;
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: {theme["primary"]};
            color: {theme["button_text"]};
            border: none;
            border-radius: 5px;
            font-weight: 600;
        }}
        
        .stButton > button:hover {{
            opacity: 0.85;
        }}
        
        /* Disabled buttons */
        .stButton > button:disabled {{
            opacity: 0.4;
            cursor: not-allowed;
        }}
        
        /* Metrics */
        [data-testid="metric-container"] {{
            background-color: {theme["secondary_bg"]};
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        [data-testid="stMetricValue"] {{
            color: {theme["primary"]};
        }}
        
        /* Dataframe */
        .dataframe {{
            background-color: {theme["secondary_bg"]} !important;
        }}
        
        /* Info box */
        .stAlert {{
            background-color: {theme["secondary_bg"]};
            color: {theme["text"]};
        }}
        
        /* Number input */
        .stNumberInput label {{
            color: {theme["text"]} !important;
        }}
        
        /* Select box */
        .stSelectbox label {{
            color: {theme["text"]} !important;
        }}
        
        /* Radio button */
        .stRadio > label {{
            color: {theme["text"]} !important;
        }}

        [data-testid="stMetricLabel"] {{
            color: {theme["text"]} !important;
            opacity: 1 !important;
        }}
        
        .stRadio [role="radiogroup"] label > div:last-child {{
            color: {theme["text"]} !important;
            opacity: 1 !important; 
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def process_step_1(items: List[KnapsackItem]) -> List[KnapsackItem]:
    """Calculate ratios and sort items"""
    sorted_items = sorted(items, key=lambda x: x.ratio, reverse=True)
    return sorted_items

def process_step_2(sorted_items: List[KnapsackItem], capacity: float) -> Tuple[float, List[KnapsackItem]]:
    """Process items and calculate what can be taken"""
    remaining_capacity = capacity
    total_value = 0.0
    
    for item in sorted_items:
        if remaining_capacity <= 0:
            break
            
        if item.weight <= remaining_capacity:
            # Take the entire item
            item.fraction_taken = 1.0
            item.status = "fully_taken"
            total_value += item.value
            remaining_capacity -= item.weight
        else:
            # Take a fraction of the item
            fraction = remaining_capacity / item.weight
            item.fraction_taken = fraction
            item.status = "partially_taken"
            value_gained = item.value * fraction
            total_value += value_gained
            remaining_capacity = 0
            
    return total_value, sorted_items

def main():
    """Main Streamlit application"""
    
    # Initialize session states
    if 'selected_theme' not in st.session_state:
        st.session_state.selected_theme = "Light Classic"
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 0
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = "light"  # Default to light mode
    
    # Get current theme
    current_theme = THEMES[st.session_state.selected_theme]
    
    # Apply custom CSS
    apply_custom_css(current_theme)
    
    # App header
    st.title("Fractional Knapsack Problem Visualizer")
    st.markdown("---")
    
    # Educational content - Algorithm explanation
    st.markdown("""
### 1. Defining the Optimization Problem

The Fractional Knapsack problem is a classic **optimization problem**. This means we are trying to **maximize** a specific outcome (our objective) while adhering to a set of **constraints**.

We are given:
* A set of $n$ items.
* A knapsack with a maximum weight capacity $W$.
* Each item $i$ has a **value** $v_i$ and a **weight** $w_i$.

**The Goal (Objective Function):**
Our objective is to **maximize** the total value in the knapsack. We do this by choosing a fraction $x_i$ for each item, where $0 \le x_i \le 1$.
* $x_i = 1$ means we take 100% of item $i$.
* $x_i = 0$ means we take 0% of item $i$.
* $x_i = 0.5$ means we take 50% of item $i$.

The total value we want to maximize is formally written as:
$$
\t{Maximize: } \sum_{i=1}^{n} v_i \cdot x_i
$$

**The Limitation (Constraint):**
We are limited by the knapsack's capacity. The total weight of the fractions we take cannot exceed $W$.
$$
\t{WMax: } \sum_{i=1}^{n} w_i \cdot x_i \le W
$$

---

### 2. The Greedy Algorithm Solution

The optimal solution for this problem can be found using an efficient **greedy strategy**. This strategy works by always making the choice that seems best at the moment.

**Step 1: Calculate Value Density**
The "greedy" choice is based on the **value-to-weight ratio**, or *value density*, for each item. This represents the "value per unit of weight."
* **Formula**:""")
                
    st.latex(r"{ratio}_i = {v_i}/{w_i}")

    st.markdown("""**Step 2: Sort by Density**
Sort all items in **descending order** based on their $\t{ratio}_i$. This places the most "efficient" items first.

**Step 3: Fill the Knapsack**
Iterate through the sorted items and add them to the knapsack (let's say `current_weight = 0` and `total_value = 0`):
1.  For each item $i$ in sorted order:
2.  Check if the item fits completely: `if current_weight + w_i < W`
3.  **If it fits:** Take the whole item ($x_i = 1$).
    * `total_value = total_value + v_i`
    * `current_weight = current_weight + w_i`
4.  **If it doesn't fit:** Take the largest possible fraction to fill the knapsack exactly.
    * `remaining_capacity = W - current_weight`
    * `fraction = remaining_capacity / w_i`
    * Set $x_i = \t{fraction}$.
    * Total Value = Total Value + `(v_i/fraction)`
    * The knapsack is now full. **Break** the loop.
                
---

### 3. Example: The "Last-Moment-Preparation" Problem 

Let's apply this. It's the night before final exams, and you've only got **8 hours** left to study. This is your **capacity ($W = 8$)**.

You have several topics, each with a potential point gain (value, $v_i$) and the total time needed (weight, $w_i$).

| Topic | Potential Point Gain ($v_i$) | Full Study Time ($w_i$) |
| :--- | :--- | :--- |
| **Python** | 20 points | 4 hours |
| **Paradigms of Algorithms** | 30 points | 10 hours |
| **Asymptotic Notation** | 12 points | 2 hours |

**Goal:** Maximize your total point gain within the 8-hour constraint.

---

### 4. Applying the Greedy Solution

**Step 1: Calculate Value Density (Points per Hour)**
We calculate $\t{ratio}_i = v_i / w_i$ for each subject.

* **Asymptotic Notation:** 12 points / 2 hours = **6 points/hour**
* **Python:** 20 points / 4 hours = **5 points/hour**
* **Paradigms of Algorithms:** 30 points / 10 hours = **3 points/hour**

**Step 2: Sort by Density (Highest to Lowest)**
1.  Asymptotic Notation (6 pts/hr)
2.  Python (5 pts/hr)
3.  Paradigms of Algorithms (3 pts/hr)

**Step 3: Fill the "Knapsack" (Your 8-Hour Schedule)**

1.  **Take Asymptotic Notation:**
    * We take all of it. $x_{asymptotic} = 1$.
    * **Time Used:** 2 hours.
    * **Points Gained:** 12.
    * **Time Remaining:** $8 - 2 = 6$ hours.

2.  **Take Python:**
    * We take all of it. $x_{python} = 1$.
    * **Time Used:** 4 hours.
    * **Points Gained:** 20.
    * **Time Remaining:** $6 - 4 = 2$ hours.""")


    st.markdown("""3.  **Take a Fraction of Paradigms of Algorithms:**
    * We only have 2 hours left, but the subject "weighs" 10 hours.
    * The fraction we take is:
""")

#FIX EQUATION
    st.latex(r"x_{paradigms} = \fraction{\text{Time Remaining}}{\text{Full Time}} = \frac{2}{10} = 0.2")

    st.markdown(r"""
    * **Time Used:** 2 hours.
    * **Points Gained:** $0.2 \times 30 \text{ points} = 6$.
    * **Time Remaining:** $2 - 2 = 0$ hours.""")

    st.markdown("""**Final Result:**
Your schedule is full.
Your total maximized gain is **12 (from Asymptotic Notation) + 20 (from Python) + 6 (from Paradigms) = 38 points**.


### 3. Why the Greedy Strategy is Optimal

This greedy strategy is **guaranteed to be optimal** for the *fractional* problem (Note: it is *not* optimal for the 0/1 Knapsack problem where you can't take fractions).

The proof of optimality, common in algorithm textbooks, uses an **"exchange argument"**:
* Imagine there is a *different* solution (let's call it $S_{other}$) that is *better* (higher value) than the greedy solution ($S_{greedy}$).
* This means $S_{other}$ must have used *less* of some high-ratio item $i$ and *more* of some lower-ratio item $j$ compared to $S_{greedy}$.
* Because we can take fractions, we can *always* improve $S_{other}$'s value. We can "swap" some of the low-ratio item $j$ *out* and "swap" an equivalent *weight* of the high-ratio item $i$ *in*.
* Since item $i$ has more value per weight, this swap will **increase** the total value of $S_{other}$.
* This contradicts our initial assumption that $S_{other}$ was the "better" solution.
* Therefore, no solution can be better than the greedy solution, proving $S_{greedy}$ is optimal.
""")
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    
    # Theme selector
    st.sidebar.subheader("Theme Settings")
    
    # Theme mode toggle
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Light", use_container_width=True, 
                    disabled=(st.session_state.theme_mode == "light")):
            st.session_state.theme_mode = "light"
            # Switch to a light theme if current theme is dark
            if THEMES[st.session_state.selected_theme]["type"] == "dark":
                st.session_state.selected_theme = "Light Classic"
            st.rerun()
    
    with col2:
        if st.button("Dark", use_container_width=True,
                    disabled=(st.session_state.theme_mode == "dark")):
            st.session_state.theme_mode = "dark"
            # Switch to a dark theme if current theme is light
            if THEMES[st.session_state.selected_theme]["type"] == "light":
                st.session_state.selected_theme = "Dark"
            st.rerun()
    
    # Filter themes based on mode
    if st.session_state.theme_mode == "dark":
        available_themes = {k: v for k, v in THEMES.items() if v["type"] == "dark"}
    else:
        available_themes = {k: v for k, v in THEMES.items() if v["type"] == "light"}
    
    # Ensure selected theme matches current mode
    if st.session_state.selected_theme not in available_themes:
        st.session_state.selected_theme = list(available_themes.keys())[0]
    
    # Theme selector
    selected_theme = st.sidebar.selectbox(
        f"Choose {st.session_state.theme_mode.title()} Theme:",
        list(available_themes.keys()),
        index=list(available_themes.keys()).index(st.session_state.selected_theme),
        help=f"Select a {st.session_state.theme_mode} theme for the application"
    )
    
    # Update theme if changed
    if selected_theme != st.session_state.selected_theme:
        st.session_state.selected_theme = selected_theme
        st.rerun()
    
  
    st.sidebar.markdown("---")
    
    # Number of items
    num_items = st.sidebar.number_input(
        "Number of Items",
        min_value=1,
        max_value=20,
        value=5,
        help="Choose how many items to include in the problem"
    )
    
    # Knapsack capacity
    capacity = st.sidebar.number_input(
        "Knapsack Capacity",
        min_value=1.0,
        max_value=1000.0,
        value=75.0,
        step=5.0,
        help="Maximum weight the knapsack can hold"
    )
    
    # Data input method
    st.sidebar.subheader("Data Input Method")
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Manual Entry", "Random Generation"]
    )
    
    # Initialize items
    if 'knapsack_items' not in st.session_state:
        st.session_state.knapsack_items = []
    
    # Generate random data
    if input_method == "Random Generation":
        if st.sidebar.button("Generate Random Data"):
            np.random.seed()
            st.session_state.knapsack_items = []
            for i in range(num_items):
                value = np.random.uniform(10, 150)
                weight = np.random.uniform(1, 100)
                st.session_state.knapsack_items.append(KnapsackItem(i + 1, round(value, 1), round(weight, 1)))
            st.session_state.current_step = 0
            st.session_state.processed_data = None
    
    # Manual data entry
    elif input_method == "Manual Entry":
        st.sidebar.subheader("Item Details")
        
        while len(st.session_state.knapsack_items) < num_items:
            item_id = len(st.session_state.knapsack_items) + 1
            st.session_state.knapsack_items.append(KnapsackItem(item_id, 10.0, 5.0))
        
        st.session_state.knapsack_items = st.session_state.knapsack_items[:num_items]
        
        for i in range(num_items):
            st.sidebar.write(f"**Item {i + 1}:**")
            col1, col2 = st.sidebar.columns(2)
            
            with col1:
                value = st.number_input(
                    f"Value {i + 1}",
                    min_value=0.1,
                    value=st.session_state.knapsack_items[i].value,
                    step=0.1,
                    key=f"value_{i}"
                )
            
            with col2:
                weight = st.number_input(
                    f"Weight {i + 1}",
                    min_value=0.1,
                    value=st.session_state.knapsack_items[i].weight,
                    step=0.1,
                    key=f"weight_{i}"
                )
            
            st.session_state.knapsack_items[i].value = value
            st.session_state.knapsack_items[i].weight = weight
            st.session_state.knapsack_items[i].ratio = value / weight
    
    # Main content area
    if st.session_state.knapsack_items:
        # Display current items
        st.subheader("Run a Simulation")
        
        items_data = []
        for item in st.session_state.knapsack_items:
            items_data.append({
                "Item ID": item.item_id,
                "Value": item.value,
                "Weight": item.weight,
                "Value/Weight Ratio": round(item.ratio, 3)
            })
        
        df = pd.DataFrame(items_data)
        st.dataframe(df, use_container_width=True)
        
        # Start button
        if st.session_state.current_step == 0:
            if st.button("Start Algorithm", type="primary"):
                st.session_state.current_step = 1
                st.session_state.processed_data = process_step_1(st.session_state.knapsack_items)
                st.rerun()
        
        # Step 1: Show sorted items
        if st.session_state.current_step >= 1:
            st.markdown("### Step 1: Calculate Value/Weight Ratios")
            st.markdown("Items are sorted by their value/weight ratio in descending order:")
            
            sorted_data = []
            for item in st.session_state.processed_data:
                sorted_data.append({
                    "Item ID": item.item_id,
                    "Value": item.value,
                    "Weight": item.weight,
                    "Value/Weight Ratio": round(item.ratio, 3)
                })
            
            st.dataframe(pd.DataFrame(sorted_data), use_container_width=True)
            
            if st.session_state.current_step == 1:
                if st.button("Next Step", type="primary"):
                    st.session_state.current_step = 2
                    total_value, processed_items = process_step_2(st.session_state.processed_data, capacity)
                    st.session_state.total_value = total_value
                    st.session_state.processed_data = processed_items
                    st.rerun()
        
        # Step 2: Show item selection
        if st.session_state.current_step >= 2:
            st.markdown("### Step 2: Select Items")
            st.markdown("Items are selected based on their ratio until the knapsack is full:")
            
            results_data = []
            for item in st.session_state.processed_data:
                status_marker = {
                    "fully_taken": "[+]", 
                    "partially_taken": "[~]", 
                    "not_taken": "[X]"
                }
                results_data.append({
                    "Item ID": item.item_id,
                    "Value": item.value,
                    "Weight": item.weight,
                    "Ratio": round(item.ratio, 3),
                    "Fraction Taken": f"{item.fraction_taken:.1%}",
                    "Value Gained": round(item.value * item.fraction_taken, 2),
                    "Status": f"{status_marker[item.status]} {item.status.replace('_', ' ').title()}"
                })
            
            st.dataframe(pd.DataFrame(results_data), use_container_width=True)
            
            # Show metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Value", f"{st.session_state.total_value:.2f}")
            with col2:
                st.metric("Capacity Used", f"{capacity:.1f}")
            with col3:
                efficiency = (st.session_state.total_value / capacity) if capacity > 0 else 0
                st.metric("Value/Weight Efficiency", f"{efficiency:.2f}")
            
            if st.session_state.current_step == 2:
                if st.button("Show Final Visualization", type="primary"):
                    st.session_state.current_step = 3
                    st.rerun()
        
        # Step 3: Show visualization
        if st.session_state.current_step == 3:
            st.markdown("### Final Visualization")
            fig = create_visualization(
                st.session_state.processed_data, 
                capacity, 
                st.session_state.total_value, 
                current_theme
            )
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No items were selected for the knapsack.")
            
            if st.button("Start Over", type="primary"):
                st.session_state.current_step = 0
                st.session_state.processed_data = None
                st.rerun()
    
    else:
        st.info("Please configure items using the sidebar to get started!")
        
        # Show sample data button
        if st.button("Load Sample Data"):
            st.session_state.knapsack_items = [
                KnapsackItem(1, 60, 10),
                KnapsackItem(2, 100, 20),
                KnapsackItem(3, 120, 30),
                KnapsackItem(4, 80, 15),
                KnapsackItem(5, 40, 8)
            ]
            st.rerun()

if __name__ == "__main__":
    main()