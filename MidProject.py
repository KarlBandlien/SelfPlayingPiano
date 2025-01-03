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

        # Manipulate only the x-value of the attack line
        attack_x_end = attack_value  # Use attack_value directly for x

        decay_duration = decay_value / 4
        decay_start_x = attack_x_end
        decay_end_x = decay_start_x + decay_duration
        
        sustain_start_x = decay_end_x
        sustain_end_x = sustain_start_x + 1.5

        release_start_x = sustain_end_x
        release_end_x = release_start_x + (release_value / 4)

        ax.clear()

        # Attack line (red)
        ax.plot([0, attack_x_end], [0, 1.0], color="red", linewidth=3, label="Attack Line")

        # Decay line (orange)
        ax.plot([decay_start_x, decay_end_x], [1.0, sustain_value], color="orange", linewidth=3, label="Decay Line")

        # Sustain line (green)
        ax.plot([sustain_start_x, sustain_end_x], [sustain_value, sustain_value], color="green", linewidth=3, label="Sustain Line")

        # Release line (yellow)
        ax.plot([release_start_x, release_end_x], [sustain_value, 0], color="blue", linewidth=3, label="Release Line")

        ax.set_title("Graph Representation")
        ax.set_ylabel("Values")
        ax.set_xlabel("Time")
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 2)
        ax.legend()
        canvas.draw()
    except Exception as e:
        print(f"Error updating graph: {e}")





def add_file():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("*.midi", "MIDI Files")]
    )
    if file_path:
        label.config(text=f"File Selected: {file_path}", fg="#4CAF50")

root = tk.Tk()
root.title("MIDI To KeyFrames")
root.geometry("1100x700")

label = tk.Label(root, text="Hello!!!", font=("Helvetica", 16, "bold"), fg="#4CAF50")
label.pack(pady=20)

validate_cmd = root.register(validate_numeric_input)

input_frame = tk.Frame(root, bg="#F5F5F5", bd=2, relief="groove")
input_frame.pack(pady=20, padx=10, fill="x", side="top")

style = ttk.Style()
style.configure("TEntry", padding=5, relief="flat", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12, "bold"), padding=5, foreground="#757575")

entries = []
labels = ["FPS", "Attack", "Decay", "Sustain", "Release"]


default_values = [30, 1.0, 1.0, 0.7, 1.0]

# Updated colors to match the graph lines
colors = ["#4CAF50", "red", "#FFC107", "green", "blue"]  # Green for sustain, red for attack

for i, (label_text, color, default_value) in enumerate(zip(labels, colors, default_values)):
    field_frame = tk.Frame(input_frame, bg="#F5F5F5")
    field_frame.pack(side="left", padx=15, pady=10)
    
    label = ttk.Label(field_frame, text=label_text, foreground=color)  # Use the updated colors here
    label.pack()
    entry = ttk.Entry(field_frame, validate="key", validatecommand=(validate_cmd, '%P'), justify="center")
    entry.pack(pady=5, ipadx=10, ipady=5)
    entry.insert(0, str(default_value))
    entry.bind("<KeyRelease>", lambda event: update_graph())
    entries.append(entry)

bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10, padx=10, fill="both", expand=True)

add_file_button = ttk.Button(bottom_frame, text="Add File", command=add_file)
add_file_button.pack(side="left", padx=10, pady=10)

graph_frame = tk.Frame(bottom_frame)
graph_frame.pack(side="left", fill="both", expand=True)

fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)

update_graph()

root.mainloop()
