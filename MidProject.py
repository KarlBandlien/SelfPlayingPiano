import tkinter as tk
from tkinter import filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import mido
import csv
from tkinter import messagebox

path_directory_var = ""

def midi_to_csv(midi_file, output_csv, fps=30):
    try:
        mid = mido.MidiFile(midi_file)
        notes = {}
        results = []
        bpm = None
        ticks_per_beat = mid.ticks_per_beat
        current_time = 0
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'set_tempo':
                    microseconds_per_beat = msg.tempo
                    bpm = 60000000 / microseconds_per_beat
                current_time += msg.time
                if msg.type == 'note_on':
                    if msg.velocity > 0:
                        notes[msg.note] = {
                            'channel': msg.channel,
                            'note_on': current_time,
                            'velocity': msg.velocity / 127
                        }
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    if msg.note in notes:
                        note_on_time = notes[msg.note]['note_on']
                        note_off_time = current_time
                        note_on_in_seconds = (note_on_time / ticks_per_beat) * (60 / bpm)
                        note_off_in_seconds = (note_off_time / ticks_per_beat) * (60 / bpm)
                        note_on_in_frames = note_on_in_seconds * fps
                        note_off_in_frames = note_off_in_seconds * fps
                        row = f"[{notes[msg.note]['channel']}, {msg.note}, {notes[msg.note]['velocity']}, {note_on_in_frames:.0f}, {note_off_in_frames:.0f}]"
                        results.append(row)
                        del notes[msg.note]
        with open(output_csv, 'w', newline='') as csvfile:
            csvfile.write(f"[{', '.join(results)}]")
        return bpm
    except Exception as e:
        print(f"Error during MIDI to CSV conversion: {e}")
        return None

def make_csv():
    if os.path.isfile(path_directory_var):
        midi_file = path_directory_var
        output_csv = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if output_csv:
            success = midi_to_csv(midi_file, output_csv)
            if success:
                messagebox.showinfo("Success", f"CSV file saved as {output_csv}")
            else:
                messagebox.showerror("Error", "An error occurred during conversion.")
    else:
        messagebox.showerror("Error", "No valid file selected. Please select a MIDI file.")

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
        attack_value /= 2
        attack_x_end = attack_value
        decay_duration = decay_value / 4
        decay_start_x = attack_x_end
        decay_end_x = decay_start_x + decay_duration
        sustain_start_x = decay_end_x
        sustain_end_x = sustain_start_x + 1.5
        release_start_x = sustain_end_x
        release_end_x = release_start_x + (release_value / 2)
        ax.clear()
        ax.plot([0, attack_x_end], [0, 1.0], color="#E57373", linewidth=3, label="Attack Line")
        ax.plot([decay_start_x, decay_end_x], [1.0, sustain_value], color="#FFB74D", linewidth=3, label="Decay Line")
        ax.plot([sustain_start_x, sustain_end_x], [sustain_value, sustain_value], color="#81C784", linewidth=3, label="Sustain Line")
        ax.plot([release_start_x, release_end_x], [sustain_value, 0], color="#64B5F6", linewidth=3, label="Release Line")
        ax.scatter([attack_x_end, decay_end_x, sustain_end_x, release_end_x], 
                   [1.0, sustain_value, sustain_value, 0], color='black', zorder=5, s=80, edgecolor="white", linewidth=2, label="Key Points")
        ax.set_title("Graph Representation")
        ax.set_ylabel("Position")
        ax.set_xlabel("Time")
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 2)
        ax.legend()
        canvas.draw()
    except Exception as e:
        print(f"Error updating graph: {e}")

def adjust_value(index, adjustment):
    try:
        current_value = float(entries[index].get()) if entries[index].get() else 0.0
        new_value = max(0, round(current_value + adjustment, 1))
        entries[index].delete(0, tk.END)
        entries[index].insert(0, f"{new_value:.1f}")
        update_graph()
    except ValueError:
        pass

def add_file():
    global path_directory_var
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("MIDI Files", "*.midi")]
    )
    if file_path:
        path_directory_var = file_path
        print(path_directory_var)
        path_directory.config(text=f"File Selected: {file_path}", fg="#4CAF50", wraplength=500)
    else:
        path_directory.config(text="No File Selected", fg="#F44336")
        path_directory_var = "No file"

root = tk.Tk()
root.title("MIDI To KeyFrames")
root.geometry("1100x700")

header_label = tk.Label(root, text="These are the default values", font=("Helvetica", 16, "bold"), fg="#4CAF50")
header_label.pack(pady=20)

input_frame = tk.Frame(root, bg="#E3F2FD", bd=2, relief="groove")
input_frame.pack(pady=20, padx=10, fill="x", side="top")

entries = []
labels = ["FPS", "Attack", "Decay", "Sustain", "Release"]
default_values = [30, 1.0, 1.0, 0.7, 1.0]
colors = ["#4CAF50", "#E57373", "#FFB74D", "#81C784", "#64B5F6"]

validate_cmd = root.register(validate_numeric_input)

for i in range(len(labels)):
    field_frame = tk.Frame(input_frame, bg="#E3F2FD")
    field_frame.pack(side="left", padx=15, pady=10)
    label = ttk.Label(field_frame, text=labels[i], foreground=colors[i], background="")
    label.pack()
    button_frame = tk.Frame(field_frame, bg="#E3F2FD")
    button_frame.pack(pady=5)
    decrement_button = tk.Button(button_frame, text="−", font=("Helvetica", 14, "bold"),
                                  command=lambda i=i: adjust_value(i, -0.1), width=3, height=1,
                                  bg="#757575", fg="white", relief="solid", borderwidth=2, highlightthickness=0)
    decrement_button.pack(side="left", padx=2)
    entry = ttk.Entry(button_frame, validate="key", validatecommand=(validate_cmd, '%P'), justify="center", width=8)
    entry.pack(side="left", padx=2, ipadx=5)
    entry.insert(0, f"{default_values[i]:.1f}")
    entry.bind("<KeyRelease>", lambda event: update_graph())
    entries.append(entry)
    increment_button = tk.Button(button_frame, text="+", font=("Helvetica", 14, "bold"),
                                  command=lambda i=i: adjust_value(i, 0.1), width=3, height=1,
                                  bg="#757575", fg="white", relief="solid", borderwidth=2, highlightthickness=0)
    increment_button.pack(side="left", padx=2)

top_frame = tk.Frame(root, bg="#FAFAFA")
top_frame.pack(pady=5, padx=10, fill="x")

bottom_frame = tk.Frame(root, bg="#FAFAFA")
bottom_frame.pack(pady=5, padx=10, fill="both", expand=True)

side_frame = tk.Frame(bottom_frame, bg="#E3F2FD", relief="ridge", bd=3)
side_frame.place(relwidth=0.5, relheight=0.5, relx=0.0)

bottom_bottom_frame = tk.Frame(bottom_frame, bg="#1a1a1a")
bottom_bottom_frame.place(relwidth=0.5, relheight=0.5, relx=0.0, rely=0.5)

left_box = tk.Frame(bottom_frame, bg="#E3F2FD", relief="ridge", bd=3)
left_box.place(relwidth=0.5, relx=0.0, relheight=0.5)

example_button = tk.Button(
    left_box,
    text="Select MIDI File",
    font=("Helvetica", 12, "bold"),
    bg="#64B5F6",
    fg="white",
    relief="raised",
    borderwidth=2,
    command=add_file
)
example_button.pack(pady=10, expand=True)

path_directory = tk.Label(
    left_box,
    text="No file selected.",
    font=("Helvetica", 10, "italic"),
    fg="#9E9E9E",
    wraplength=500,
    justify="center"
)
path_directory.pack(pady=5, expand=True)

new_button = tk.Button(
    bottom_bottom_frame,
    text="New Button",
    font=("Helvetica", 12, "bold"),
    bg="#FF7043",
    fg="white",
    relief="raised",
    borderwidth=2,
    command=make_csv
)
new_button.pack(pady=10, expand=True)

graph_frame = tk.Frame(bottom_frame, bg="#FAFAFA")
graph_frame.place(relwidth=0.5, relheight=1.0, relx=0.5)

fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)

update_graph()

root.mainloop()
