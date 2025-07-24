from globals import current_theme
import tkinter as tk

def user_guide(parent):
    bg = current_theme["bg"]
    fg = current_theme["fg"]

    guide_frame = tk.Frame(parent, bg=bg)
    guide_frame.pack(fill="both", expand=True)

    guide_text = """
📚✨ WELCOME TO THE TASK MANAGEMENT APP ✨📚

👋 Hello! Here's how to get started and make the most out of this app:

1️⃣ **Add Tasks:**
   ➕ Click the **Add New Entry** button.
   📝 Fill in the task details: 
      - Task Name (required)
      - Cost (numeric)
      - Value (numeric)
      - Category (optional)
   🆗 Press **Save Tasks** to save your changes.

2️⃣ **Edit / Remove Tasks:**
   🔍 Go to the Edit/Remove page.
   📋 Select a task from the list.
   ✏️ Click **Load** to edit details.
   🗑️ Click **Remove** to delete the selected task.
   💾 Click **Save** to update changes.

3️⃣ **Load / Save Data (New JSON Feature):**
   📂 **Load:** Imports tasks from the JSON file located at your specified path.
      - This replaces current tasks in the app with those loaded from the file.
      - Use it to quickly add many tasks at once without typing manually.
   💾 **Save:** Exports your current tasks to the JSON file.
      - Saves your current task list globally for use across all parts of the app.
      - Ensures your data persists between sessions.
   🔄 **Important:** Loaded tasks update the global tasks variable, which is shared app-wide.

4️⃣ **Task Dependencies:**
   🔗 When editing a task, specify dependencies as comma-separated task names.
   ⚠️ Ensure these names match existing tasks exactly for scheduling to work.

5️⃣ **Scheduling & Optimization:**
   🎯 Use the Scheduler to optimize tasks based on cost-to-value ratio.
   📈 Helps identify the best tasks to focus on within your constraints.

6️⃣ **UI and Usability Features:**
   🌗 Switch between Light and Dark themes using the **Toggle Theme** button.
   🖱️ Scrollable lists keep navigation smooth even with many tasks.
   📋 Tables and labels dynamically adjust when resizing the window.

7️⃣ **Shortcuts for Power Users:**
   ⌨️ Use **Ctrl + Right Arrow** and **Ctrl + Left Arrow** to quickly switch between pages.

⚠️ **Tips:**
- Always **Save Tasks** after edits to update both the global variable and JSON file.
- Numeric fields (Cost, Value) must be valid numbers to avoid errors.
- Task dependencies should exactly match other task names for correct behavior.
- Use **Load** to quickly pull data from your JSON file, replacing current tasks.

📞 Need Help?
Check the README or contact the developer for assistance.

Thank you for using the app! 🚀
"""

    text_widget = tk.Text(
        guide_frame, wrap="word", bg=bg, fg=fg, font=("Segoe UI", 12), bd=0, relief="flat"
    )
    text_widget.insert("1.0", guide_text)
    text_widget.config(state="disabled")  # Read-only
    text_widget.pack(padx=20, pady=20, fill="both", expand=True)

    return guide_frame
