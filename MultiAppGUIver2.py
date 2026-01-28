import tkinter as tk
import customtkinter as ctk
import os
from moviepy import VideoFileClip
from PIL import Image
import shutil
import time
from threading import Thread

# Create the main application window
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"
class MultiAppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Multi-App GUI")
        self.geometry("600x400")
        
        # Create a navigation frame
        self.nav_frame = ctk.CTkFrame(self, width=200)
        self.nav_frame.pack(side="left", fill="y")

        # Create a main frame to display the selected app
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="top", fill="both", expand=True)

        # Path dir
        global path
        path_var = tk.StringVar()
        path = ctk.CTkEntry(self, width=350, height=40, textvariable=path_var)
        path.pack(side="bottom", expand=True)

        # Add navigation buttons
        #app1
        app1_button = ctk.CTkButton(self.nav_frame, text="Web Files to Real Files", command=self.show_app1)
        app1_button.place(relx=0.5, rely=0.4, anchor="center")
        
        #app2
        app2_button = ctk.CTkButton(self.nav_frame, text="Subfolder Empty", command=self.show_app2)
        app2_button.place(relx=0.5, rely=0.6, anchor="center")

        # Create a label for progbar
        progbar = ctk.CTkLabel(self, text="Click 'Start' to begin loading", font=("Arial", 16), )
        progbar.pack(pady=20)
        
        # Create a progress bar
        progress_bar = ctk.CTkProgressBar(self, width=300)
        progress_bar.set(0)  # Set initial progress to 0
        progress_bar.pack(pady=20)

        # Function to update the progress bar
        def update_progress():
            for i in range(101):  # Progress from 0 to 100
                time.sleep(0.05)  # Simulate work being done
                progress_bar.set(i / 100)  # Update the progress bar value
            progbar.configure(text="Loading Complete!")  # Update progbar when done

        # Initialize with the first app
        self.show_app1()

    def show_app1(self):
        # Clear the main frame and load App 1
        self.clear_main_frame()
        App1(self.main_frame).pack(fill="both", expand=True)

    def show_app2(self):
        # Clear the main frame and load App 2
        self.clear_main_frame()
        App2(self.main_frame).pack(fill="both", expand=True)

    def clear_main_frame(self):
        # Remove all widgets from the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Define App 1
class App1(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Welcome to Web2Real!", font=("Arial", 20))
        label.place(relx=0.5, rely=0.5, anchor="center")

        # Button for "Do Something" in App 1
        self.button = ctk.CTkButton(self, text="Replace Files", command=self.on_click1)
        self.button.place(relx=0.5, rely=0.7, anchor="center")

    def on_click1(self):
        try:
            pathget = path.get()
            convert_videos(pathget)
            convert_images(pathget)
            self.button.configure("Task done files changed!")
        except:
            self.button.configure("No files found")

# Define what app1 does
def convert_videos(pathget):
        for root, dirs, files in os.walk(pathget):
            for file in files:
                file_path = os.path.join(root, file)
                # Convert .webm to .mp4
                if file.endswith(".webm"):
                    output_file = os.path.splitext(file_path)[0] + ".mp4"
                    print(f"Converting {file_path} to {output_file}")
                    video = VideoFileClip(file_path)
                    video.write_videofile(output_file, codec="libx264")
                    video.close()
                    os.remove(file_path)  # Optional: remove the original .webm file
def convert_images(pathget):
        for root, dirs, files in os.walk(pathget):
            for file in files:
                file_path = os.path.join(root, file)
                # Convert .webp to .jpg
                if file.endswith(".webp"):
                    output_file = os.path.splitext(file_path)[0] + ".jpg"
                    print(f"Converting {file_path} to {output_file}")
                    image = Image.open(file_path).convert("RGB")
                    image.save(output_file, "JPEG")
                    os.remove(file_path)  # Optional: remove the original .webp file

# Define App 2
class App2(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Welcome to Empty Folders!", font=("Arial", 20))
        label.place(relx=0.5, rely=0.5, anchor="center")

        # Button for "Do Something" in App 2
        self.button = ctk.CTkButton(self, text="Take Out all files from a subfolders", command=self.on_click2)
        self.button.place(relx=0.5, rely=0.7, anchor="center")

    def on_click2(self):
        try:
            pathget = path.get()
            takedir(pathget)
        except:
            if not os.path.isdir(pathget):
                print("The specified path does not exist or is not a directory.")
        self.button.configure(text="Subfolders emptied and deleted")  # Update button2 text
# Define what app2 does
def takedir(parent_folder):
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            file_path = os.path.join(root, file)
            new_path = os.path.join(parent_folder, file)
            if file_path != new_path:
                shutil.move(file_path, new_path)

            # Optionally, remove empty directories
    for root, dirs, files in os.walk(parent_folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

# Run the application
if __name__ == "__main__":
    app = MultiAppGUI()
    app.mainloop()
