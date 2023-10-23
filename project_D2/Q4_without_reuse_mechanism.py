import tkinter as tk
from tkinter import filedialog

# Custom function to split input string into a list of numbers
def split_numbers(input_str):
    num_list = []
    num_str = ""
    for char in input_str:
        if char.isdigit() or char == '.' or (char == '-' and not num_str):
            num_str += char
        elif num_str:
            num_list.append(float(num_str))
            num_str = ""
    if num_str:
        num_list.append(float(num_str))
    return num_list

# Custom function to calculate the minimum value
def calculateMin():
    input_str = num_entry.get()
    num_list = split_numbers(input_str)
    if num_list:
        min_value = num_list[0]
        for num in num_list:
            if num < min_value:
                min_value = num
        display_result(f"Minimum is: {min_value}")

# Custom function to calculate the maximum value
def calculateMax():
    input_str = num_entry.get()
    num_list = split_numbers(input_str)
    if num_list:
        max_value = num_list[0]
        for num in num_list:
            if num > max_value:
                max_value = num
        display_result(f"Maximum is: {max_value}")

# Custom function to calculate the mean (average)
def calculateMean():
    input_str = num_entry.get()
    num_list = split_numbers(input_str)
    if num_list:
        total = 0
        count = 0
        for num in num_list:
            total += num
            count += 1
        mean = total / count
        display_result(f"Mean is: {mean}")

# Custom function to calculate the mode
def calculateMode():
    input_str = num_entry.get()
    num_list = split_numbers(input_str)
    if num_list:
        mode_dict = {}
        for num in num_list:
            if num not in mode_dict:
                mode_dict[num] = 1
            else:
                mode_dict[num] += 1
        max_count = 0
        modes = []
        for num, count in mode_dict.items():
            if count > max_count:
                max_count = count
                modes = [num]
            elif count == max_count:
                modes.append(num)
        display_result(f"Mode is: {modes}")

# Custom function to calculate the median
def calculateMedian():
    input_str = num_entry.get()
    num_list = split_numbers(input_str)
    if num_list:
        num_list.sort()
        n = len(num_list)
        if n % 2 == 0:
            median = (num_list[n // 2 - 1] + num_list[n // 2]) / 2
        else:
            median = num_list[n // 2]
        display_result(f"Median is: {median}")

# Custom function to calculate the mean absolute deviation
def calculateMAD():
    input_str = num_entry.get()
    num_list = split_numbers(input_str)
    if num_list:
        mean = 0
        count = 0
        for num in num_list:
            mean += num
            count += 1
        mean /= count
        mad = 0
        for num in num_list:
            mad += abs(num - mean)
        mad /= count
        display_result(f"Mean Absolute Deviation is: {mad}")

# Custom function to calculate the standard deviation
def calculateSD():
    input_str = num_entry.get()
    num_list = split_numbers(input_str)
    if num_list:
        mean = 0
        count = 0
        for num in num_list:
            mean += num
            count += 1
        mean /= count
        variance = 0
        for num in num_list:
            variance += (num - mean) ** 2
        variance /= count
        std_deviation = variance ** 0.5
        display_result(f"Standard Deviation is: {std_deviation}")

# Custom function to display the result
def display_result(result_text):
    result_label.config(text=result_text)


def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
            num_entry.delete(0, "end")
            num_entry.insert(0, data)


root = tk.Tk()
root.geometry("520x350")
root.title("Statistics Calculator")

header = tk.Label(root, text="METRICSTICS system", bg="green", fg="white", font=("Helvetica", 16))
header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

input_frame = tk.Frame(root, padx=20, pady=10)
input_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

num_label = tk.Label(input_frame, text="Enter numbers (space-separated): ", font=("Helvetica", 12))
num_label.grid(row=0, column=0, sticky="e")

num_entry = tk.Entry(input_frame, width=36, font=("Helvetica", 12))
num_entry.grid(row=0, column=1, sticky="w")
num_entry.focus()

result_label = tk.Label(root, text="", padx=20, pady=10, font=("Helvetica", 14))
result_label.grid(row=2, column=0, columnspan=2, sticky="ew")

button_frame = tk.Frame(root, padx=20, pady=10)
button_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

# Add buttons to the grid layout
upload_button = tk.Button(button_frame, text="Upload File", command=upload_file, font=("Helvetica", 15), highlightbackground="blue", highlightcolor="blue")
upload_button.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)


# Add buttons to the grid layout
calculateMin_button = tk.Button(button_frame, text="Calculate Minimum", command=calculateMin, font=("Helvetica", 15))
calculateMin_button.grid(row=1, column=0, columnspan=1, sticky="ew", padx=10, pady=5)

calculateMax_button = tk.Button(button_frame, text="Calculate Maximum", command=calculateMax, font=("Helvetica", 15))
calculateMax_button.grid(row=1, column=1, columnspan=1, sticky="ew", padx=10, pady=5)

calculateMean_button = tk.Button(button_frame, text="Calculate Mean", command=calculateMean, font=("Helvetica", 15))
calculateMean_button.grid(row=2, column=0, columnspan=1, sticky="ew", padx=10, pady=5)

calculateMode_button = tk.Button(button_frame, text="Calculate Mode", command=calculateMode, font=("Helvetica", 15))
calculateMode_button.grid(row=2, column=1, columnspan=1, sticky="ew", padx=10, pady=5)

calculateMedian_button = tk.Button(button_frame, text="Calculate Median", command=calculateMedian, font=("Helvetica", 15))
calculateMedian_button.grid(row=3, column=0, columnspan=1, sticky="ew", padx=10, pady=5)

calculateMAD_button = tk.Button(button_frame, text="Calculate Mean Absolute Deviation", command=calculateMAD, font=("Helvetica", 15))
calculateMAD_button.grid(row=3, column=1, columnspan=1, sticky="ew", padx=10, pady=5)

calculateSD_button = tk.Button(button_frame, text="Calculate Standard Deviation", command=calculateSD, font=("Helvetica", 15))
calculateSD_button.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

# Configure column weights to ensure equal width for the buttons
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()