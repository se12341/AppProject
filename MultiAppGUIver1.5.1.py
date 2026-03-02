import sys
import subprocess
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os
from PIL import Image
import shutil
import hashlib
from collections import defaultdict
import threading
from concurrent.futures import ThreadPoolExecutor

def get_ffmpeg_path() -> str:
    """Return the ffmpeg executable path, whether frozen or running from source."""
    if getattr(sys, 'frozen', False):
        binaries_dir = os.path.join(sys._MEIPASS, 'imageio_ffmpeg', 'binaries')
        if os.path.isdir(binaries_dir):
            for f in os.listdir(binaries_dir):
                if f.startswith('ffmpeg') and f.endswith('.exe'):
                    return os.path.join(binaries_dir, f)
    # Fallback: use imageio_ffmpeg (works when running from source)
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return 'ffmpeg'


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
        app1_button.place(relx=0.5, rely=0.2, anchor="center")

        app2_button = ctk.CTkButton(self.nav_frame, text="Subfolder Empty", command=self.show_app2)
        app2_button.place(relx=0.5, rely=0.4, anchor="center")

        app3_button = ctk.CTkButton(self.nav_frame, text="Replace Names", command=self.show_app3)
        app3_button.place(relx=0.5, rely=0.6, anchor="center")

        app4_button = ctk.CTkButton(self.nav_frame, text="Duplicate Finder", command=self.show_app4)
        app4_button.place(relx=0.5, rely=0.8, anchor="center")
        
        
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

    def show_app4(self):
        # Clear the main frame and load App 4
        self.clear_main_frame()
        App4(self.main_frame).pack(fill="both", expand=True)

    def clear_main_frame(self):
        # Remove all widgets from the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Define App 1
class App1(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.progress_lock = threading.Lock()
        label = ctk.CTkLabel(self, text="Welcome to Web2Real!", font=("Arial", 25))
        label.place(y=-150, relx=0.5, rely=0.5, anchor="center")

        self.button = ctk.CTkButton(self, text="Replace Files", command=self.on_click1)
        self.button.place(y=-100, relx=0.5, rely=0.7, anchor="center")

        self.path_var = tk.StringVar()
        self.path = ctk.CTkEntry(self, width=350, height=40, textvariable=self.path_var)
        self.path.pack(side="bottom", expand=True, anchor="s", pady=75)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 11))
        self.status_label.pack(side="bottom", pady=(0, 5))

        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")

    def on_click1(self):
        self.progress.pack(side="top", pady=10)
        pathget = self.path.get()
        if not os.path.isdir(pathget):
            self.status_label.configure(text="Invalid path.")
            return
        self.button.configure(state="disabled")
        self.status_label.configure(text="Working...")
        thread = threading.Thread(target=self.process_conversion, args=(pathget,), daemon=True)
        thread.start()

    def process_conversion(self, pathget):
        self.convert_videos(pathget)
        self.convert_images(pathget)
        self.after(0, lambda: self.button.configure(state="normal", text="Done!"))
        self.after(0, lambda: self.status_label.configure(text="All files converted."))

    def convert_videos(self, pathget):
        files = [os.path.join(root, f) for root, _, fs in os.walk(pathget) for f in fs if f.lower().endswith(".webm")]
        if not files:
            return
        ffmpeg = get_ffmpeg_path()
        self.after(0, lambda: self.progress.configure(maximum=len(files), value=0))

        def convert_video_task(file_path):
            output_file = os.path.splitext(file_path)[0] + ".mp4"
            try:
                result = subprocess.run(
                    [ffmpeg, "-y", "-i", file_path, "-c:v", "libx264", "-c:a", "aac", output_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                )
                if result.returncode == 0:
                    os.remove(file_path)
                else:
                    err = result.stderr.decode(errors="replace").strip().splitlines()[-1] if result.stderr else "unknown error"
                    self.after(0, lambda e=err: self.status_label.configure(text=f"Error: {e}"))
            except Exception as e:
                self.after(0, lambda e=e: self.status_label.configure(text=f"Error: {e}"))
            with self.progress_lock:
                self.after(0, lambda: self.progress.step(1))

        with ThreadPoolExecutor(max_workers=4) as executor:
            list(executor.map(convert_video_task, files))

    def convert_images(self, pathget):
        files = [os.path.join(root, f) for root, _, fs in os.walk(pathget) for f in fs if f.lower().endswith(".webp")]
        if not files:
            return
        self.after(0, lambda: self.progress.configure(maximum=len(files), value=0))

        def convert_image_task(file_path):
            output_file = os.path.splitext(file_path)[0] + ".jpg"
            try:
                image = Image.open(file_path).convert("RGB")
                image.save(output_file, "JPEG")
                os.remove(file_path)
            except Exception as e:
                self.after(0, lambda e=e: self.status_label.configure(text=f"Error: {e}"))
            with self.progress_lock:
                self.after(0, lambda: self.progress.step(1))

        with ThreadPoolExecutor(max_workers=10) as executor:
            list(executor.map(convert_image_task, files))

# Define App 2
class App2(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.progress_lock = threading.Lock()
        label = ctk.CTkLabel(self, text="Welcome to Empty Folders!", font=("Arial", 25))
        label.place(y= -150, relx=0.5, rely=0.5, anchor="center")

        # Button for "Do Something" in App 1
        self.button = ctk.CTkButton(self, text="Take Out all files from a subfolders", command=self.on_click2)
        self.button.place(y= -100, relx=0.5, rely=0.7, anchor="center")
        
        # Path dir
        self.path_var = tk.StringVar()
        self.path = ctk.CTkEntry(self, width=350, height=40, textvariable=self.path_var)
        self.path.pack(side = "bottom", expand = True, anchor = "s", pady = 75)    

        # Progress bar (hidden by default)
        self.progress1 = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")

    def on_click2(self):
        # Show progress bar
        self.progress1.pack(side="top", pady=10)
        pathget = self.path.get()
        if not os.path.isdir(pathget):
            print("The specified path does not exist or is not a directory.")
            return
        # Run in background thread
        thread = threading.Thread(target=self.process_takedir, args=(pathget,), daemon=True)
        thread.start()

    def process_takedir(self, pathget):
        try:
            self.takedir(pathget)
        except Exception as e:
            print(f"Error: {e}")
        self.button.configure(text="Subfolders emptied and deleted")  # Update button2 text

    def takedir(self, parent_folder):
        # First pass: collect all files and count total items
        all_files = []
        all_dirs = []
        for root, dirs, files in os.walk(parent_folder):
            for name in files:
                all_files.append(os.path.join(root, name))
            for name in dirs:
                all_dirs.append(os.path.join(root, name))

        total_items = len(all_files) + len(all_dirs)
        self.progress1["maximum"] = total_items
        self.progress1["value"] = 0

        # Second pass: move files to root using thread pool
        def move_file_task(file_path):
            new_path = os.path.join(parent_folder, os.path.basename(file_path))
            if file_path != new_path:
                shutil.move(file_path, new_path)
            with self.progress_lock:
                self.progress1["value"] += 1
                self.update_idletasks()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            list(executor.map(move_file_task, all_files))

        # Third pass: delete empty directories
        for root, dirs, files in os.walk(parent_folder, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                except Exception:
                    pass
                with self.progress_lock:
                    self.progress1["value"] += 1
                    self.update_idletasks()

# Define App 3
class App3(ctk.CTkFrame): 
    def __init__(self, parent):
        super().__init__(parent)
        self.progress_lock = threading.Lock()
        label = ctk.CTkLabel(self, text="Welcome to Name Changer!", font=("Arial", 20))
        label.place(y= -150, relx=0.5, rely=0.5, anchor="center")

        # Button for "Do Something" in App 1
        self.button = ctk.CTkButton(self, text="Change File Names", command=self.on_click3)
        self.button.place(y= -100, relx=0.5, rely=0.7, anchor="center")

        # Path dir
        self.path_var1 = tk.StringVar()
        self.path1 = ctk.CTkEntry(self, width=350, height=40, textvariable=self.path_var1)
        self.path1.pack(side="bottom", pady=(0, 10))
        
        # Label indicating the lower entry
        change_label = ctk.CTkLabel(self, text="Files in the LOWER folder WILL change", font=("Arial", 12))
        change_label.pack(side="bottom", pady=(0, 10))

        self.path_var2 = tk.StringVar()
        self.path2 = ctk.CTkEntry(self, width=350, height=40, textvariable=self.path_var2)
        self.path2.pack(side="bottom", pady=(0, 10))

        # Progress bar (hidden by default)
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")

    def on_click3(self):
        # Show progress bar
        self.progress.pack(side="top", pady=10)
        pathget1 = self.path1.get()
        pathget2 = self.path2.get()
        if not os.path.isdir(pathget1) or not os.path.isdir(pathget2):
            print("The specified path does not exist or is not a directory.")
            return
        # Run in background thread
        thread = threading.Thread(target=self.process_rename, args=(pathget1, pathget2), daemon=True)
        thread.start()

    def process_rename(self, pathget1, pathget2):
        try:
            self.rename_duplicate_files(pathget1, pathget2)
        except Exception as e:
            print(f"Error: {e}")
        self.button.configure(text="Replacing File Names")  # Update button3 text

    def rename_duplicate_files(self, source_folder, target_folder):
        # Collect all files from source (including subfolders)
        source_files = []
        for root, _, files in os.walk(source_folder):
            for file in files:
                source_files.append(os.path.join(root, file))
        
        if not source_files:
            print("No files found in source folder.")
            return
        
        # Collect all target filenames (including subfolders)
        target_filenames = set()
        for root, _, files in os.walk(target_folder):
            for file in files:
                target_filenames.add(os.path.splitext(file)[0].lower())
        
        self.progress["maximum"] = len(source_files)
        self.progress["value"] = 0

        def rename_file_task(file_path):
            name, extension = os.path.splitext(os.path.basename(file_path))
            name_lower = name.lower()

            # Check if name exists in target
            if name_lower in target_filenames:
                counter = 1
                while True:
                    new_name = f"{name}_{counter}{extension}"
                    if os.path.splitext(new_name)[0].lower() not in target_filenames:
                        break
                    counter += 1
                
                new_filepath = os.path.join(os.path.dirname(file_path), new_name)
                try:
                    os.rename(file_path, new_filepath)
                    print(f"Renamed '{file_path}' to '{new_filepath}'.")
                except Exception as e:
                    print(f"Failed to rename '{file_path}': {e}")
            
            # Update progress outside the lock
            with self.progress_lock:
                self.progress["value"] += 1
            self.after(0, self.update_idletasks)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            list(executor.map(rename_file_task, source_files))

# Define App 4
class App4(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.progress_lock = threading.Lock()
        label = ctk.CTkLabel(self, text="Welcome to Duplicate Finder!", font=("Arial", 25))
        label.place(y=-150, relx=0.5, rely=0.5, anchor="center")

        # Button for DupliCheck
        self.button = ctk.CTkButton(self, text="Find & Delete Duplicates", command=self.on_click4)
        self.button.place(y=-100, relx=0.5, rely=0.7, anchor="center")

        # Path dir
        self.path_var = tk.StringVar()
        self.path = ctk.CTkEntry(self, width=350, height=40, textvariable=self.path_var)
        self.path.pack(side="bottom", expand=True, anchor="s", pady=75)

        # Progress bar (hidden by default)
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")

        # Status label (hidden by default)
        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12))

    def on_click4(self):
        # Show progress bar and status label
        self.progress.pack(side="top", pady=10)
        self.status_label.pack(side="top", pady=5)
        pathget = self.path.get()
        if not os.path.isdir(pathget):
            self.status_label.configure(text="Invalid path!")
            print("The specified path does not exist or is not a directory.")
            return
        # Run in background thread
        thread = threading.Thread(target=self.process_duplicates, args=(pathget,), daemon=True)
        thread.start()

    def process_duplicates(self, pathget):
        try:
            self.find_and_delete_duplicates(pathget)
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}")
            print(f"Error: {e}")
        self.button.configure(text="Duplicates Processed")

    def hash_file(self, path, chunk_size=65536):
        hasher = hashlib.sha256()
        try:
            with open(path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return None

    def find_and_delete_duplicates(self, directory):
        # Collect all files
        all_files = []
        for root, _, files in os.walk(directory):
            for name in files:
                path = os.path.join(root, name)
                all_files.append(path)

        self.progress["maximum"] = len(all_files)
        hashes = defaultdict(list)

        # Hash all files with progress tracking using thread pool
        def hash_file_task(file_path):
            file_hash = self.hash_file(file_path)
            if file_hash:
                hashes[file_hash].append(file_path)
            with self.progress_lock:
                current_progress = self.progress["value"] = self.progress["value"] + 1
                status_text = f"Processed {current_progress}/{len(all_files)} files"
                self.after(0, lambda: self.status_label.configure(text=status_text))
                self.after(0, self.update_idletasks)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            list(executor.map(hash_file_task, all_files))

        # Find duplicates and delete
        duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
        total_deleted = 0

        if not duplicates:
            self.status_label.configure(text="No duplicates found!")
            print("No duplicates found.")
            return

        print(f"\nDuplicate groups found: {len(duplicates)}")
        for file_list in duplicates.values():
            kept_file = file_list[0]
            print(f"Keeping: {kept_file}")
            for duplicate in file_list[1:]:
                try:
                    os.remove(duplicate)
                    print(f"Deleted: {duplicate}")
                    total_deleted += 1
                except Exception as e:
                    print(f"Failed to delete {duplicate}: {e}")

        self.status_label.configure(text=f"Deleted {total_deleted} duplicate files!")
        print(f"\nDeleted {total_deleted} duplicate files.")

# Run the application
if __name__ == "__main__":
    app = MultiAppGUI()
    app.mainloop()