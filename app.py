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

# Add JavaScript to detect system theme
st.markdown(
    """
    <script>
        const darkThemeMq = window.matchMedia("(prefers-color-scheme: dark)");
        const urlParams = new URLSearchParams(window.location.search);
        if (!urlParams.has('theme')) {
            urlParams.set('theme', darkThemeMq.matches ? 'dark' : 'light');
            window.location.search = urlParams;
        }
    </script>
    """,
    unsafe_allow_html=True
)

# Get browser theme from URL parameters
try:
    browser_theme = st.query_params().get("theme", ["light"])[0]
except:
    browser_theme = "light"

# Theme definitions
THEMES = {
    # Dark themes (original)
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
        "not_taken": "#9A9A9A"
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
        "not_taken": "#888888"       
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
    },
    # New Light themes
    "Light Classic": {
        "primary": "#1976D2",
        "background": "#FFFFFF",
        "secondary_bg": "#F5F5F5",
        "text": "#000000",
        "button_text": "#FFFFFF",
        "plot_bg": "#FFFFFF",
        "paper_bg": "#FFFFFF",
        "grid": "#E0E0E0",
        "legend_bg": "rgba(245, 245, 245, 0.95)",
        "fully_taken": "#1B5E20",
        "partially_taken": "#E65100",
        "not_taken": "#757575"
    },
    "Mint Fresh": {
        "primary": "#00695C",
        "background": "#F2F7F5",
        "secondary_bg": "#E6F3F0",
        "text": "#000000",
        "button_text": "#FFFFFF",
        "plot_bg": "#F2F7F5",
        "paper_bg": "#F2F7F5",
        "grid": "#B2DFDB",
        "legend_bg": "rgba(230, 243, 240, 0.95)",
        "fully_taken": "#004D40",
        "partially_taken": "#E65100",
        "not_taken": "#607D8B"
    },
    "Rose Gold": {
        "primary": "#B71C1C",
        "background": "#FFF0F3",
        "secondary_bg": "#FFE4E8",
        "text": "#000000",
        "button_text": "#FFFFFF",
        "plot_bg": "#FFF0F3",
        "paper_bg": "#FFF0F3",
        "grid": "#FFCDD2",
        "legend_bg": "rgba(255, 228, 232, 0.95)",
        "fully_taken": "#880E4F",
        "partially_taken": "#BF360C",
        "not_taken": "#616161"
    },
    "Lavender Light": {
        "primary": "#4527A0",
        "background": "#F6F4FC",
        "secondary_bg": "#EDE7F6",
        "text": "#000000",
        "button_text": "#FFFFFF",
        "plot_bg": "#F6F4FC",
        "paper_bg": "#F6F4FC",
        "grid": "#D1C4E9",
        "legend_bg": "rgba(237, 231, 246, 0.95)",
        "fully_taken": "#311B92",
        "partially_taken": "#BF360C",
        "not_taken": "#616161"
    },
    "Sandy Beach": {
        "primary": "#E65100",
        "background": "#FDFBF3",
        "secondary_bg": "#F5F0E5",
        "text": "#000000",
        "button_text": "#FFFFFF",
        "plot_bg": "#FDFBF3",
        "paper_bg": "#FDFBF3",
        "grid": "#FFE0B2",
        "legend_bg": "rgba(245, 240, 229, 0.95)",
        "fully_taken": "#BF360C",
        "partially_taken": "#E65100",
        "not_taken": "#757575"
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
    Creates a Plotly bar chart visualization of the knapsack solution
    """
    # Prepare data for visualization - only include items that are taken (fully or partially)
    item_data = [(item, f"Item {item.item_id}") for item in items 
                 if item.status in ["fully_taken", "partially_taken"]]
    
    if not item_data:  # If no items are taken
        return None
        
    taken_items, item_ids = zip(*item_data)
    
    values = [item.value * item.fraction_taken for item in taken_items]  # Show actual value taken
    weights = [item.weight for item in taken_items]
    ratios = [item.ratio for item in taken_items]
    fractions = [item.fraction_taken for item in taken_items]
    
    # Color coding based on status
    colors = [theme["fully_taken"] if item.status == "fully_taken" 
             else theme["partially_taken"] for item in taken_items]
    
    # Create the bar chart
    fig = go.Figure()
    
    # Add bars for item values
    fig.add_trace(go.Bar(
        x=item_ids,
        y=values,
        name="Value Taken",
        marker_color=colors,
        text=[f"Weight: {w}<br>Ratio: {r:.2f}<br>Taken: {f:.1%}" 
              for w, r, f in zip(weights, ratios, fractions)],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>" +
                      "Value Taken: %{y:.2f}<br>" +
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
        xaxis_title="Selected Items",
        yaxis_title="Value Taken",
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
        text="<b>Legend:</b><br>Fully taken<br>Partially taken",
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

        /* Comprehensive sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {theme["secondary_bg"]} !important;
            color: {theme["text"]} !important;
        }}
        
        [data-testid="stSidebar"] > div:first-child {{
            background-color: {theme["secondary_bg"]} !important;
        }}
        
        [data-testid="stSidebar"] .st-bx {{
            background-color: {theme["secondary_bg"]} !important;
            color: {theme["text"]} !important;
        }}
        
        [data-testid="stSidebar"] .st-c0 {{
            color: {theme["text"]} !important;
        }}
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .st-bq,
        [data-testid="stSidebar"] .st-bc,
        [data-testid="stSidebar"] .st-bd,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {{
            color: {theme["text"]} !important;
        }}
        
        [data-testid="stSidebar"] input[type="number"] {{
            color: {theme["text"]} !important;
        }}

        /* Dataframe styling */
        div[data-testid="stDataFrame"] {{
            background-color: {theme["secondary_bg"]} !important;
            border-radius: 5px;
        }}
        
        div[data-testid="stDataFrame"] .data-grid-container {{
            background-color: {theme["secondary_bg"]} !important;
        }}
        
        div[data-testid="stDataFrame"] * {{
            color: {theme["text"]} !important;
        }}

        /* Other containers */
        div[data-testid="stExpander"],
        div[data-testid="stInfo"] {{
            background-color: {theme["secondary_bg"]} !important;
            border-radius: 5px;
        }}
        
        div[data-testid="stInfo"] * {{
            color: {theme["text"]} !important;
        }}

        /* Button styling */
        .stButton>button {{
            background-color: {theme["primary"]} !important;
            color: {theme["button_text"]} !important;
            border: none;
            border-radius: 5px;
            font-weight: 600;
            width: 100%;
            margin: 5px 0;
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

        /* Step container styling */
        .step-container {{
            background-color: {theme["secondary_bg"]};
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
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
    
    # Sidebar configuration
    st.sidebar.header("Configuration")
    
    # Theme selector
    st.sidebar.subheader("Theme")
    
    # Split themes into dark and light categories
    dark_themes = {k: v for k, v in THEMES.items() if k in ["Dark", "Ocean", "Dracula", "Cyberpunk", "Purple Palace", "Solar Ember"]}
    light_themes = {k: v for k, v in THEMES.items() if k in ["Light Classic", "Mint Fresh", "Rose Gold", "Lavender Light", "Sandy Beach"]}
    
    # Select appropriate themes based on browser theme
    if browser_theme == "dark":
        available_themes = dark_themes
        default_theme = "Dark"
    else:
        available_themes = light_themes
        default_theme = "Light Classic"
    
    # Initialize theme in session state if not set or if theme type doesn't match browser preference
    if ('selected_theme' not in st.session_state or 
        (browser_theme == "dark" and st.session_state.selected_theme not in dark_themes) or 
        (browser_theme == "light" and st.session_state.selected_theme not in light_themes)):
        st.session_state.selected_theme = default_theme
    
    # Theme selector
    selected_theme = st.sidebar.selectbox(
        "Choose Color Theme:",
        list(available_themes.keys()),
        index=list(available_themes.keys()).index(st.session_state.selected_theme),
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
    
    # Initialize items
    if 'knapsack_items' not in st.session_state:
        st.session_state.knapsack_items = []
    
    # Generate random data
    if input_method == "Random Generation":
        if st.sidebar.button("Generate Random Data"):
            np.random.seed()
            st.session_state.knapsack_items = []
            for i in range(num_items):
                value = np.random.uniform(10, 100)
                weight = np.random.uniform(5, 30)
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
        st.subheader("Current Items")
        
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