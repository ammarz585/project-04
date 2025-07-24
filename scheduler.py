import globals as g  # make sure your globals module has current_results dict

def schedule_tasks(strategy, tasks, budget, parallelism):
    """
    Schedule tasks based on strategy and constraints.

    Parameters:
    - strategy: 'cost', 'value', or 'ratio' (value/cost)
    - tasks: list of dicts with keys: 'name', 'cost', 'value', 'category', 'dependencies'
    - budget: maximum allowed total cost
    - parallelism: max number of tasks per time slot

    Returns:
    - execution_slots: list of lists, where each inner list is tasks scheduled for one time slot
    - total_cost: sum of costs of all scheduled tasks
    - total_value: sum of values of all scheduled tasks
    """

    # Sort tasks based on strategy
    if strategy == "cost":
        sorted_tasks = sorted(tasks, key=lambda t: t["cost"])
    elif strategy == "value":
        sorted_tasks = sorted(tasks, key=lambda t: t["value"], reverse=True)
    elif strategy == "ratio":
        sorted_tasks = sorted(tasks, key=lambda t: (t["value"] / t["cost"]) if t["cost"] else 0, reverse=True)
    else:
        raise ValueError("Invalid strategy. Choose 'cost', 'value', or 'ratio'.")

    execution_slots = []
    current_slot = []
    current_slot_cost = 0
    total_cost = 0
    total_value = 0

    for task in sorted_tasks:
        task_cost = task["cost"]

        # Skip tasks that alone exceed the budget
        if task_cost > budget:
            continue

        # Check if task fits in current slot and budget
        if (len(current_slot) < parallelism) and (current_slot_cost + task_cost <= budget):
            current_slot.append(task)
            current_slot_cost += task_cost
            total_cost += task_cost
            total_value += task["value"]
        else:
            # Commit the current slot if not empty
            if current_slot:
                execution_slots.append(current_slot)

            # Start a new slot with the current task
            current_slot = [task]
            current_slot_cost = task_cost
            total_cost += task_cost
            total_value += task["value"]

    # Add the last slot if it has any tasks
    if current_slot:
        execution_slots.append(current_slot)

    # --- Prepare data for graphs and store in globals.current_results ---

    # Calculate efficiency per slot = total value / total cost per slot
    efficiency = []
    for slot in execution_slots:
        slot_value = sum(t["value"] for t in slot)
        slot_cost = sum(t["cost"] for t in slot)
        eff = (slot_value / slot_cost) if slot_cost else 0
        efficiency.append(eff)

    # Constraint utilization per slot = % utilization of parallelism (tasks scheduled / max parallelism * 100)
    constraint_utilization = [len(slot) / parallelism * 100 for slot in execution_slots]

    # Schedule cost per slot (sum of costs per slot)
    schedule_cost = [sum(t["cost"] for t in slot) for slot in execution_slots]

    # Store all results globally for graphs access
    g.current_results = {
        "efficiency": efficiency,
        "constraint_utilization": constraint_utilization,
        "schedule_cost": schedule_cost,
        "total_cost": total_cost,
        "total_value": total_value,
        "execution_slots": execution_slots,
    }

    return execution_slots, total_cost, total_value
