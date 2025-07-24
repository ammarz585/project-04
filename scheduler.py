# scheduler.py
def schedule_tasks(strategy, tasks, budget, parallelism):
    """
    Schedule tasks by strategy:
    - strategy: 'cost', 'value', or 'ratio'
    - tasks: list of dict {name, cost, value, category, dependencies}
    - budget: max total cost allowed
    - parallelism: max tasks per slot

    Returns:
    - execution_slots: list of lists of tasks per time slot
    - total_cost: total cost of scheduled tasks
    - total_value: total value of scheduled tasks
    """

    if strategy == "cost":
        sorted_tasks = sorted(tasks, key=lambda t: t["cost"])
    elif strategy == "value":
        sorted_tasks = sorted(tasks, key=lambda t: t["value"], reverse=True)
    else:  # ratio
        sorted_tasks = sorted(tasks, key=lambda t: (t["value"] / t["cost"]) if t["cost"] else 0, reverse=True)

    execution_slots = []
    current_slot = []
    current_cost = 0
    total_cost = 0
    total_value = 0

    for task in sorted_tasks:
        if current_cost + task["cost"] <= budget and len(current_slot) < parallelism:
            current_slot.append(task)
            current_cost += task["cost"]
            total_cost += task["cost"]
            total_value += task["value"]
        else:
            if current_slot:
                execution_slots.append(current_slot)
            current_slot = []
            current_cost = 0
            if task["cost"] <= budget:
                current_slot.append(task)
                current_cost += task["cost"]
                total_cost += task["cost"]
                total_value += task["value"]

    if current_slot:
        execution_slots.append(current_slot)

    return execution_slots, total_cost, total_value
