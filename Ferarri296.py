import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Daytona Racetrack Analysis")
root.geometry("900x600")
root.configure(bg="white")

# Set global font styles
FONT_TITLE = ("Lato", 16, "bold")
FONT_REGULAR = ("American Typewriter", 12)

# ===== QUOTE BOARD (Left Side) =====
quote_frame = tk.Frame(root, width=200, height=600, bg="red")
quote_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
quote_label = tk.Label(quote_frame, text="Quote Board", font=FONT_TITLE, fg="white", bg="red")
quote_label.pack(pady=10)

# ===== TRACK MAP (Right Side) =====
canvas = tk.Canvas(root, width=600, height=400, bg="white", highlightthickness=2)
canvas.pack(side=tk.RIGHT, padx=10, pady=10)

# Placeholder for the track outline (this will be updated with an actual image)
canvas.create_rectangle(50, 50, 550, 350, outline="black", width=2)
canvas.create_text(300, 200, text="Track Map Placeholder", font=FONT_REGULAR)

# ===== DATA TABLE (Center) =====
table_frame = tk.Frame(root, bg="white")
table_frame.pack(pady=10)

table_title = tk.Label(table_frame, text="Lap, Speed & Miles Data", font=FONT_TITLE, bg="white")
table_title.grid(row=0, column=1, columnspan=2)

# Table Headers
headers = ["", "Fixed Column", "Standard", "Challenge"]
for col, header in enumerate(headers):
    label = tk.Label(table_frame, text=header, font=FONT_REGULAR, bg="white", borderwidth=1, relief="solid", padx=5, pady=5)
    label.grid(row=1, column=col, sticky="nsew")

# Table Data
data = [
    ["Laps", 40, 38.4, 67.2],
    ["Speed (mph)", 40, 40, 70],
    ["Miles Driven", 96, 96, 168]
]

for row_idx, row in enumerate(data, start=2):
    for col_idx, value in enumerate(row):
        label = tk.Label(table_frame, text=value, font=FONT_REGULAR, bg="white", borderwidth=1, relief="solid", padx=5, pady=5)
        label.grid(row=row_idx, column=col_idx, sticky="nsew")

# ===== TIME CLOCK & CAR INFO (Bottom) =====
clock_frame = tk.Frame(root, bg="white")
clock_frame.pack(side=tk.BOTTOM, pady=10)

car_info = tk.Label(clock_frame, text="Model of Car: GT\nFuel Efficiency: 6.6 mi/gal\nTire Swap: 35-40 mins", font=FONT_REGULAR, bg="white")
car_info.pack()

# Start the Tkinter loop
root.mainloop()
