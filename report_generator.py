import tkinter as tk
from tkinter import messagebox, filedialog
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image  # type: ignore
from reportlab.lib.pagesizes import A4  # type: ignore
from reportlab.lib import colors  # type: ignore
from reportlab.lib.styles import getSampleStyleSheet  # type: ignore
from datetime import datetime
import matplotlib.pyplot as plt  # type: ignore
import globals as g
import os
import numpy as np

class ReportGeneratorPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=g.current_theme["bg"])

        tk.Label(self, text="📄 Generate Task Report as PDF", font=("Helvetica", 18, "bold"),
                 bg=g.current_theme["bg"], fg=g.current_theme["fg"]).pack(pady=20)

        tk.Label(self, text="Enter PDF file name (without .pdf):", font=("Arial", 12),
                 bg=g.current_theme["bg"], fg=g.current_theme["fg"]).pack(pady=5)
        self.filename_entry = tk.Entry(self, font=("Arial", 12), width=40)
        self.filename_entry.pack(pady=5)
        # Bind Enter key to generate_pdf method
        self.filename_entry.bind("<Return>", lambda event: self.generate_pdf())

        tk.Button(self, text="Generate PDF", font=("Arial", 12, "bold"),
                  bg=g.current_theme["button_bg"], fg=g.current_theme["button_fg"],
                  command=self.generate_pdf).pack(pady=20)

    def generate_pdf(self):
        if not g.tasks:
            messagebox.showerror("No Tasks", "⚠️ No tasks available to generate a report.")
            return

        name = self.filename_entry.get().strip()
        if not name:
            name = f"Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=name,
            title="Save Report As"
        )
        if not filename:
            return  # User cancelled

        try:
            self.generate_graphs()

            pdf = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []

            # Title
            elements.append(Paragraph("📊 Complex Decision Maker – Task Report", styles['Title']))
            elements.append(Spacer(1, 12))

            # Execution type description (reads from globals.execution_type)
            g.execution_type = getattr(g, "execution_type", "Value-Based")
            bold_type = f"<b>{g.execution_type}</b>"
            description_map = {
    "Value-Based": f"This report is based on {bold_type} execution results.",
    "Cost-Based": f"This report is based on {bold_type} execution results.",
    "Cost-to-Value-Based": f"This report is based on {bold_type} execution results."
}
            desc_text = description_map.get(g.execution_type, "This report is based on execution results.")
            elements.append(Paragraph(desc_text, styles['Normal']))
            elements.append(Spacer(1, 20))

            # Task Table
            data = [['Task', 'Cost', 'Value', 'Status']]
            for task in g.tasks:
                status = task.get('status', 'Pending')
                data.append([task['name'], str(task['cost']), str(task['value']), status])

            table = Table(data, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 20))

            # Summary Stats
            executed = sum(1 for t in g.tasks if t.get('status') == 'Executed')
            total = len(g.tasks)
            elements.append(Paragraph(f"✅ Executed Tasks: {executed} / {total}", styles['Normal']))
            elements.append(Paragraph(f"🕒 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            elements.append(Spacer(1, 12))

            # Add graphs images
            graph_files = ["report_efficiency.png", "report_constraint_utilization.png", "report_schedule_cost.png"]
            graph_titles = ["📈 Efficiency Over Time", "📊 Constraint Utilization", "💰 Schedule Cost"]

            for img_file, title in zip(graph_files, graph_titles):
                if os.path.exists(img_file):
                    elements.append(Paragraph(title, styles['Heading2']))
                    elements.append(Image(img_file, width=400, height=200))
                    elements.append(Spacer(1, 12))
                else:
                    elements.append(Paragraph(f"⚠️ {title} graph not available.", styles['Normal']))

            pdf.build(elements)
            messagebox.showinfo("Success", f"✅ Report saved as:\n{filename}")

            # Optionally, delete the generated images after PDF creation
            for f in graph_files:
                if os.path.exists(f):
                    os.remove(f)

        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to generate PDF:\n{e}")

    def generate_graphs(self):
        # Prepare data
        efficiency = g.current_results.get("efficiency", [])
        constraint_util = g.current_results.get("constraint_utilization", [])
        schedule_cost = g.current_results.get("schedule_cost", [])

        # Defaults if empty
        if not efficiency:
            efficiency = [0]
        if not constraint_util:
            constraint_util = [0]
        if not schedule_cost:
            schedule_cost = [0]

        # Efficiency graph
        plt.figure(figsize=(6, 3))
        plt.plot(efficiency, color='blue', marker='o')
        plt.title("Efficiency Over Time")
        plt.xlabel("Task/Time")
        plt.ylabel("Efficiency")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("report_efficiency.png")
        plt.close()

        # Constraint Utilization graph
        plt.figure(figsize=(6, 3))
        plt.bar(range(len(constraint_util)), constraint_util, color='orange', edgecolor='black')
        plt.title("Constraint Utilization")
        plt.xlabel("Constraint ID")
        plt.ylabel("Utilization (%)")
        plt.grid(axis='y')
        plt.tight_layout()
        plt.savefig("report_constraint_utilization.png")
        plt.close()

        # Schedule Cost graph
        plt.figure(figsize=(6, 3))
        plt.plot(schedule_cost, color='green', marker='x')
        plt.title("Schedule Cost Over Time")
        plt.xlabel("Task/Time")
        plt.ylabel("Cost")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("report_schedule_cost.png")
        plt.close()
