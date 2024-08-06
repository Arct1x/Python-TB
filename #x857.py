# Hi there, dont expect this to work please I have had trouble with it for very long :( 



import tkinter as tk
from tkinter import font, messagebox
import time
import pyautogui
from pynput.keyboard import Controller
from PIL import Image
import math

# Window
root = tk.Tk()
root.title("TR1GG3R B0T")
root.geometry("300x500")
root.configure(bg="darkblue", relief="sunken")
default_font = font.nametofont("TkDefaultFont")
root.resizable(False, False)

# Labels
Title = tk.Label(root, text="Trigger Bot Alpha", bg="darkblue", fg="white", font=(default_font, 14))
WKill = tk.Label(root, text="Press P to kill this application quickly", fg="red", bg="darkblue", anchor="w", justify="left")
SelColLabel = tk.Label(root, text="Select Color", fg="white", bg="darkblue", anchor="w", justify="left")
SelTTLabel = tk.Label(root, text="Choose a weapon below, it determines recoil control.", fg="white", bg="darkblue", anchor="w", justify="left", wraplength=300)
SelDeLabel = tk.Label(root, text="Type in a delay before firing in ms.", fg="white", bg="darkblue", anchor='w', justify='left')
SelFPLabel = tk.Label(root, text="Insert FOV around cursor to detect color:", fg="white", bg="darkblue", anchor='w', justify='left')

# Functions

def validate_numeric_input(new_value):
    if new_value.isdigit() or new_value == "":
        return True
    else:
        messagebox.showerror("Invalid Input", "Please enter only numeric values.")
        return False

vcmd = (root.register(validate_numeric_input), '%P')

def kill(event=None):
    root.destroy()

def wraplength(event):
    SelTTLabel.config(wraplength=SelTTLabel.winfo_width())

def ApplySettings():
    TaptimeValue = TapTimeVar.get()
    SelectedColValue = ColorSelectInt.get()
    DelayTimeValue = DelayTimeVar.get()
    FOVPixelValue = FOVPixelVar.get()
    
    if not DelayTimeValue or not FOVPixelValue:
        print("There are no values that can be read in one of the Entrys, reinput them and try again.")
    elif not DelayTimeValue.isdigit() or not FOVPixelValue.isdigit():
        print("Please enter only numeric values for Delay and FOV.")
    else:
        global FOVPixelVal, DelayTimeVal, SelectedColVal, TaptimeVal
        FOVPixelVal = int(FOVPixelValue)
        DelayTimeVal = int(DelayTimeValue)
        SelectedColVal = ColorVals.get(SelectedColValue, (0, 0, 0))
        TaptimeVal = option_values.get(TaptimeValue, "Unknown")
        print("ok", SelectedColVal, TaptimeVal, DelayTimeVal, FOVPixelVal)

# Color selection

ColorSelectInt = tk.IntVar()

RedRAD = tk.Radiobutton(root, text="Red", bg="red", fg="black", variable=ColorSelectInt, value=1)
PurRAD = tk.Radiobutton(root, text="Purple", bg="purple", fg="black", variable=ColorSelectInt, value=2)
YelRAD = tk.Radiobutton(root, text="Yellow", bg="yellow", fg="black", variable=ColorSelectInt, value=3)

ColorVals = {
    1: (255, 0, 0),       # Red
    2: (161, 69, 163),    # Purple
    3: (254, 254, 64)     # Yellow
}

# Taptime drop down.

TapTimeVar = tk.StringVar()

options = [
    "Vandal (~150ms)",
    "Guardian (???)",
    "Sheriff (250ms)",
    "Fast (<50ms)"
]

option_values = {
    "Vandal (~150ms)": 150,
    "Guardian (???)": 200,
    "Sheriff (250ms)": 250,
    "Fast (<50ms)": 50
}

TapTimeVar.set(options[0])
TaptimeMenu = tk.OptionMenu(root, TapTimeVar, *options)

# Delay

DelayTimeVar = tk.StringVar()

DelayTimeEntry = tk.Entry(root, textvariable=DelayTimeVar, validate="key", validatecommand=vcmd)

# FOV in Pixels

FOVPixelVar = tk.StringVar()

FOVPixelEntry = tk.Entry(root, textvariable=FOVPixelVar, validate="key", validatecommand=vcmd)

# Apply Settings Button.

ApplyConfig = tk.Button(root, text="Apply Current Settings.", command=ApplySettings)

# Packing

Title.pack(pady=2)
WKill.pack(fill="x", pady=2)
SelColLabel.pack(fill="x", pady=2)
RedRAD.pack(pady=2)
PurRAD.pack(pady=2)
YelRAD.pack(pady=2)
SelTTLabel.pack(fill="x", pady=2)
TaptimeMenu.pack(pady=2)
SelDeLabel.pack(fill="x", pady=2)
DelayTimeEntry.pack(pady=2)
SelFPLabel.pack(fill='x', pady=2)
FOVPixelEntry.pack(pady=2)
ApplyConfig.pack(pady=30)

# Binding

root.bind("<p>", kill)
SelTTLabel.bind("<Configure>", wraplength)

# Mainloop for root
root.mainloop()

# Main functionality

def GetColor(radius):
    x, y = pyautogui.position()
    Left = x - radius
    Right = x + radius
    Top = y - radius
    Bottom = y + radius
    
    Screenshot = pyautogui.screenshot(region=(Left, Top, Right - Left, Bottom - Top))
    image = Image.frombytes('RGB', Screenshot.size, Screenshot.tobytes())

    return image

def CheckWithinCircle(x, y, center_x, center_y, radius):
    return math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2) <= radius

def get_colors_within_fov(image, radius):
    width, height = image.size
    center_x, center_y = width // 2, height // 2
    pixels = image.load()

    colors = []

    for x in range(width):
        for y in range(height):
            if CheckWithinCircle(x, y, center_x, center_y, radius):
                colors.append(pixels[x, y])

    return colors

def is_color_within_tolerance(pixel, target_color, tolerance=25):
    return all(abs(pixel[i] - target_color[i]) <= tolerance for i in range(3))

def compare_colors_to_targets(colors, target_color, tolerance=25):
    for color in colors:
        if is_color_within_tolerance(color, target_color, tolerance):
            print(f"Detected target color: {target_color}")
            return True
    return False

# Main loop for detection
keyboard = Controller()

while True:
    if 'FOVPixelVal' in globals() and 'DelayTimeVal' in globals() and 'SelectedColVal' in globals() and 'TaptimeVal' in globals():
        region_image = GetColor(FOVPixelVal)
        colors_within_fov = get_colors_within_fov(region_image, FOVPixelVal)

        if compare_colors_to_targets(colors_within_fov, SelectedColVal):
            time.sleep(DelayTimeVal / 1000)  # Delay before starting the action
            while compare_colors_to_targets(colors_within_fov, SelectedColVal):
                keyboard.write('l')  # Simulate pressing 'l'
                print("Holyyy shit it works!!")
                time.sleep(TaptimeVal / 1000)  # Repeat action based on tap time
                region_image = GetColor(FOVPixelVal)
                colors_within_fov = get_colors_within_fov(region_image, FOVPixelVal)
    time.sleep(0.1)  # Add a small delay to avoid high CPU usage
