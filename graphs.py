import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore
from matplotlib.figure import Figure  # type: ignore
import numpy as np
from scipy.interpolate import make_interp_spline  # type: ignore
import globals as g

class GraphsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=g.current_theme['bg'])
        
        self.title_label = tk.Label(self, text="Graphs and Efficiency Reports",
                                    font=("Arial", 16, "bold"),
                                    bg=g.current_theme['bg'], fg=g.current_theme['fg'])
        self.title_label.pack(pady=10)
        
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.tooltip = None
        self.plotted_points = []
        self.draw_graphs()

        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def draw_graphs(self):
        self.fig.clear()

        efficiency = g.current_results.get("efficiency", [0])
        constraint_util = g.current_results.get("constraint_utilization", [0])
        schedule_cost = g.current_results.get("schedule_cost", [0])

        bg_color = g.current_theme['bg']
        fg_color = g.current_theme['fg']
        grid_color = "#444444" if bg_color != "#ffffff" else "#cccccc"

        ax1 = self.fig.add_subplot(131, facecolor=bg_color)
        ax2 = self.fig.add_subplot(132, facecolor=bg_color)
        ax3 = self.fig.add_subplot(133, facecolor=bg_color)

        def style_axis(ax):
            ax.set_facecolor(bg_color)
            ax.title.set_color(fg_color)
            ax.xaxis.label.set_color(fg_color)
            ax.yaxis.label.set_color(fg_color)
            ax.tick_params(axis='x', colors=fg_color)
            ax.tick_params(axis='y', colors=fg_color)
            ax.grid(True, color=grid_color, linestyle='--', alpha=0.5)
            for spine in ax.spines.values():
                spine.set_color(fg_color)

        def plot_wavy(ax, y, color, label=None, marker='o', wavy=True):
            x = np.arange(len(y))
            if len(x) > 3:
                xnew = np.linspace(x.min(), x.max(), 300)
                spline = make_interp_spline(x, y, k=3)
                y_smooth = spline(xnew)
                if wavy:
                    amplitude = 0.03 * (max(y) - min(y) + 1e-6)
                    frequency = 15
                    y_smooth += amplitude * np.sin(2 * np.pi * frequency * (xnew - x.min()) / (x.max() - x.min()))
                ax.plot(xnew, y_smooth, color=color, linewidth=3, label=label, alpha=0.9)
                ax.fill_between(xnew, y_smooth, color=color, alpha=0.25)
                ax.scatter(x, y, color=color, s=80, edgecolor='k', linewidth=1.2, marker=marker, zorder=5)
                return xnew, y_smooth, x, y
            else:
                ax.plot(x, y, color=color, linewidth=2, label=label, alpha=0.85)
                ax.scatter(x, y, color=color, s=60, edgecolor='k', linewidth=0.8, marker=marker, zorder=5)
                return x, y, x, y

        self.plotted_points.clear()

        x_smooth1, y_smooth1, x_orig1, y_orig1 = plot_wavy(ax1, efficiency, '#1f77b4', wavy=True)
        style_axis(ax1)
        ax1.set_title("Efficiency", fontweight='bold', fontsize=12)
        ax1.set_xlabel("Task/Time")
        ax1.set_ylabel("Efficiency")
        self.plotted_points.append({
            "ax": ax1,
            "x_smooth": x_smooth1,
            "y_smooth": y_smooth1,
            "x_orig": x_orig1,
            "y_orig": y_orig1,
            "label": "Efficiency",
            "type": "line"
        })

        bars = ax2.bar(range(len(constraint_util)), constraint_util, color='#ff7f0e', edgecolor='black', alpha=0.8)
        style_axis(ax2)
        ax2.set_title("Constraint Utilization", fontweight='bold', fontsize=12)
        ax2.set_xlabel("Constraint ID")
        ax2.set_ylabel("Utilization (%)")
        bar_x = np.array([bar.get_x() + bar.get_width() / 2 for bar in bars])
        bar_y = np.array([bar.get_height() for bar in bars])
        self.plotted_points.append({
            "ax": ax2,
            "x": bar_x,
            "y": bar_y,
            "label": "Constraint Utilization",
            "type": "bar",
            "bars": bars
        })

        x_smooth3, y_smooth3, x_orig3, y_orig3 = plot_wavy(ax3, schedule_cost, '#2ca02c', marker='x', wavy=True)
        style_axis(ax3)
        ax3.set_title("Schedule Cost", fontweight='bold', fontsize=12)
        ax3.set_xlabel("Task/Time")
        ax3.set_ylabel("Cost")
        self.plotted_points.append({
            "ax": ax3,
            "x_smooth": x_smooth3,
            "y_smooth": y_smooth3,
            "x_orig": x_orig3,
            "y_orig": y_orig3,
            "label": "Schedule Cost",
            "type": "line"
        })

        self.fig.tight_layout()
        self.canvas.draw()

    def on_mouse_move(self, event):
        if event.inaxes is None:
            self.hide_tooltip()
            return

        # Get mouse pixel coordinates relative to canvas
        mx_pixel, my_pixel = event.x, event.y

        for data in self.plotted_points:
            if data["ax"] != event.inaxes:
                continue

            # Convert data points to pixel coordinates for accurate distance check
            ax = data["ax"]
            trans = ax.transData.transform

            if data["type"] == "line":
                points = np.column_stack((data["x_orig"], data["y_orig"]))
                points_pix = trans(points)
                mouse_point = np.array([mx_pixel, my_pixel])
                dists = np.linalg.norm(points_pix - mouse_point, axis=1)
                min_idx = np.argmin(dists)
                min_dist = dists[min_idx]

                threshold_pixels = 10  # pixels distance to trigger tooltip

                if min_dist < threshold_pixels:
                    val = data["y_orig"][min_idx]
                    self.show_tooltip(
                        event.guiEvent.x_root + 10 if hasattr(event, 'guiEvent') else event.x_root + 10,
                        event.guiEvent.y_root + 10 if hasattr(event, 'guiEvent') else event.y_root + 10,
                        f"{data['label']} Point\nIndex: {min_idx}\nValue: {val:.3f}"
                    )
                    return

                # Also check smooth curve (optional, but less meaningful than original points)
                points_smooth = np.column_stack((data["x_smooth"], data["y_smooth"]))
                points_smooth_pix = trans(points_smooth)
                dists_smooth = np.linalg.norm(points_smooth_pix - mouse_point, axis=1)
                min_dist_smooth = np.min(dists_smooth)

                if min_dist_smooth < threshold_pixels / 2:  # smaller threshold for smooth curve
                    min_idx_smooth = np.argmin(dists_smooth)
                    val_smooth = data["y_smooth"][min_idx_smooth]
                    self.show_tooltip(
                        event.guiEvent.x_root + 10 if hasattr(event, 'guiEvent') else event.x_root + 10,
                        event.guiEvent.y_root + 10 if hasattr(event, 'guiEvent') else event.y_root + 10,
                        f"{data['label']} Curve\nIndex: {min_idx_smooth}\nValue: {val_smooth:.3f}"
                    )
                    return

            elif data["type"] == "bar":
                # Check if mouse is inside any bar rectangle (in data coords)
                mx, my = event.xdata, event.ydata
                for i, bar in enumerate(data["bars"]):
                    x0 = bar.get_x()
                    width = bar.get_width()
                    y0 = 0
                    height = bar.get_height()
                    if x0 <= mx <= x0 + width and y0 <= my <= y0 + height:
                        self.show_tooltip(
                            event.guiEvent.x_root + 10 if hasattr(event, 'guiEvent') else event.x_root + 10,
                            event.guiEvent.y_root + 10 if hasattr(event, 'guiEvent') else event.y_root + 10,
                            f"{data['label']} Bar\nIndex: {i}\nValue: {height:.3f}"
                        )
                        return

        self.hide_tooltip()

    def show_tooltip(self, x, y, text):
        if self.tooltip is None:
            self.tooltip = tk.Toplevel(self)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.attributes("-topmost", True)
            label = tk.Label(self.tooltip, text=text, background="yellow", relief="solid", borderwidth=1,
                             font=("Arial", 10))
            label.pack()
            self.tooltip.label = label
        else:
            self.tooltip.label.config(text=text)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        self.tooltip.deiconify()

    def hide_tooltip(self):
        if self.tooltip:
            self.tooltip.withdraw()

    def refresh_graph(self):
        self.draw_graphs()

def open_graphs_window(parent):
    return GraphsFrame(parent)
