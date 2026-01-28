import tkinter as tk
import customtkinter as ctk
import os
from moviepy import *
from PIL import Image

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

def startpreform():
    try:
        pathget = path.get()
        convert_images(pathget)
        convert_videos(pathget)
    except:
        print("nothing to see here!")
    finishlabel.configure(text="Finished Task!")

# Root theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create the main window
root = ctk.CTk()
root.geometry("500x200")
root.title("Web Files to Real Files")

# UI elements
title = ctk.CTkLabel(root, text="Path")
title.pack()

# Path dir
path_var = tk.StringVar()
path = ctk.CTkEntry(root, width=350, height=40, textvariable=path_var)
path.pack()

# Start button
preform = ctk.CTkButton(root, text="Preform Task!", command=startpreform)
preform.pack(padx=20, pady=20)

# Finished preforming task
finishlabel = ctk.CTkLabel(root, text="")
finishlabel.pack(padx=10, pady=10)


# Start the main event loop
root.mainloop()


#C:\Users\naor\Downloads