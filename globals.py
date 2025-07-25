# themes
from themes import LIGHT_THEME, DARK_THEME
current_theme = LIGHT_THEME

# Task list
tasks = []
budget = 100
parallelism = 2
constraints = []

# Results for graphs
current_results = {
    "efficiency": [],              # List or array of efficiency values over time or tasks
    "constraint_utilization": [],  # Constraint usage data
    "schedule_cost": [],           # Cost values over time or tasks
    # Add any other metrics you want to visualize
}

# Task Execution Status Tracking
executed_tasks = set()     # Holds names/IDs of executed tasks
removed_tasks = set()      # Tracks tasks removed before execution
execution_type = "Value-Based"  # Default execution type, can be "Cost-Based", "Value-Based", or "Cost-to-Value-Based"