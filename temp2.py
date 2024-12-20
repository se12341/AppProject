import customtkinter as ctk
import time
from threading import Thread

# Initialize the main application window
app = ctk.CTk()
app.geometry("400x300")
app.title("Loading Bar Example")

# Create a label
label = ctk.CTkLabel(app, text="Click 'Start' to begin loading", font=("Arial", 16))
label.pack(pady=20)

# Create a progress bar
progress_bar = ctk.CTkProgressBar(app, width=300)
progress_bar.set(0)  # Set initial progress to 0
progress_bar.pack(pady=20)

# Function to update the progress bar
def update_progress():
    for i in range(101):  # Progress from 0 to 100
        time.sleep(0.05)  # Simulate work being done
        progress_bar.set(i / 100)  # Update the progress bar value
    label.configure(text="Loading Complete!")  # Update label when done

# Start the loading process in a separate thread
