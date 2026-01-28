import customtkinter as ctk

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
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Add navigation buttons
        app1_button = ctk.CTkButton(self.nav_frame, text="App 1", command=self.show_app1)
        app1_button.pack(pady=20, padx=20)

        app2_button = ctk.CTkButton(self.nav_frame, text="App 2", command=self.show_app2)
        app2_button.pack(pady=20, padx=20)

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
        label = ctk.CTkLabel(self, text="Welcome to App 1!", font=("Arial", 20))
        label.pack(pady=20)

        button = ctk.CTkButton(self, text="Do Something in App 1")
        button.pack(pady=10)

# Define App 2
class App2(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="Welcome to App 2!", font=("Arial", 20))
        label.pack(pady=20)

        button = ctk.CTkButton(self, text="Do Something in App 2")
        button.pack(pady=10)

# Run the application
if __name__ == "__main__":
    app = MultiAppGUI()
    app.mainloop()
