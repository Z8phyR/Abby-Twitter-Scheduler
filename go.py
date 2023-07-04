import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

# Function to handle tweet submission


def submit_tweet():
    tweet = tweet_text.get("1.0", "end-1c")
    date = date_entry.get_date()
    hour = hour_var.get()

    if date == datetime.today().date():
        scheduled_date = None
    else:
        scheduled_date = datetime.combine(date, datetime.strptime(
            hour, "%H").time()).strftime("%Y-%m-%d %H:%M")

    # Call your schedule_tweet function here with tweet and scheduled_date parameters
    # Replace the print statement below with your actual success/failure confirmation

    print("Tweet scheduled successfully.")


# Create GUI window
window = tk.Tk()
window.title("Tweeter")

# Tweet Text Entry
tweet_label = tk.Label(window, text="Tweet:")
tweet_label.pack()
tweet_text = tk.Text(window, height=5, width=40)
tweet_text.pack()

# Date Entry
date_label = tk.Label(window, text="Date:")
date_label.pack()
date_entry = DateEntry(window, date_pattern="yyyy-mm-dd",
                       background="white", foreground="black")
date_entry.pack()
date_entry.set_date(datetime.today().date())

# Hour Selection Dropdown
hour_label = tk.Label(window, text="Hour:")
hour_label.pack()
hours = [str(i).zfill(2) for i in range(24)]  # Generate hours from 00 to 23
hour_var = tk.StringVar()
hour_dropdown = tk.OptionMenu(window, hour_var, *hours)
hour_dropdown.pack()
hour_var.set(datetime.now().strftime("%H"))

# Submit Button
submit_button = tk.Button(window, text="Submit", command=submit_tweet)
submit_button.pack()

# Run the GUI event loop
window.mainloop()
