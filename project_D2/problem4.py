import statistics

import numpy as np
import pandas as pd
from numpy import mean, absolute
import tkinter as tk
from statistics import median
from tkinter import ttk


# tk._test()

def calculateMin():  # calculate min
    list = num_entry.get().split(" ")
    list = num_entry.get().split(" ")
    for i in range(0, len(list)):
        list[i] = float(list[i])
    print(f"Minimum is: {min(list)}")


def calculateMax():  # calculate max
    list = num_entry.get().split(" ")
    list = num_entry.get().split(" ")
    for i in range(0, len(list)):
        list[i] = float(list[i])
    print(f"Maximum is: {max(list)}")


def calculateMode():  # calculate mode
    list = num_entry.get().split(" ")
    for i in range(0, len(list)):
        list[i] = float(list[i])
    mode = {}
    for a in list:
        if a not in mode:
            mode[a] = 1
        else:
            mode[a] += 1
    print(f"Mode is: {[k for k, v in mode.items() if v == max(mode.values())]}")


def calculateMedian():  # calculate mean
    list = num_entry.get().split(" ")
    for i in range(0, len(list)):
        list[i] = float(list[i])
    print(f"Median is: {median(list)}")


def calculateArithmeticMean():
    list = num_entry.get().split(" ")
    list = num_entry.get().split(" ")
    for i in range(0, len(list)):
        list[i] = float(list[i])
    print(f"Arithmetic Mean is: {sum(list) / len(list)}")


def calculateMAD():
    list = num_entry.get().split(" ")
    for i in range(0, len(list)):
        list[i] = float(list[i])
    result = mean(absolute(list - mean(list)))
    print(f"Mean absolute deviation is: {result}")


def calculateSD():
    list = num_entry.get().split(" ")
    for i in range(0, len(list)):
        list[i] = float(list[i])
    result = statistics.stdev(list)
    print(f"Standard deviation is: {result}")


root = tk.Tk()
root.geometry("700x500")  # set window size

input_nums = tk.DoubleVar()

# display header
header = tk.Label(root, text="METRICSTICS system", bg="green", fg="white")
header.pack(ipadx=10, ipady=10, fill="x")

# a frame for input numbers from a user
input_frame = ttk.Frame(root, padding=(20, 10, 20, 0))
input_frame.pack(fill="both")

# ask user input value
num_label = ttk.Label(input_frame, text="Please enter the numbers: ")
num_label.pack(side="left", padx=(0, 10))
num_entry = ttk.Entry(input_frame, width=35, textvariable=input_nums)
num_entry.pack(side="left")
num_entry.focus()

# first button frame
button_frame = ttk.Frame(root, padding=(20, 10))
button_frame.pack(fill="both")

# button to calculate minimum
calculateMin_button = ttk.Button(button_frame, text="calculate minimum", command=calculateMin)
calculateMin_button.pack(side="left", expand="true")

# button to calculate maximum
calculateMax_button = ttk.Button(button_frame, text="calculate maximum", command=calculateMax)
calculateMax_button.pack(side="left", expand="true")

# button to calculate mode
calculateMode_button = ttk.Button(button_frame, text="calculate mode", command=calculateMode)
calculateMode_button.pack(side="left", expand="true")

# button to calculate median
calculateMedian_button = ttk.Button(button_frame, text="calculate median", command=calculateMedian)
calculateMedian_button.pack(side="left", expand="true")

# second button frame
button_frame2 = ttk.Frame(root, padding=(20, 10))
button_frame2.pack(fill="both")

# button to calculate arithmetic mean
calculateArithmeticMean_button = ttk.Button(button_frame2, text="calculate arithmetic mean",
                                            command=calculateArithmeticMean)
calculateArithmeticMean_button.pack(side="left", expand="true")

# button to calculate MAD
calculateMAD_button = ttk.Button(button_frame2, text="calculate mean absolute deviation", command=calculateMAD)
calculateMAD_button.pack(side="left", expand="true")

# button to calculate SD
calculateSD_button = ttk.Button(button_frame2, text="calculate standard deviation", command=calculateSD)
calculateSD_button.pack(side="left", expand="true")

# keeps the window visible
# typically as the last statement after creating widgets
root.mainloop()
