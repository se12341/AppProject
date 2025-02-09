import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os
from moviepy import VideoFileClip
from PIL import Image
import shutil

# Create the main application window
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"
class MultiAppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Multi-App GUI")
        self.geometry("800x600")

        # Create a navigation frame
        self.nav_frame = ctk.CTkFrame(self, width=200)
        self.nav_frame.pack(side="left", fill="y")

        # Create a main frame to display the selected app
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="top", fill="both", expand=True)

        # Add navigation buttons
        app1_button = ctk.CTkButton(self.nav_frame, text="Web Files to Real Files", command=self.show_app1)
        app1_button.place(relx=0.5, rely=0.22, anchor="center")

        app2_button = ctk.CTkButton(self.nav_frame, text="Subfolder Empty", command=self.show_app2)
        app2_button.place(relx=0.5, rely=0.5, anchor="center")

        app3_button = ctk.CTkButton(self.nav_frame, text="Replace Names", command=self.show_app3)
        app3_button.place(relx=0.5, rely=0.77, anchor="center")
        
        
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
    
    def show_app3(self):
        # Clear the main frame and load App 3
        self.clear_main_frame()
        App3(self.main_frame).pack(fill="both", expand=True)

    def clear_main_frame(self):
        # Remove all widgets from the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Define App 1
class App1(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Welcome to Web2Real!", font=("Arial", 25))
        label.place(y= -150, relx=0.5, rely=0.5, anchor="center")

        # Button for "Do Something" in App 1
        self.button = ctk.CTkButton(self, text="Replace Files", command=self.on_click1)
        self.button.place(y= -100, relx=0.5, rely=0.7, anchor="center")

        # Path dir
        global path
        path_var = tk.StringVar()
        path = ctk.CTkEntry(self, width=350, height=40, textvariable=path_var)
        path.pack(side="bottom", expand=True, anchor = "s", pady = 75)

        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(side="top", pady=10)

    def on_click1(self):
        pathget = path.get()
        self.convert_videos(pathget)
        self.convert_images(pathget)
#Define what app1 does
    def convert_videos(self, pathget):
        files = [os.path.join(root, file) for root, _, files in os.walk(pathget) for file in files if file.endswith(".webm")]
        self.progress["maximum"] = len(files)
        for i, file_path in enumerate(files):
            output_file = os.path.splitext(file_path)[0] + ".mp4"
            print(f"Converting {file_path} to {output_file}")
            video = VideoFileClip(file_path)
            video.write_videofile(output_file, codec="libx264")
            video.close()
            os.remove(file_path)  # Optional: remove the original .webm file
            self.progress["value"] = i + 1
            self.update_idletasks()
    def convert_images(self, pathget):
        files = [os.path.join(root, file) for root, _, files in os.walk(pathget) for file in files if file.endswith(".webp")]
        self.progress["maximum"] = len(files)
        for i, file_path in enumerate(files):
            output_file = os.path.splitext(file_path)[0] + ".jpg"
            print(f"Converting {file_path} to {output_file}")
            image = Image.open(file_path).convert("RGB")
            image.save(output_file, "JPEG")
            os.remove(file_path)  # Optional: remove the original .webp file
            self.progress["value"] = i + 1
            self.update_idletasks()

# Define App 2
class App2(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Welcome to Empty Folders!", font=("Arial", 25))
        label.place(y= -150, relx=0.5, rely=0.5, anchor="center")

        # Button for "Do Something" in App 1
        self.button = ctk.CTkButton(self, text="Take Out all files from a subfolders", command=self.on_click2)
        self.button.place(y= -100, relx=0.5, rely=0.7, anchor="center")
        
        # Path dir
        global path
        path_var = tk.StringVar()
        path = ctk.CTkEntry(self, width=350, height=40, textvariable=path_var)
        path.pack(side = "bottom", expand = True, anchor = "s", pady = 75)    

        # Progress bar
        self.progress1 = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress1.pack(side="top", pady=10)        

    def on_click2(self):
        try:
            pathget = path.get()
            self.takedir(pathget)
        except:
            if not os.path.isdir(pathget):
                print("The specified path does not exist or is not a directory.")
        self.button.configure(text="Subfolders emptied and deleted")  # Update button2 text

    def takedir(self, parent_folder):
        files = [os.path.join(root, file) for root, _, files in os.walk(parent_folder) for file in files]
        self.progress1["maximum"] = len(files)
        for i, file_path in enumerate(files):
            new_path = os.path.join(parent_folder, os.path.basename(file_path))
            if file_path != new_path:
                shutil.move(file_path, new_path)
            self.progress1["value"] = i + 1
            self.update_idletasks()

        for root, dirs, files in os.walk(parent_folder, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                self.progress1["value"] += 1
                self.update_idletasks()

# Define App 3
class App3(ctk.CTkFrame): 
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Welcome to Name Changer!", font=("Arial", 20))
        label.place(y= -150, relx=0.5, rely=0.5, anchor="center")

        # Button for "Do Something" in App 1
        self.button = ctk.CTkButton(self, text="Change File Names", command=self.on_click3)
        self.button.place(y= -100, relx=0.5, rely=0.7, anchor="center")

        # Path dir
        global path1
        path_var1 = tk.StringVar()
        path1 = ctk.CTkEntry(self, width=350, height=40, textvariable=path_var1)
        path1.pack(side="bottom", pady=(0, 10))
        
        # Label indicating the lower entry
        change_label = ctk.CTkLabel(self, text="Files in the LOWER folder WILL change", font=("Arial", 12))
        change_label.pack(side="bottom", pady=(0, 10))

        global path2
        path_var2 = tk.StringVar()
        path2 = ctk.CTkEntry(self, width=350, height=40, textvariable=path_var2)
        path2.pack(side="bottom", pady=(0, 10))

        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(side="top", pady=10)

    def on_click3(self):
        try:
            pathget1 = path1.get()
            pathget2 = path2.get()
            self.rename_duplicate_files(pathget1, pathget2)
        except Exception as e:
            print(f"Error: {e}")
            if not os.path.isdir(pathget1) or not os.path.isdir(pathget2):
                print("The specified path does not exist or is not a directory.")
        self.button.configure(text="Replacing File Names")  # Update button3 text

    def rename_duplicate_files(self, source_folder, target_folder):
        files = [os.path.join(source_folder, file) for file in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, file))]
        self.progress["maximum"] = len(files)
        target_filenames = {os.path.splitext(file)[0].lower(): file for file in os.listdir(target_folder) if os.path.isfile(os.path.join(target_folder, file))}

        for i, file_path in enumerate(files):
            name, extension = os.path.splitext(os.path.basename(file_path))
            name_lower = name.lower()

            if name_lower in target_filenames:
                new_filename = generate_unique_filename(name, extension, target_filenames.keys())
                new_filepath = os.path.join(source_folder, new_filename)
                os.rename(file_path, new_filepath)
                print(f"Renamed '{file_path}' to '{new_filepath}'.")
                target_filenames[name_lower] = new_filename

            self.progress["value"] = i + 1
            self.update_idletasks()

def generate_unique_filename(base_name, extension, existing_names):
    count = 1
    new_name = f"{base_name}_{count}{extension}"
    while new_name.lower() in existing_names:
        count += 1
        new_name = f"{base_name}_{count}{extension}"
    return new_name

# Run the application
if __name__ == "__main__":
    app = MultiAppGUI()
    app.mainloop()
