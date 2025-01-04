import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def validate_numeric_input(new_value):
    try:
        if new_value == "" or float(new_value) >= 0:
            return True
    except ValueError:
        pass
    return False


def update_graph():
    try:
        attack_value = float(entries[1].get()) if entries[1].get() else 1.0
        decay_value = float(entries[2].get()) if entries[2].get() else 1.0
        sustain_value = float(entries[3].get()) if entries[3].get() else 0.7
        release_value = float(entries[4].get()) if entries[4].get() else 1.0

        # Halve the attack value
        attack_value /= 2

        # Manipulate only the x-value of the attack line
        attack_x_end = attack_value

        decay_duration = decay_value / 4
        decay_start_x = attack_x_end
        decay_end_x = decay_start_x + decay_duration

        sustain_start_x = decay_end_x
        sustain_end_x = sustain_start_x + 1.5

        release_start_x = sustain_end_x
        release_end_x = release_start_x + (release_value / 2)

        ax.clear()

        # Attack line (light red)
        ax.plot([0, attack_x_end], [0, 1.0], color="#E57373", linewidth=3, label="Attack Line")

        # Decay line (light orange)
        ax.plot([decay_start_x, decay_end_x], [1.0, sustain_value], color="#FFB74D", linewidth=3, label="Decay Line")

        # Sustain line (light green)
        ax.plot([sustain_start_x, sustain_end_x], [sustain_value, sustain_value], color="#81C784", linewidth=3,
                label="Sustain Line")

        # Release line (soft blue)
        ax.plot([release_start_x, release_end_x], [sustain_value, 0], color="#64B5F6", linewidth=3, label="Release Line")

        # Add circles at key points for aesthetics
        ax.scatter([attack_x_end, decay_end_x, sustain_end_x, release_end_x], 
                   [1.0, sustain_value, sustain_value, 0],
                   color='black', zorder=5, s=80, edgecolor="white", linewidth=2, label="Key Points")

        ax.set_title("Graph Representation")
        ax.set_ylabel("Positition")
        ax.set_xlabel("Time")
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 2)
        ax.legend()
        canvas.draw()
    except Exception as e:
        print(f"Error updating graph: {e}")


def adjust_value(index, adjustment):
    """Adjust the value in the entry by the given amount."""
    try:
        current_value = float(entries[index].get()) if entries[index].get() else 0.0
        new_value = max(0, round(current_value + adjustment, 1))  # Limit precision to 1 decimal place
        entries[index].delete(0, tk.END)
        entries[index].insert(0, f"{new_value:.1f}")  # Format to 1 decimal place
        update_graph()
    except ValueError:
        pass




root = tk.Tk()
root.title("MIDI To KeyFrames")
root.geometry("1100x700")

label = tk.Label(root, text="Hello!!!", font=("Helvetica", 16, "bold"), fg="#4CAF50")
label.pack(pady=20)

validate_cmd = root.register(validate_numeric_input)

input_frame = tk.Frame(root, bg="#E3F2FD", bd=2, relief="groove")  # Light blue background
input_frame.pack(pady=20, padx=10, fill="x", side="top")

style = ttk.Style()
style.configure("TEntry", padding=5, relief="flat", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12, "bold"), padding=5, foreground="#607D8B")  # Muted text color

entries = []
labels = ["FPS", "Attack", "Decay", "Sustain", "Release"]

default_values = [30, 1.0, 1.0, 0.7, 1.0]

# Updated colors to match the graph lines
colors = ["#4CAF50", "#E57373", "#FFB74D", "#81C784", "#64B5F6"]

for i, (label_text, color, default_value) in enumerate(zip(labels, colors, default_values)):
    field_frame = tk.Frame(input_frame, bg="#E3F2FD")
    field_frame.pack(side="left", padx=15, pady=10)

    label = ttk.Label(field_frame, text=label_text, foreground=color)
    label.pack()

    button_frame = tk.Frame(field_frame, bg="#E3F2FD")
    button_frame.pack(pady=5)

    # Create a darkened grey button with rounded corners
    decrement_button = tk.Button(button_frame, text="−", font=("Helvetica", 14, "bold"),
                                  command=lambda i=i: adjust_value(i, -0.1), width=3, height=1,
                                  bg="#757575", fg="white", relief="solid", borderwidth=2, highlightthickness=0)
    decrement_button.pack(side="left", padx=2)

    entry = ttk.Entry(button_frame, validate="key", validatecommand=(validate_cmd, '%P'), justify="center", width=8)
    entry.pack(side="left", padx=2, ipadx=5)
    entry.insert(0, f"{default_value:.1f}")  # Format to 1 decimal place
    entry.bind("<KeyRelease>", lambda event: update_graph())
    entries.append(entry)

    increment_button = tk.Button(button_frame, text="+", font=("Helvetica", 14, "bold"),
                                  command=lambda i=i: adjust_value(i, 0.1), width=3, height=1,
                                  bg="#757575", fg="white", relief="solid", borderwidth=2, highlightthickness=0)
    increment_button.pack(side="left", padx=2)















def add_file():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("*.midi", "MIDI Files")]
    )
    if file_path:
        label.config(text=f"File Selected: {file_path}", fg="#4CAF50")




 

# Bottom Frame
bottom_frame = tk.Frame(root, bg="#FAFAFA")  # Soft background color for aesthetics
bottom_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Left Rectangular Box with updated design
left_box = tk.Frame(
    bottom_frame,
    bg="#E3F2FD",  # Light blue background
    width=300,
    height=400,
    relief="ridge",  # A subtle ridge effect for borders
    bd=3,  # Border thickness
)
left_box.pack(side="left", padx=20, pady=10, fill="y")

# Add content to the updated rectangular box
content_label = tk.Label(
    left_box,
    text="Box Content",
    bg="#E3F2FD",
    font=("Helvetica", 14, "bold"),
    fg="#37474F",  # Muted text color for elegance
)
content_label.pack(pady=20)

example_button = tk.Button(
    left_box,
    text="Select MIDI File",
    font=("Helvetica", 12, "bold"),
    bg="#64B5F6",  # Vibrant button color
    fg="white",
    relief="raised",  # Slightly raised effect for buttons
    borderwidth=2,
)
example_button.pack(pady=10)

# Right Graph Area
graph_frame = tk.Frame(bottom_frame, bg="#FAFAFA")  # Matches the background color for consistency
graph_frame.pack(side="left", fill="both", expand=True)

# Matplotlib Graph
fig, ax = plt.subplots(figsize=(6, 4))  # Adjusted aspect ratio for a more balanced layout
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)

update_graph()

root.mainloop()
