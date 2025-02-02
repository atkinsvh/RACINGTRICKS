import tkinter as tk
from itertools import cycle
from PIL import Image, ImageTk
import time
import datetime

# Initialize Tkinter
root = tk.Tk()
root.title("Daytona Raceway Analysis")
root.geometry("400x400")  # Adjusted for Raspberry Pi screen
root.configure(bg="white")

# Font settings
FONT_TITLE = ("Lato", 10, "bold")
FONT_REGULAR = ("American Typewriter", 8)

# ===== TITLE BAR (Full Width) =====
title_label = tk.Label(root, text="Daytona Raceway Analysis", font=FONT_TITLE, bg="white")
title_label.grid(row=0, column=0, columnspan=3, pady=2, sticky="ew")

# ===== QUOTE BOARD (Left Fixed Column) =====
quote_frame = tk.Frame(root, width=70, height=240, bg="red")
quote_frame.grid(row=1, column=0, rowspan=3, sticky="ns", padx=2, pady=2)

quote_label = tk.Label(
    quote_frame, 
    text="Speed is life.", 
    font=FONT_TITLE, 
    fg="white", 
    bg="red", 
    wraplength=65, 
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

update_quote()

# ===== TIME CLOCK SECTION (Center) =====
time_clock_frame = tk.Frame(root, bg="white")
time_clock_frame.grid(row=1, column=1, pady=2, sticky="n")

car_info = tk.Label(time_clock_frame, text="Model: Ferrari 296 | MPG: 6.6", font=FONT_REGULAR, bg="white")
car_info.pack()

tires_label = tk.Label(time_clock_frame, text="TIRES: 38:00", font=FONT_REGULAR, bg="white")
tires_label.pack()

def tires_timer(time_left=2280):
    """Repeating 38-minute countdown timer labeled as 'TIRES'."""
    minutes = time_left // 60
    seconds = time_left % 60
    tires_label.config(text=f"TIRES: {minutes:02}:{seconds:02}")
    
    if time_left > 0:
        root.after(1000, lambda: tires_timer(time_left - 1))
    else:
        root.after(1000, lambda: tires_timer(2280))  # Restart after 38 minutes

tires_timer()  # Start countdown loop

# ===== RIGHT INFO PANEL (Above Track Map) =====
info_frame = tk.Frame(root, bg="white")
info_frame.grid(row=1, column=2, sticky="n", padx=5, pady=2)

miles_label = tk.Label(info_frame, text="Total Miles: 0", font=FONT_REGULAR, bg="white")
miles_label.pack()

time_elapsed_label = tk.Label(info_frame, text="Total Time: 00:00", font=FONT_REGULAR, bg="white")
time_elapsed_label.pack()

static_text_label = tk.Label(info_frame, text="1 Lap = 2.5 Miles", font=FONT_REGULAR, bg="white")
static_text_label.pack()

start_time = None  # Will be set when 8PM EST starts

def update_miles_and_time():
    """Calculates miles driven and time elapsed since 8PM EST."""
    global start_time
    current_time = datetime.datetime.now()
    est_now = current_time.astimezone(datetime.timezone(datetime.timedelta(hours=-5)))  # EST timezone

    if start_time is None and est_now.hour >= 20:
        start_time = time.time()  # Store the timestamp when counting starts

    if start_time:
        elapsed_seconds = int(time.time() - start_time)
        elapsed_hours = elapsed_seconds // 3600
        elapsed_minutes = (elapsed_seconds % 3600) // 60
        miles_covered = round((elapsed_seconds / 3600) * 40, 2)  # Using 40 mph standard speed

        miles_label.config(text=f"Total Miles: {miles_covered}")
        time_elapsed_label.config(text=f"Total Time: {elapsed_hours:02}:{elapsed_minutes:02}")

    root.after(1000, update_miles_and_time)  # Update every second

update_miles_and_time()  # Start counter

# ===== TRACK MAP WITH MOVING DOT =====
canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

# Load and resize the track map
track_image_path = "daytona-map_orig.png"
try:
    img = Image.open(track_image_path).resize((300, 300), Image.ANTIALIAS)
    track_img = ImageTk.PhotoImage(img)
    canvas.create_image(150, 150, image=track_img)
except Exception as e:
    print("Error loading image:", e)

# Approximate points tracing the Daytona International Speedway layout
track_points = [
    (50, 250), (70, 220), (90, 190), (110, 160), (130, 130),
    (150, 100), (170, 80), (190, 60), (210, 50), (230, 55),
    (250, 70), (260, 90), (270, 120), (275, 150), (270, 180),
    (260, 210), (240, 230), (220, 250), (200, 270), (180, 280),
    (150, 290), (120, 280), (90, 270), (70, 260), (50, 250)
]

dot = canvas.create_oval(48, 248, 52, 252, fill="yellow")
speed = 200  # Default speed

def move_dot(index=0):
    """Moves the dot along the track."""
    x, y = track_points[index]
    canvas.coords(dot, x-2, y-2, x+2, y+2)
    next_index = (index + 1) % len(track_points)
    root.after(speed, lambda: move_dot(next_index))

def set_standard_speed():
    """Set movement speed to standard."""
    global speed
    speed = 200  # Standard speed
    move_dot()

def set_challenge_speed():
    """Set movement speed to challenge mode (faster)."""
    global speed
    speed = 100  # Challenge speed
    move_dot()

# ===== SPEED CONTROL BUTTONS =====
button_frame = tk.Frame(root, bg="white")
button_frame.grid(row=4, column=1, columnspan=2, pady=2)

standard_btn = tk.Button(button_frame, text="Standard", command=set_standard_speed, font=FONT_REGULAR)
standard_btn.pack(side=tk.LEFT, padx=5)

challenge_btn = tk.Button(button_frame, text="Challenge", command=set_challenge_speed, font=FONT_REGULAR)
challenge_btn.pack(side=tk.RIGHT, padx=5)

# Start dot movement
move_dot()

# Start Tkinter loop
root.mainloop()
