import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize the main window
root = tk.Tk()
root.title("Air Quality Monitoring and Analysis")
root.geometry("800x600")
root.configure(bg="#f0f0f0")  # Light gray background

# Title Label
title_label = tk.Label(root, text="Air Quality Monitoring and Analysis", font=("Arial", 24), bg="#f0f0f0")
title_label.pack(pady=20)

# Function to load data
def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            global data
            data = pd.read_csv(file_path)
            messagebox.showinfo("Success", "Data loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

# Function to show data summary
def show_data_summary():
    if 'data' in globals():
        summary_window = tk.Toplevel(root)
        summary_window.title("Data Summary")
        
        # Calculate summary statistics
        summary_text = tk.Text(summary_window, height=15, width=80)
        summary_text.insert(tk.END, str(data.describe()))
        summary_text.pack()
    else:
        messagebox.showwarning("Warning", "No data loaded yet!")

# Function to plot PM2.5 trends
def plot_trends():
    if 'data' in globals():
        plt.figure(figsize=(10, 6))
        plt.plot(data['Date'], data['PM2.5'], label="PM2.5", color='blue', marker='o')
        plt.xlabel("Date")
        plt.ylabel("PM2.5 Levels")
        plt.title("PM2.5 Trends Over Time", fontsize=16)
        plt.legend()
        plt.grid()
        plt.show()
    else:
        messagebox.showwarning("Warning", "No data loaded yet!")

# Function to plot region comparison
def plot_region_comparison():
    if 'data' in globals():
        region_avg = data.groupby('Region')['PM2.5'].mean().sort_values()
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=region_avg.index, y=region_avg.values, palette='viridis')
        plt.xlabel("Region")
        plt.ylabel("Average PM2.5 Level")
        plt.title("Average PM2.5 Levels by Region", fontsize=16)
        plt.xticks(rotation=45)
        plt.show()
    else:
        messagebox.showwarning("Warning", "No data loaded yet!")

# Function to check high pollution levels
def check_high_pollution():
    if 'data' in globals():
        high_pollution = data[data['PM2.5'] > 100]
        if not high_pollution.empty:
            alert_text = "Regions with High Pollution:\n"
            alert_text += "\n".join(high_pollution['Region'].unique())
            messagebox.showwarning("High Pollution Alert", alert_text)
        else:
            messagebox.showinfo("Info", "All regions have safe pollution levels.")
    else:
        messagebox.showwarning("Warning", "No data loaded yet!")

# Frame for buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=20)

# Add buttons with improved style
load_button = tk.Button(button_frame, text="Load Data", command=load_data, bg="#4CAF50", fg="white", font=("time new roman", 16), width=20)
load_button.grid(row=0, column=0, padx=10)

summary_button = tk.Button(button_frame, text="Show Data Summary", command=show_data_summary, bg="#2196F3", fg="white", font=("time new roman", 16), width=20)
summary_button.grid(row=0, column=1, padx=10)

trend_button = tk.Button(button_frame, text="Plot PM2.5 Trends", command=plot_trends, bg="#FF9800", fg="white", font=("time new roman", 16), width=20)
trend_button.grid(row=1, column=0, padx=10)

region_button = tk.Button(button_frame, text="Compare by Region", command=plot_region_comparison, bg="#9C27B0", fg="white", font=("time new roman", 16), width=20)
region_button.grid(row=1, column=1, padx=10)

alert_button = tk.Button(button_frame, text="Check High Pollution", command=check_high_pollution, bg="#F44336", fg="white", font=("time new roman", 16), width=20)
alert_button.grid(row=2, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
