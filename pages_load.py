from task_form_gui import open_task_form
from scheduler_tasks import open_results_window
from graphs import open_graphs_window
from user_help import user_guide
def load_task_form(container):
    return open_task_form(container)

def load_results_window(container):
    return open_results_window(container)

def load_graphs_window(container):
    return open_graphs_window(container)

def load_user_guide(container):
    return user_guide(container)