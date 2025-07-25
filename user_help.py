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

1️⃣ **Add Tasks or Commands:**
   ➕ Click the **Add New Entry** button.
   📝 Fill in:
      - Task/Command Name ✅
      - Cost, Value (numeric) 💰📈
      - Category (optional) 🗂️
   🔗 Optionally, define **dependencies** for tasks.
   🆗 Click **Save Tasks** to save your input.

2️⃣ **Edit / Remove Tasks or Commands:**
   🛠️ Go to the Edit/Remove section.
   📋 Select from the list.
   ✏️ Click **Load** to edit or
   🗑️ **Remove** to delete.
   💾 Hit **Save** to finalize changes.

3️⃣ **NEW: Load / Save via JSON 📂💾**
   🔹 **Load:** Import from a `.json` file.
      - Replaces current list with data from file.
      - Useful for batch-importing tasks.
   🔹 **Save:** Export your data to JSON.
      - Saves global state of tasks/commands.
   ⚠️ Shared globally—affects all pages.

4️⃣ **Command Execution Table 🚦**
   📑 Tracks:
      - Serial No. 🔢
      - Command Name 🏷️
      - Priority 🥇
      - Execution Status (Pending / Executed) ✅❌
      - Removal Count ❌➕
   🔁 Execute commands by **Serial No.**

5️⃣ **Task Dependencies 🔗**
   - When editing, specify dependencies as comma-separated task names.
   - ⚠️ Must match names **exactly** for scheduling to work.

6️⃣ **Execution & Optimization Engine 🤖**
   - Choose execution strategy:
     • **Value-Based** 🌟  
     • **Cost-Based** 💸  
     • **Cost-to-Value Ratio** 📊  
   - Dynamically highlighted in reports based on selection.
   - Choose strategy via Execution Panel.

7️⃣ **Real-Time Report Generation 📝📈**
   - Generate PDF reports showing:
     • Execution table with stats 📊  
     • Beautiful line/bar graphs 📉  
   - Automatically uses your current data & selected strategy.
   - File is saved for review 📁

8️⃣ **Interface & Theme 🖥️**
   - Use **Toggle Theme** to switch 🌗 Light / 🌘 Dark.
   - Scrollable lists for long entries 📜
   - Pages adjust to resizing 🖱️

9️⃣ **Navigation Shortcuts 🚀**
   - 🔁 **Ctrl + Right Arrow** → Next Page  
   - 🔁 **Ctrl + Left Arrow** → Previous Page  
   - 🧭 You can also click arrow buttons (top-left) to switch sections.

⚠️ **Tips:**
- Always **Save Tasks** after changes to reflect updates globally and in JSON.
- Numeric fields must be valid (Cost, Value).
- Match dependency names exactly!
- Use **Load** to quickly populate tasks from JSON.

📞 Need Help?
📃 Check README or contact the developer 👨‍💻 for support.

Thanks for using the app! 💖🚀
"""

    text_widget = tk.Text(
        guide_frame, wrap="word", bg=bg, fg=fg,
        font=("Segoe UI", 12), bd=0, relief="flat"
    )
    text_widget.insert("1.0", guide_text)
    text_widget.config(state="disabled")  # Read-only
    text_widget.pack(padx=20, pady=20, fill="both", expand=True)

    return guide_frame
