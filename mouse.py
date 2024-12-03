import time
from pynput.mouse import Listener, Button
import tkinter as tk
from threading import Thread

# Global variables for tracking mouse events
left_click_count = 0
right_click_count = 0
double_left_click_count = 0
last_left_click_time = 0
click_start_time = None
last_click_duration = 0
movement_count = 0  # Tracks the number of mouse movements

# Callback function for mouse clicks
def on_click(x, y, button, pressed):
    global left_click_count, right_click_count, double_left_click_count, last_left_click_time, click_start_time, last_click_duration

    if pressed:  # Handle mouse button press
        click_start_time = time.time()  # Record the start time
    else:  # Handle mouse button release
        if click_start_time is not None:
            click_duration = time.time() - click_start_time  # Calculate click duration
            last_click_duration = click_duration  # Store the duration of the last click
            click_start_time = None  # Reset the start time

            # Check the type of click
            if button == Button.left:
                current_time = time.time()
                if current_time - last_left_click_time <= 0.3:  # Check for double click (within 300ms)
                    double_left_click_count += 1
                    left_click_count -= 1  # Adjust for single clicks
                else:
                    left_click_count += 1
                last_left_click_time = current_time
            elif button == Button.right:
                right_click_count += 1

            # Update the UI
            update_ui()

# Callback function for mouse movements
def on_move(x, y):
    global movement_count
    movement_count += 1  # Increment the movement count for every mouse movement
    # Update the UI
    update_ui()

# Function to update the UI with the latest statistics
def update_ui():
    left_click_label.config(text=f"Total Left Clicks: {left_click_count}")
    right_click_label.config(text=f"Total Right Clicks: {right_click_count}")
    double_left_click_label.config(text=f"Double Left Clicks: {double_left_click_count}")
    click_duration_label.config(text=f"Last Click Duration: {last_click_duration:.2f} seconds")
    movement_count_label.config(text=f"Total Mouse Movements: {movement_count}")

# Function to continuously monitor mouse events in a separate thread
def monitor_mouse():
    with Listener(on_click=on_click, on_move=on_move) as listener:
        listener.join()  # Keep the listener running

# Function to start the mouse listener in a background thread
def start_listener():
    listener_thread = Thread(target=monitor_mouse)
    listener_thread.daemon = True  # Allows the thread to exit when the main program exits
    listener_thread.start()

# Setting up the Tkinter UI
root = tk.Tk()
root.title("Mouse Activity Tracker")

# Create labels for displaying the statistics
left_click_label = tk.Label(root, text="Total Left Clicks: 0", font=("Arial", 14))
left_click_label.pack()

right_click_label = tk.Label(root, text="Total Right Clicks: 0", font=("Arial", 14))
right_click_label.pack()

double_left_click_label = tk.Label(root, text="Double Left Clicks: 0", font=("Arial", 14))
double_left_click_label.pack()

click_duration_label = tk.Label(root, text="Last Click Duration: 0.00 seconds", font=("Arial", 14))
click_duration_label.pack()

movement_count_label = tk.Label(root, text="Total Mouse Movements: 0", font=("Arial", 14))
movement_count_label.pack()

# Start the mouse event listener
start_listener()

# Run the Tkinter event loop
root.mainloop()
