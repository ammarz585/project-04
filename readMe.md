# project-04
# 🤖 Complex Decision Maker

Welcome to the **Complex Decision Maker** — a powerful desktop application that helps you execute tasks based on intelligent strategies like **Value-Based**, **Cost-Based**, and **Cost-to-Value-Based** decision-making.

✨ This project was built using **Python**, **Tkinter GUI**, and **Matplotlib**, with a focus on real-time simulation, user control, and insightful PDF reports.

---

## 📌 Features

- 🔄 **Dynamic Task Execution**: Load tasks and execute them using multiple strategies.
- 📊 **Real-Time Graphs**: Visual representation of decision efficiency.
- 🧮 **Cost, Value, and Ratio-Based Scheduling**.
- 🧾 **Automated PDF Reports** with task tables and plots.
- 📂 **JSON Data Import Support** for loading pre-configured task sets.
- 🎨 **Dark/Light Theme Toggle**.
- 🧭 **Interactive User Guide** with colored emojis!
- 📋 **Execution Table** with status updates.
- 🖱️ Mouse wheel scroll support for task lists.
- 🧠 Shows constraints and parallelism handling (configurable).

---

## 🚀 Getting Started

### ✅ Prerequisites

Make sure you have Python 3.7+ installed.

### 📦 Install Required Packages

pip install matplotlib
pip install fpdf
🏁 Run the App
python main.py
🗃️ JSON Format for Importing Tasks
Use a .json file like this and import it using the app:

json
{
  "tasks": [
    { "name": "Task 01", "value": 20, "cost": 1000, "category": "A", "status": "Pending" },
    { "name": "Task 02", "value": 30, "cost": 1100, "category": "B", "status": "Pending" }
  ],
  "constraints": []
}
📸 Screenshots
🖥 Interface	
📈 Graph Output	
📄 PDF Report
🧠 Execution Strategies

Value-Based: Prioritizes highest value tasks first.
Cost-Based: Chooses the lowest cost tasks.
Cost-to-Value-Based: Selects based on the cost-to-value ratio for efficient execution.

# The selected strategy is highlighted in bold in the PDF report automatically.

📖 User Guide Highlights

📤 Import JSON tasks

🟢 Execute based on selected strategy

🧾 Generate reports with graphs & tables

🔄 Undo / Redo support

🖱️ Scroll through task list easily

🌗 Switch between Dark and Light themes

💡 Read guide via help section before use

🧠 Logic Insights

Tasks are stored and executed based on priority queues

Dynamic update of task status (Pending, Executed)

Execution Table tracks status + time stamping on report generation

Real-time graphical interpolation using make_interp_spline

Mouse scroll support for seamless navigation

🛠️ Tech Stack
Python 3.x
Tkinter
Matplotlib
FPDF
JSON File Handling

👨‍💻 Author

Made with 💙 by Ammar Zeeshan
Department of Computer Engineering, UET Taxila

📝 License

This project is open-source and free to use under the MIT License.