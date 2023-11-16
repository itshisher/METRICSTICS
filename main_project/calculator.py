import csv
import random
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import logging
import re
from tkinter import messagebox
from concurrent.futures import ProcessPoolExecutor
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph import Graph

# logging format
logging.basicConfig(filename="scraper.log", level=logging.DEBUG,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class StatisticsCalculator:
    def __init__(self, root, sessionId, username, login_ui):
        self.root = root
        self.sessionId = sessionId
        self.username = username
        self.login_ui = login_ui
        self.root.title("Statistic Calculator")
        self.executor = ProcessPoolExecutor()
        self.clear_widgets()
        self.create_widgets()

    def create_widgets(self):
        self.header = tk.Label(self.root, text="METRICSTICS system", bg="green", fg="white", font=("Helvetica", 16))
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.input_frame = tk.Frame(self.root, padx=20, pady=10)
        self.input_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.num_label = tk.Label(self.input_frame, text="Enter numbers (space/comma separated): ",
                                  font=("Helvetica", 12))
        self.num_label.grid(row=0, column=0, sticky="e")

        self.num_entry = tk.Entry(self.input_frame, width=36, font=("Helvetica", 12))
        self.num_entry.grid(row=0, column=1, sticky="w")
        self.num_entry.focus()

        # self.result_label = tk.Label(self.root, text="", padx=20, pady=10, font=("Helvetica", 14))
        # self.result_label.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.result_label = tk.Text(self.root, height=10, width=70)  # Adjust height and width as needed
        self.scrollbar = tk.Scrollbar(self.root, command=self.result_label.yview)
        self.result_label.configure(yscrollcommand=self.scrollbar.set)
        self.result_label.grid(row=2, column=0)
        self.scrollbar.grid(row=2, column=1, sticky='ns')

        self.button_frame = tk.Frame(self.root, padx=10, pady=10)
        self.button_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

        # Populate the frame with buttons
        self._create_buttons()

        # Configure column weights to ensure equal width for the buttons
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def _create_buttons(self):

        # This is a helper function to modularize button creation
        # Add buttons to the grid layout
        self.upload_button = tk.Button(self.button_frame, text="Upload File", command=self.upload_file,
                                       font=("Helvetica", 15), highlightbackground="blue", highlightcolor="blue")
        self.upload_button.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.calculateMin_button = tk.Button(self.button_frame, text="Calculate Minimum", command=self.calculateMin,
                                             font=("Helvetica", 15))
        self.calculateMin_button.grid(row=1, column=0, columnspan=1, sticky="ew", padx=10, pady=5)
        self.calculateMax_button = tk.Button(self.button_frame, text="Calculate Maximum", command=self.calculateMax,
                                             font=("Helvetica", 15))
        self.calculateMax_button.grid(row=1, column=1, columnspan=1, sticky="ew", padx=10, pady=5)
        self.calculateMean_button = tk.Button(self.button_frame, text="Calculate Mean", command=self.calculateMean,
                                              font=("Helvetica", 15))
        self.calculateMean_button.grid(row=2, column=0, columnspan=1, sticky="ew", padx=10, pady=5)

        self.calculateMode_button = tk.Button(self.button_frame, text="Calculate Mode", command=self.calculateMode,
                                              font=("Helvetica", 15))
        self.calculateMode_button.grid(row=2, column=1, columnspan=1, sticky="ew", padx=10, pady=5)

        self.calculateMedian_button = tk.Button(self.button_frame, text="Calculate Median",
                                                command=self.calculateMedian,
                                                font=("Helvetica", 15))
        self.calculateMedian_button.grid(row=3, column=0, columnspan=1, sticky="ew", padx=10, pady=5)

        self.calculateMAD_button = tk.Button(self.button_frame, text="Calculate Mean Absolute Deviation",
                                             command=self.calculateMAD,
                                             font=("Helvetica", 15))
        self.calculateMAD_button.grid(row=3, column=1, columnspan=1, sticky="ew", padx=10, pady=5)

        self.calculateSD_button = tk.Button(self.button_frame, text="Calculate Standard Deviation",
                                            command=self.calculateSD,
                                            font=("Helvetica", 15))
        self.calculateSD_button.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        Label(self.button_frame, text="Please input number of data: ").grid(row=5, column=0, columnspan=1, sticky="ew",
                                                                            padx=5,
                                                                            pady=2)
        self.numData = StringVar()
        Entry(self.button_frame, textvariable=self.numData).grid(row=5, column=1, columnspan=1, sticky="ew", padx=5,
                                                                 pady=2)

        self.generate_data_button = tk.Button(self.button_frame, text="Generate", command=self.generate_data,
                                              font=("Helvetica", 15))
        self.generate_data_button.grid(row=6, column=0, columnspan=1, sticky="ew", padx=5, pady=2)

        self.clear_data_button = tk.Button(self.button_frame, text="Reset", command=self.reset_data,
                                           font=("Helvetica", 15))
        self.clear_data_button.grid(row=6, column=1, columnspan=1, sticky="ew", padx=5, pady=2)

        self.save_data_button = tk.Button(self.button_frame, text="Add record", command=self.write_file,
                                          font=("Helvetica", 15))
        self.save_data_button.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.previous_button = tk.Button(self.button_frame, text="Previous Session", command=self.previous_session,
                                         font=("Helvetica", 15))
        self.previous_button.grid(row=8, column=0, columnspan=1, sticky="ew", padx=5, pady=5)

        self.logout_button = tk.Button(self.button_frame, text="Logout", command=self.logout, font=("Helvetica", 15))
        self.logout_button.grid(row=8, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        self.delete_data_button = tk.Button(self.button_frame, text="Delete Data", command=self.delete_data, font=("Helvetica", 15))
        self.delete_data_button.grid(row=9, column=0, columnspan=1, sticky="ew", padx=5, pady=5)

        self.graph_button = tk.Button(self.button_frame, text="Graph", command=self.plot_graph, font=("Helvetica", 15))
        self.graph_button.grid(row=9, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        
    def delete_data(self):
        self.result_label.delete('1.0', tk.END)
        try:
            with open(f"Data_{self.username}.csv", "w") as f:
                # File is opened in 'w' mode to clear its content
                pass  # 'pass' is used as a placeholder since no action is needed.
            print(f)
            logging.info('All data in the file has been successfully deleted.')
        except Exception as e:
            print("AWEF")
            logging.error(f"Error occurred while trying to delete data: {e}")

    def plot_graph(self):
        app = Graph(self.root, self.sessionId, self.username, self.login_ui)  # Pass the session ID to the application

    def split_numbers(self, input_str):
        num_list = []
        num_str = ""
        for char in input_str:
            if char.isdigit() or char == '.' or (char == '-' and not num_str):
                num_str += char
            elif num_str:
                num_list.append(float(num_str))
                num_str = ""
            elif not char.isdigit():  # erroe msg if with wrong input
                messagebox.showerror('Python Error', 'Error: This is not an digit! Please try again!')
                logging.info('Input data is not a digit...')
                return
        if num_str:
            num_list.append(float(num_str))
        info = (
            "Numbers to split: ",
            num_list
        )
        logging.info(info)
        return num_list

    def calculateMin(self):
        start_time = time.time()
        input_str = self.num_entry.get()
        num_list = self.split_numbers(input_str)
        if not num_list:
            return None

        # Define a recursive function to find minimum, DAC technique
        def min_recursive(arr):
            length = len(arr)

            # If the list is of length 1, return the single element as the minimum
            if length == 1:
                return arr[0]

            # If the list has more than one element, divide it into two halves
            mid = length // 2
            left_min = min_recursive(arr[:mid])  # Minimum of the left segment
            right_min = min_recursive(arr[mid:])  # Minimum of the right segment

            # Compare the minimums of the two segments
            return left_min if left_min < right_min else right_min

        # Call the recursive function on the entire list
        min_value = min_recursive(num_list)

        # Display the minimum value and log the information
        self.display_result(f"Minimum is: {min_value}")
        end_time = time.time()
        info = (
            "The length of dataset is: ",
            len(num_list),
            "Minimum number in the list is: ",
            min_value,
            "Time spent on this calculations is: ",
            f"--- {end_time - start_time} seconds ---",
        )
        logging.info(info)

        return min_value

    def calculateMax(self):
        start_time = time.time()
        input_str = self.num_entry.get()
        num_list = self.split_numbers(input_str)
        if not num_list:
            return None

        # Define a recursive function to find maximum, DAC technique
        def max_recursive(arr):
            length = len(arr)

            # If the list is of length 1, return the single element as the maximum
            if length == 1:
                return arr[0]

            # If the list has more than one element, divide it into two halves
            mid = length // 2
            left_max = max_recursive(arr[:mid])  # Maximum of the left segment
            right_max = max_recursive(arr[mid:])  # Maximum of the right segment

            # Compare the maximums of the two segments
            return left_max if left_max > right_max else right_max

        # Call the recursive function on the entire list
        max_value = max_recursive(num_list)

        # Display the maximum value and log the information
        self.display_result(f"Maximum is: {max_value}")
        end_time = time.time()
        info = (
            "The length of dataset is: ",
            len(num_list),
            "Maximum number in the list is : ",
            max_value,
            "Time spent on this calculations is: ",
            f"--- {end_time - start_time} seconds ---",
        )
        logging.info(info)

        return max_value

    def calculateMean(self):
        start_time = time.time()
        input_str = self.num_entry.get()
        num_list = self.split_numbers(input_str)
        if not num_list:
            return None

        # Define a recursive function to find the mean, DAC technique
        def mean_recursive(arr):
            length = len(arr)

            # Base case: if the list has only one element, return that element
            if length == 1:
                return arr[0], 1

            # If the list has more than one element, divide it into two halves
            mid = length // 2
            left_sum, left_count = mean_recursive(arr[:mid])  # Mean and count of the left segment
            right_sum, right_count = mean_recursive(arr[mid:])  # Mean and count of the right segment

            total = left_sum + right_sum # Sum of the entire segment
            combined_count = left_count + right_count # Count of the entire segment
            return total, combined_count

        # Call the recursive function on the entire list
        final_sum, final_count = mean_recursive(num_list)
        mean = final_sum / final_count  # Calculate the final mean

        # Display the mean and log the information
        self.display_result(f"Mean is: {mean}")
        end_time = time.time()
        info = (
            "The length of dataset is: ",
            len(num_list),
            "Mean value in the list is: ",
            mean,
            "Time spent on this calculations is: ",
            f"--- {end_time - start_time} seconds ---",
        )
        logging.info(info)

        return mean

    def calculateMode(self):
        start_time = time.time()
        input_str = self.num_entry.get()
        num_list = self.split_numbers(input_str)
        if not num_list:
            return None

        mode_dict = {}
        max_count = 0
        modes = []

        for num in num_list:
            if num in mode_dict:
                mode_dict[num] += 1
            else:
                mode_dict[num] = 1

            if mode_dict[num] > max_count:
                max_count = mode_dict[num]
                modes = [num]
            elif mode_dict[num] == max_count and num not in modes:
                modes.append(num)

        if max_count == 1:
            self.display_result("No mode found, all numbers appear once")
            return None
        else:
            self.display_result(f"Mode is: {modes}")
        end_time = time.time()
        info = (
            "The length of dataset is: ",
            len(num_list),
            "Mode in the list is: ",
            modes,
            "Time spent on this calculations is: ",
            f"--- {end_time - start_time} seconds ---",
        )
        logging.info(info)

        return modes

    def calculateMedian(self):
        start_time = time.time()
        input_str = self.num_entry.get()
        num_list = self.split_numbers(input_str)
        def partition(lst, low, high):
            pivot = lst[high]
            i = low - 1

            for j in range(low, high):
                if lst[j] <= pivot:
                    i = i + 1
                    lst[i], lst[j] = lst[j], lst[i]

            lst[i + 1], lst[high] = lst[high], lst[i + 1]
            return i + 1

        def quick_select(lst, low, high, k):
            if low == high:
                return lst[low]

            pivot = partition(lst, low, high)
            if k == pivot:
                return lst[k]
            elif k < pivot:
                return quick_select(lst, low, pivot - 1, k)
            else:
                return quick_select(lst, pivot + 1, high, k)

        if not num_list:
            return None

        n = len(num_list)
        is_even = (n % 2 == 0)
        mid = n // 2

        median = quick_select(num_list, 0, n - 1, mid - 1) if is_even else quick_select(num_list, 0, n - 1, mid)

        self.display_result(f"Median is: {median}")
        end_time = time.time()
        info = (
            "The length of dataset is: ",
            len(num_list),
            "Median in the list is: ",
            median,
            "Time spent on this calculations is: ",
            f"--- {end_time - start_time} seconds ---",
        )
        logging.info(info)

        return median

    def calculateMAD(self):
        start_time = time.time()
        input_str = self.num_entry.get()
        num_list = self.split_numbers(input_str)
        if not num_list:
            return None

        mean = self.calculateMean()
        mad = sum(abs(num - mean) for num in num_list) / len(num_list) if len(num_list) > 0 else 0
        self.display_result(f"Mean Absolute Deviation is: {mad}")
        end_time = time.time()
        info = (
            "The length of dataset is: ",
            len(num_list),
            "Mean absolute deviation in the list is: ",
            mad,
            "Time spent on this calculations is: ",
            f"--- {end_time - start_time} seconds ---",
        )
        logging.info(info)
        return mad

    def calculateSD(self):
        start_time = time.time()
        input_str = self.num_entry.get()
        num_list = self.split_numbers(input_str)
        if not num_list or len(num_list) == 1:
            return None

        n = 0
        mean = 0
        M2 = 0

        for num in num_list:
            n += 1
            delta = num - mean
            mean += delta / n
            delta2 = num - mean
            M2 += delta * delta2

        variance = M2 / (n - 1) if n > 1 else 0
        std_deviation = variance ** 0.5

        self.display_result(f"Standard Deviation is: {std_deviation}")
        end_time = time.time()
        info = (
            "The length of dataset is: ",
            len(num_list),
            "Standard deviation in the list is: ",
            std_deviation,
            "Time spent on this calculations is: ",
            f"--- {end_time - start_time} seconds ---",
        )
        logging.info(info)
        return std_deviation

    def on_calculation_done(self, message_format):
        def callback(future):
            try:
                result = future.result()
                self.display_result(message_format.format(result))
            except Exception as e:
                messagebox.showerror('Error', str(e))
                logging.error(f'Error in calculation: {str(e)}')

        return callback

    # def display_result(self, result_text):
    #     self.result_label.config(text=result_text)
    #     logging.info('Result successfully displayed!')

    def display_result(self, result_text):
        # Modified part - Updating the display_result method
        self.result_label.insert(tk.END, result_text + "\n")  # Appends the new result
        logging.info('Result successfully displayed!')

    def upload_file(self):
        self.result_label.delete('1.0', tk.END)
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.csv")])
        if self.file_path:
            with open(self.file_path, 'r') as file:
                csv_reader = csv.reader(file)
                common_separated_numbers = ",".join(
                    ",".join(str(int(value)) for value in row)
                    for row in csv_reader
                )
                self.num_entry.delete(0, "end")
                self.num_entry.insert(0, common_separated_numbers)

            logging.info('File successfully uploaded!')

    def logout(self):
        # self.root.destroy()
        self.login_ui()

    def previous_session(self):
        self.result_label.delete('1.0', tk.END)
        with open(f"Output_{self.username}.csv", 'r') as file:
            content = file.read().strip()  # Remove any trailing whitespace or newline characters
            sets = content.split('\n\n')  # Splitting by double newline to get each set of data
            return self.display_result(sets[-1]) if sets else self.display_result(
                "No content found")  # Return the last set of data

    def write_file(self):
        self.result_label.delete('1.0', tk.END)
        with open(f"Output_{self.username}.csv", "a+", newline="") as f:
            wt = csv.writer(f, delimiter=',')
            min_value = self.calculateMin()
            max_value = self.calculateMax()
            mean_value = self.calculateMean()
            mode_value = self.calculateMode()
            median_value = self.calculateMedian()
            mad_value = self.calculateMAD()
            sd_value = self.calculateSD()
            if min_value is None:
                logging.info('No input values found!')
                print("No input values found!")
            else:
                # wt.writerow(['Statistic', 'Value'])
                wt.writerow(['Minimum', min_value])
                wt.writerow(['Maximum', max_value])
                if mode_value != None: 
                    wt.writerow(['Mode', mode_value])
                else : 
                    wt.writerow(['Mode', 'None'])
                wt.writerow(['Median', median_value])
                wt.writerow(['Arithmetic mean', mean_value])
                wt.writerow(['Mean absolute deviation', mad_value])
                wt.writerow(['Standard deviation', sd_value])
                wt.writerow([])
                print("Record has been inserted!")
                logging.info('File successfully saved!')
        f.close()

    def generate_data(self):
        self.result_label.delete('1.0', tk.END)
        with open(f"Data_{self.username}.csv", 'w', newline='') as data:
            wr = csv.writer(data, quoting=csv.QUOTE_ALL)
            num_data = self.numData.get()
            self.mylist = []
            self.mylist.extend(random.randint(-1000000, 1000000) for _ in range(int(num_data)))
            logging.info('Data successfully generated!')
            wr.writerow(self.mylist)

    def reset_data(self):
        self.result_label.delete('1.0', tk.END)
        for widget in self.button_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0, 'end')
        for widget in self.input_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.delete(0, 'end')
        logging.info('Data successfully reset!')

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mainFunction(self):
        self.clear_widgets()
        self.root.mainloop()
        self.executor.shutdown(wait=False)
