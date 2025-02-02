import tkinter as tk
from itertools import cycle
from PIL import Image, ImageTk

# Initialize Tkinter
root = tk.Tk()
root.title("Daytona Raceway Analysis")
root.geometry("320x240")
root.configure(bg="white")

# Fonts
FONT_TITLE = ("Lato", 10, "bold")
FONT_REGULAR = ("American Typewriter", 8)

# ===== QUOTE BOARD =====
quote_frame = tk.Frame(root, width=90, height=240, bg="red")
quote_frame.pack(side=tk.LEFT, fill=tk.Y, padx=2, pady=2)

quote_label = tk.Label(
    quote_frame, 
    text="Quote Board", 
    font=FONT_TITLE, 
    fg="white", 
    bg="red", 
    wraplength=85, 
    justify="left"
)
quote_label.pack(pady=5)

# Cycling quotes (every 5 minutes)
quotes = cycle([
    "Speed is life.", "Fast is fun!", "Smooth is fast.", "Grip it and rip it!",
    "Racing is the art of control.", "Throttle solves everything.", "The line is everything.",
    "Brake late, win big.", "Flat out or nothing.", "Corners separate the pros.",
    "Go fast, don’t crash.", "Racing is a state of mind.", "Winning starts in the head.",
    "Momentum wins races.", "No lift, no limits.", "Drive fast, take chances.",
    "Every lap is a lesson.", "The car follows your mind.", "Slow is smooth, smooth is fast.",
    "Tires win races.", "The best driver adapts.", "Full throttle fixes all.",
    "Push until you find the edge.", "Fuel, tires, and courage.", "Every lap is a new challenge."
])

def update_quote():
    """Update quote every 5 minutes."""
    quote_label.config(text=next(quotes))
    root.after(300000, update_quote)  # 5 minutes

update_quote()  # Start the quote cycle

# ===== TRACK MAP =====
canvas = tk.Canvas(root, width=140, height=120, bg="white")
canvas.pack(side=tk.RIGHT, padx=5, pady=5)

# Load and resize the track map
track_image_path = "/mnt/data/daytona-map_orig.png"
try:
    img = Image.open(track_image_path).resize((140, 120), Image.ANTIALIAS)
    track_img = ImageTk.PhotoImage(img)
    canvas.create_image(70, 60, image=track_img)
except Exception as e:
    print("Error loading image:", e)

# ===== TRACE DOT FUNCTION =====
# Counterclockwise movement path (approximated)
track_points = [
    (20, 100), (30, 80), (40, 60), (50, 40), (60, 30), (80, 20),  # Up through Turns 1-3
    (100, 25), (110, 40), (115, 60), (118, 80), (120, 100),       # Back around top
    (115, 120), (100, 130), (80, 135), (60, 140), (40, 130),      # Down right side
    (30, 110), (25, 90)  # Completing the lap
]

dot = canvas.create_oval(18, 98, 22, 102, fill="yellow")  # Start at Turn 1

def move_dot(index=0):
    """Moves the dot counterclockwise along the track."""
    x, y = track_points[index]
    canvas.coords(dot, x-2, y-2, x+2, y+2)  # Update dot position
    next_index = (index + 1) % len(track_points)  # Loop back after last point
    root.after(200, lambda: move_dot(next_index))  # Move every 200ms

move_dot()  # Start animation

# ===== TABLE =====
table_frame = tk.Frame(root, bg="white")
table_frame.pack(pady=5)

headers = ["", "Fixed Column", "Standard", "Challenge"]
data = [
    ["Laps", 40, 38.4, 67.2],
    ["Speed (mph)", 40, 40, 70],
    ["Miles Driven", 96, 96, 168]
]

for row_idx, row in enumerate([headers] + data):
    for col_idx, value in enumerate(row):
        lbl = tk.Label(
            table_frame, 
            text=value, 
            font=FONT_REGULAR, 
            bg="white", 
            padx=2, 
            pady=2, 
            borderwidth=1, 
            relief="solid"
        )
        lbl.grid(row=row_idx, column=col_idx, sticky="nsew")

# Start Tkinter
root.mainloop()
