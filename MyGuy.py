import tkinter as tk
from itertools import cycle
from PIL import Image, ImageTk
import time
import datetime

# Initialize Tkinter
root = tk.Tk()
root.title("Daytona Raceway Analysis")
root.geometry("320x240")  # Optimized for Raspberry Pi screen
root.configure(bg="white")

# Font settings
FONT_TITLE = ("Lato", 10, "bold")
FONT_REGULAR = ("American Typewriter", 8)

# ===== TITLE BAR (Full Width) =====
title_label = tk.Label(root, text="Daytona Raceway Analysis", font=FONT_TITLE, bg="white")
title_label.grid(row=0, column=0, columnspan=3, pady=2, sticky="ew")

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

# ===== TRACK MAP (Bottom Right) =====
canvas = tk.Canvas(root, width=120, height=100, bg="white")
canvas.grid(row=2, column=2, rowspan=2, padx=5, pady=5)

# Load and resize the track map
track_image_path = "/mnt/data/daytona-map_orig.png"
try:
    img = Image.open(track_image_path).resize((120, 100), Image.ANTIALIAS)
    track_img = ImageTk.PhotoImage(img)
    canvas.create_image(60, 50, image=track_img)
except Exception as e:
    print("Error loading image:", e)

# ===== TRACK DOT MOVEMENT =====
track_points = [
    (30, 80), (35, 65), (40, 50), (50, 35), (65, 25), (80, 20),
    (100, 25), (110, 40), (115, 60), (118, 80), (120, 100),
    (110, 115), (90, 125), (70, 130), (50, 125), (35, 110), (30, 95)
]

dot = canvas.create_oval(28, 78, 32, 82, fill="yellow")
speed = 200  # Default to Standard Speed (in milliseconds)

def move_dot(index=0):
    """Moves the dot along the track based on selected speed."""
    x, y = track_points[index]
    canvas.coords(dot, x-2, y-2, x+2, y+2)
    next_index = (index + 1) % len(track_points)
    root.after(speed, lambda: move_dot(next_index))

def set_standard_speed():
    """Sets speed to standard (slower)."""
    global speed
    speed = 200  # Standard speed
    move_dot()

def set_challenge_speed():
    """Sets speed to challenge (faster)."""
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

# Start Tkinter
root.mainloop()
