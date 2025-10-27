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
        "not_taken": "#A9A9A9"
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
        "not_taken": "#8892B0"
    },
    "Dracula": {
        "primary": "#BD93F9",        # Purple
        "background": "#282A36",     # Dark bg
        "secondary_bg": "#44475A",   # Lighter bg
        "text": "#F8F8F2",           # White text
        "button_text": "#F8F8F2",
        "plot_bg": "#282A36",
        "paper_bg": "#282A36",
        "grid": "#44475A",
        "legend_bg": "rgba(68, 71, 90, 0.9)",
        "fully_taken": "#50FA7B",    # Green
        "partially_taken": "#FFB86C",# Orange
        "not_taken": "#9A9A9A"       # Grey
    },
    "Cyberpunk": {
        "primary": "#00FFFF",        # Cyan
        "background": "#0A0A0A",     # Near Black
        "secondary_bg": "#212121",   # Dark Grey
        "text": "#E0E0E0",           # Light Grey
        "button_text": "#0A0A0A",    # Near Black
        "plot_bg": "#0A0A0A",
        "paper_bg": "#0A0A0A",
        "grid": "#333333",
        "legend_bg": "rgba(33, 33, 33, 0.9)",
        "fully_taken": "#00FF7F",    # Spring Green
        "partially_taken": "#FFD700",# Gold
        "not_taken": "#888888"       # Grey
    },
    "Purble Palace": {
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
        "not_taken": "#7B68A6"
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
    "not_taken": "#A68A64"
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
    
    Args:
        items: List of KnapsackItem objects
        capacity: Maximum weight capacity of the knapsack
    
    Returns:
        Tuple of (total_value, processed_items, step_log)
    """
    # Reset all items
    for item in items:
        item.fraction_taken = 0.0
        item.status = "not_taken"
    
    # Step 1: Sort items by value/weight ratio in descending order
    sorted_items = sorted(items, key=lambda x: x.ratio, reverse=True)
    
    total_value = 0.0
    remaining_capacity = capacity
    step_log = []
    
    step_log.append(f"**Step 1**: Sorted items by value/weight ratio:")
    for i, item in enumerate(sorted_items):
        step_log.append(f"   Item {item.item_id}: Ratio = {item.ratio:.2f} (Value: {item.value}, Weight: {item.weight})")
    
    step_log.append(f"\n**Step 2**: Processing items in order:")
    step_log.append(f"   Initial capacity: {capacity}")
    
    # Step 2: Greedily select items
    for i, item in enumerate(sorted_items):
        if remaining_capacity <= 0:
            step_log.append(f"   X Item {item.item_id}: Knapsack is full, skipping remaining items")
            break
            
        if item.weight <= remaining_capacity:
            # Take the entire item
            item.fraction_taken = 1.0
            item.status = "fully_taken"
            total_value += item.value
            remaining_capacity -= item.weight
            step_log.append(f"   + Item {item.item_id}: Taken fully (Value gained: {item.value}, Remaining capacity: {remaining_capacity})")
        else:
            # Take a fraction of the item
            fraction = remaining_capacity / item.weight
            item.fraction_taken = fraction
            item.status = "partially_taken"
            value_gained = item.value * fraction
            total_value += value_gained
            step_log.append(f"   ~ Item {item.item_id}: Taken {fraction:.2%} (Value gained: {value_gained:.2f}, Remaining capacity: 0)")
            remaining_capacity = 0
    
    step_log.append(f"\n**Final Result**: Total value = {total_value:.2f}")
    
    return total_value, sorted_items, step_log

def create_visualization(items: List[KnapsackItem], capacity: float, total_value: float, theme: Dict):
    """
    Creates a Plotly bar chart visualization of the knapsack solution
    """
    # Prepare data for visualization
    item_ids = [f"Item {item.item_id}" for item in items]
    values = [item.value for item in items]
    weights = [item.weight for item in items]
    ratios = [item.ratio for item in items]
    fractions = [item.fraction_taken for item in items]
    
    # Color coding based on status using theme colors
    colors = []
    for item in items:
        if item.status == "fully_taken":
            colors.append(theme["fully_taken"])
        elif item.status == "partially_taken":
            colors.append(theme["partially_taken"])
        else:
            colors.append(theme["not_taken"])
    
    # Create the bar chart
    fig = go.Figure()
    
    # Add bars for item values
    fig.add_trace(go.Bar(
        x=item_ids,
        y=values,
        name="Item Value",
        marker_color=colors,
        text=[f"Weight: {w}<br>Ratio: {r:.2f}<br>Taken: {f:.1%}" 
              for w, r, f in zip(weights, ratios, fractions)],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>" +
                      "Value: %{y}<br>" +
                      "Weight: %{customdata[0]}<br>" +
                      "Ratio: %{customdata[1]:.2f}<br>" +
                      "Fraction Taken: %{customdata[2]:.1%}<extra></extra>",
        customdata=list(zip(weights, ratios, fractions))
    ))
    
    # Update layout with theme colors
    fig.update_layout(
        title={
            'text': f"Fractional Knapsack Solution<br><sub>Total Value: {total_value:.2f} | Capacity: {capacity}</sub>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'color': theme["text"], 'size': 20}
        },
        xaxis_title="Items (sorted by value/weight ratio)",
        yaxis_title="Item Value",
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
    
    # Add color legend as annotations
    fig.add_annotation(
        x=0.02, y=0.98,
        xref="paper", yref="paper",
        text="<b>Legend:</b><br>Fully taken<br>Partially taken<br>Not taken",
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
        [data-testid="stAppViewContainer"] {{
            background-color: {theme["background"]} !important;
            color: {theme["text"]} !important;
        }}

        /* === FIX 1: Sidebar Background === */
        /* Target the inner div of the sidebar */
        [data-testid="stSidebar"] > div:first-child {{
            background-color: {theme["secondary_bg"]} !important;
        }}
        
        /* Sidebar text */
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .st-bq {{
            color: {theme["text"]} !important;
        }}

        /* === FIX 2: Dataframe === */
        /* Target the dataframe container */
        div[data-testid="stDataFrame"] {{
            background-color: {theme["secondary_bg"]} !important;
            border-radius: 5px;
        }}
        
        /* Target the *inner* grid of the dataframe */
        div[data-testid="stDataFrame"] .data-grid-container {{
            background-color: {theme["secondary_bg"]} !important;
        }}
        
        /* Target all text elements *inside* the dataframe and expander */
        div[data-testid="stExpander"] *,
        div[data-testid="stDataFrame"] * {{
            color: {theme["text"]} !important;
        }}

        /* --- Other Containers (already working but good to keep) --- */
        
        div[data-testid="stExpander"],
        div[data-testid="stInfo"] {{
            background-color: {theme["secondary_bg"]} !important;
            border-radius: 5px;
        }}
        
        div[data-testid="stInfo"] * {{
            color: {theme["text"]} !important;
        }}

        /* --- Your Existing Styles --- */

        /* Button styling */
        .stButton>button {{
            background-color: {theme["primary"]} !important;
            color: {theme["button_text"]} !important;
            border: none;
            border-radius: 5px;
            font-weight: 600;
        }}
        .stButton>button:hover {{
            opacity: 0.8;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        
        /* Metric styling */
        div[data-testid="stMetricValue"] {{
            color: {theme["primary"]} !important;
        }}
        
        /* Header styling */
        h1, h2, h3 {{
            color: {theme["text"]} !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    
    # Initialize theme in session state
    if 'selected_theme' not in st.session_state:
        st.session_state.selected_theme = "Dark"
    
    # Get current theme
    current_theme = THEMES[st.session_state.selected_theme]
    
    # Apply custom CSS
    apply_custom_css(current_theme)
    
    # App header
    st.title("Fractional Knapsack Problem Visualizer")
    st.markdown("---")
    
    # Educational content - Algorithm explanation
    with st.expander("About the Fractional Knapsack Problem", expanded=False):
        st.markdown("""
        ### What is the Fractional Knapsack Problem?
        
        The **Fractional Knapsack Problem** is a classic optimization problem where you have:
        - A knapsack with limited weight capacity
        - A set of items, each with a value and weight
        - The goal: maximize the total value while staying within the weight limit
        - **Key difference**: You can take fractions of items (unlike 0/1 knapsack)
        
        ### The Greedy Algorithm Approach
        
        **Step 1**: Calculate the value/weight ratio for each item
        - **Formula**: `ratio = value ÷ weight`
        - This ratio represents "value per unit weight"
        
        **Step 2**: Sort items by ratio in descending order
        - Items with higher ratios are more "valuable per unit weight"
        
        **Step 3**: Greedily select items
        - Take items in order until the knapsack is full
        - If an item doesn't fit completely, take the fraction that fits
        
        ### Why Does This Work?
        The greedy approach works for the fractional knapsack because:
        - We can always improve by swapping a lower-ratio item for a higher-ratio one
        - Taking fractions allows us to fully utilize the knapsack capacity
        - The optimal solution always takes items in decreasing order of their ratios
        """)
    
    # Sidebar for inputs
    st.sidebar.header("Configuration")
    
    # Theme selector
    st.sidebar.subheader("Theme")
    theme_options = list(THEMES.keys())
    selected_theme = st.sidebar.selectbox(
        "Choose Color Theme:",
        theme_options,
        index=theme_options.index(st.session_state.selected_theme),
        help="Select a color theme for the application"
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
        value=50.0,
        step=5.0,
        help="Maximum weight the knapsack can hold"
    )
    
    # Data input method
    st.sidebar.subheader("Data Input Method")
    input_method = st.sidebar.radio(
        "Choose input method:",
        ["Manual Entry", "Random Generation"]
    )
    
    # Initialize session state for items
    if 'knapsack_items' not in st.session_state:
        st.session_state.knapsack_items = []
    
    # Generate random data button
    if input_method == "Random Generation":
        if st.sidebar.button("Generate Random Data"):
            np.random.seed()
            st.session_state.knapsack_items = []
            for i in range(num_items):
                value = np.random.uniform(10, 100)
                weight = np.random.uniform(5, 30)
                st.session_state.knapsack_items.append(KnapsackItem(i + 1, round(value, 1), round(weight, 1)))
    
    # Manual data entry
    elif input_method == "Manual Entry":
        st.sidebar.subheader("Item Details")
        
        # Ensure we have the right number of items in session state
        while len(st.session_state.knapsack_items) < num_items:
            item_id = len(st.session_state.knapsack_items) + 1
            st.session_state.knapsack_items.append(KnapsackItem(item_id, 10.0, 5.0))
        
        # Remove excess items if num_items decreased
        st.session_state.knapsack_items = st.session_state.knapsack_items[:num_items]
        
        # Input fields for each item
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
            
            # Update the item
            st.session_state.knapsack_items[i].value = value
            st.session_state.knapsack_items[i].weight = weight
            st.session_state.knapsack_items[i].ratio = value / weight
    
    # Main content area
    if st.session_state.knapsack_items:
        # Display current items
        st.subheader("Current Items")
        
        # Create a dataframe for display
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
        
        # Run algorithm button
        if st.button("Run Visualization", type="primary"):
            # Run the algorithm
            total_value, processed_items, step_log = fractional_knapsack(st.session_state.knapsack_items, capacity)
            
            # Store results in session state
            st.session_state.total_value = total_value
            st.session_state.processed_items = processed_items
            st.session_state.step_log = step_log
            st.session_state.capacity_used = capacity - sum(item.weight * (1 - item.fraction_taken) for item in processed_items)
        
        # Display results if available
        if hasattr(st.session_state, 'total_value'):
            st.markdown("---")
            st.subheader("Results")
            
            # Key metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Value", f"{st.session_state.total_value:.2f}")
            with col2:
                st.metric("Capacity Used", f"{capacity:.1f}")
            with col3:
                efficiency = (st.session_state.total_value / capacity) if capacity > 0 else 0
                st.metric("Value/Weight Efficiency", f"{efficiency:.2f}")
            
            # Visualization
            st.subheader("Visualization")
            fig = create_visualization(st.session_state.processed_items, capacity, st.session_state.total_value, current_theme)
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed results table
            st.subheader("Detailed Results")
            
            results_data = []
            for item in st.session_state.processed_items:
                status_marker = {"fully_taken": "[+]", "partially_taken": "[~]", "not_taken": "[X]"}
                results_data.append({
                    "Item ID": item.item_id,
                    "Value": item.value,
                    "Weight": item.weight,
                    "Ratio": round(item.ratio, 3),
                    "Fraction Taken": f"{item.fraction_taken:.1%}",
                    "Value Gained": round(item.value * item.fraction_taken, 2),
                    "Status": f"{status_marker[item.status]} {item.status.replace('_', ' ').title()}"
                })
            
            results_df = pd.DataFrame(results_data)
            st.dataframe(results_df, use_container_width=True)
            
            # Algorithm steps
            with st.expander("Algorithm Steps", expanded=False):
                for step in st.session_state.step_log:
                    st.markdown(step)
    
    else:
        st.info("Please configure items using the sidebar to get started!")
        
        # Show sample data button for quick start
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
