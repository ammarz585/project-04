import os
import sys
import json
from tkinter import messagebox
import globals as g

JSON_PATH = "import_data.json"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_data_from_json(filepath=None):
    if filepath is None:
        filepath = resource_path("import_data.json")
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        tasks = data.get('tasks', [])
        constraints = data.get('constraints', [])
        return tasks, constraints
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load JSON:\n{e}")
        return [], []


def save_data_to_json(filepath=JSON_PATH):
    try:
        with open(filepath, 'w') as file:
            json.dump({"tasks": g.tasks, "constraints": g.constraints}, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save JSON:\n{e}")
