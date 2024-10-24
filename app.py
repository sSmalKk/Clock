import tkinter as tk
from datetime import datetime
import pytz
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("TIMEZONE_DB_API_KEY")

class FloatingClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Floating Clock")
        self.root.geometry("300x100")  # Window size
        self.root.overrideredirect(True)  # Remove window borders
        self.root.wm_attributes("-topmost", True)  # Keep the clock on top
        self.root.wm_attributes("-alpha", 0.5)  # Set initial translucency to 50%
        self.root.wm_attributes("-transparentcolor", "black")  # Make black background click-through

        # Label for displaying the time with a black background and no padding
        self.label = tk.Label(root, font=('Helvetica', 18), fg='white', bg='black', justify='center', bd=0, padx=0, pady=0)
        self.label.pack(fill='both', expand=True)  # Fill the entire frame with the label

        self.lisbon_time = self.fetch_time('Europe/Lisbon')  # Fetch Lisbon time once
        self.manhattan_time = self.fetch_time('America/New_York')  # Fetch Manhattan time once

        self.update_clock()  # Start updating the clock
        self.position_clock()  # Position the clock in the corner

        # Make the window draggable
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)

    def fetch_time(self, timezone):
        try:
            response = requests.get(f'https://api.timezonedb.com/v2.1/get-time-zone?key={API_KEY}&format=json&by=zone&zone={timezone}')
            if response.status_code == 200:
                data = response.json()
                return datetime.fromisoformat(data['formatted'])  # Adjust according to API response format
            else:
                print("Failed to fetch time:", response.status_code)
                return None
        except Exception as e:
            print("Error fetching time:", e)
            return None

    def update_clock(self):
        # Get current local time
        local_time = datetime.now().strftime('%H:%M:%S')

        # If the times were fetched successfully, format them to string
        lisbon_time_str = self.lisbon_time.strftime('%H:%M:%S') if self.lisbon_time else 'Error'
        manhattan_time_str = self.manhattan_time.strftime('%H:%M:%S') if self.manhattan_time else 'Error'

        # Update the label with times
        self.label.config(text=f'Local: {local_time}\nLisboa: {lisbon_time_str}\nManhattan: {manhattan_time_str}')
        self.root.after(1000, self.update_clock)  # Update the clock every second

    def position_clock(self):
        # Set the position of the clock in the bottom right corner
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"+{screen_width - 320}+{screen_height - 150}")  # Adjust position if needed

    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_move(self, event):
        x = self.root.winfo_pointerx() - self.x_offset
        y = self.root.winfo_pointery() - self.y_offset
        self.root.geometry(f'+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    clock = FloatingClock(root)
    root.mainloop()
