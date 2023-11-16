import csv
import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from concurrent.futures import ProcessPoolExecutor

class Graph:
    def __init__(self, root, sessionId, username, login_ui):
        self.root = root
        self.sessionId = sessionId
        self.username = username
        self.login_ui = login_ui
        self.root.title("Graph")
        self.executor = ProcessPoolExecutor()
        self.clear_widgets()
        self.create_widgets()

    def create_widgets(self):
        self.header = tk.Label(self.root, text="Graph", bg="green", fg="white", font=("Helvetica", 16))
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.plot_graph()

        self.button_frame = tk.Frame(self.root, padx=10, pady=10)
        self.button_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.upload_button = tk.Button(self.button_frame, text="Back to Calculator", command=self.back,
                                       font=("Helvetica", 15))
        self.upload_button.grid(row=0, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
        
    def back(self):
        from calculator import StatisticsCalculator
        app = StatisticsCalculator(self.root, self.sessionId, self.username, self.login_ui)  # Pass the session ID to the application

    def plot_graph(self):
        # Read values from CSV
        min_values, max_values, mode_values, median_values, arithmetic_means, mad_values, std_dev_values = [], [], [], [], [], [], []
        with open(f'Output_{self.username}.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 1:
                    if row[0] == "Minimum":
                        min_values.append(float(row[1]))
                    elif row[0] == "Maximum":
                        max_values.append(float(row[1]))
                    elif row[0] == "Median":
                        median_values.append(float(row[1]))
                    elif row[0] == "Arithmetic mean":
                        arithmetic_means.append(float(row[1]))
                    elif row[0] == "Mean absolute deviation":
                        mad_values.append(float(row[1]))
                    elif row[0] == "Standard deviation":
                        std_dev_values.append(float(row[1]))

        # Creating the figure with subplots
        fig, axs = plt.subplots(2, 3, figsize=(10, 5))  # 2 rows, 3 columns

        # Plotting each graph
        axs[0, 0].plot(min_values, marker='o')
        axs[0, 0].set_title('Minimum')

        axs[0, 1].plot(max_values, marker='o')
        axs[0, 1].set_title('Maximum')

        axs[0, 2].plot(median_values, marker='o')
        axs[0, 2].set_title('Median')

        axs[1, 0].plot(arithmetic_means, marker='o')
        axs[1, 0].set_title('Arithmetic mean')

        axs[1, 1].plot(mad_values, marker='o')
        axs[1, 1].set_title('Mean absolute deviation')

        axs[1, 2].plot(std_dev_values, marker='o')
        axs[1, 2].set_title('Standard deviation')

        # Adjust layout
        plt.tight_layout()

        # Embedding the figure in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.root)  # self.root is your Tkinter window
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=10, column=0, columnspan=3, sticky="ew")
        canvas.draw()
    
    def mainFunction(self):
        self.clear_widgets()
        self.root.mainloop()
        self.executor.shutdown(wait=False)

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()