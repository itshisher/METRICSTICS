import csv
import random
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import logging
import re
from tkinter import messagebox
from concurrent.futures import ProcessPoolExecutor


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

        self.num_label = tk.Label(self.input_frame, text="Enter numbers (space/comma separated): ", font=("Helvetica", 12))
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
        self.upload_button = tk.Button(self.button_frame, text="Upload File", command=self.upload_file, font=("Helvetica", 15), highlightbackground="blue", highlightcolor="blue")
        self.upload_button.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.calculateMin_button = tk.Button(self.button_frame, text="Calculate Minimum", command=self.calculateMin, font=("Helvetica", 15))
        self.calculateMin_button.grid(row=1, column=0, columnspan=1, sticky="ew", padx=10, pady=5)
        self.calculateMax_button = tk.Button(self.button_frame, text="Calculate Maximum", command=self.calculateMax, font=("Helvetica", 15))
        self.calculateMax_button.grid(row=1, column=1, columnspan=1, sticky="ew", padx=10, pady=5)
        self.calculateMean_button = tk.Button(self.button_frame, text="Calculate Mean", command=self.calculateMean, font=("Helvetica", 15))
        self.calculateMean_button.grid(row=2, column=0, columnspan=1, sticky="ew", padx=10, pady=5)

        self.calculateMode_button = tk.Button(self.button_frame, text="Calculate Mode", command=self.calculateMode, font=("Helvetica", 15))
        self.calculateMode_button.grid(row=2, column=1, columnspan=1, sticky="ew", padx=10, pady=5)

        self.calculateMedian_button = tk.Button(self.button_frame, text="Calculate Median", command=self.calculateMedian,
                                           font=("Helvetica", 15))
        self.calculateMedian_button.grid(row=3, column=0, columnspan=1, sticky="ew", padx=10, pady=5)

        self.calculateMAD_button = tk.Button(self.button_frame, text="Calculate Mean Absolute Deviation", command=self.calculateMAD,
                                        font=("Helvetica", 15))
        self.calculateMAD_button.grid(row=3, column=1, columnspan=1, sticky="ew", padx=10, pady=5)

        self.calculateSD_button = tk.Button(self.button_frame, text="Calculate Standard Deviation", command=self.calculateSD,
                                        font=("Helvetica", 15))
        self.calculateSD_button.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        Label(self.button_frame, text="Please input number of data: ").grid(row=5, column=0, columnspan=1, sticky="ew", padx=5,
                                                                        pady=2)
        self.numData = StringVar()
        Entry(self.button_frame, textvariable=self.numData).grid(row=5, column=1, columnspan=1, sticky="ew", padx=5, pady=2)

        self.generate_data_button = tk.Button(self.button_frame, text="Generate", command=self.generate_data, font=("Helvetica", 15))
        self.generate_data_button.grid(row=6, column=0, columnspan=1, sticky="ew", padx=5, pady=2)

        self.clear_data_button = tk.Button(self.button_frame, text="Reset", command=self.reset_data, font=("Helvetica", 15))
        self.clear_data_button.grid(row=6, column=1, columnspan=1, sticky="ew", padx=5, pady=2)

        self.save_data_button = tk.Button(self.button_frame, text="Add record", command=self.write_file, font=("Helvetica", 15))
        self.save_data_button.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        self.previous_button = tk.Button(self.button_frame, text="Previous Session", command=self.previous_session, font=("Helvetica", 15))
        self.previous_button.grid(row=8, column=0, columnspan=1, sticky="ew", padx=5, pady=5)
        
        self.logout_button = tk.Button(self.button_frame, text="Logout", command=self.logout, font=("Helvetica", 15))
        self.logout_button.grid(row=8, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        

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


    # Modify all calculation methods to use the executor
    def calculateMinValue(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            future = self.executor.submit(self.calculateMin, num_list)
            future.add_done_callback(self.on_calculation_done("Minimum is: {}"))

    def calculateMaxValue(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            future = self.executor.submit(self.calculateMax, num_list)
            future.add_done_callback(self.on_calculation_done("Maximum is: {}"))

    def calculateMeanValue(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            future = self.executor.submit(self.calculateMean, num_list)
            future.add_done_callback(self.on_calculation_done("Mean is: {}"))

    def calculateModeValue(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            future = self.executor.submit(self.calculateMode, num_list)
            future.add_done_callback(self.on_calculation_done("Mode is: {}"))

    def calculateMedianValue(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            future = self.executor.submit(self.calculateMedian, num_list)
            future.add_done_callback(self.on_calculation_done("Median is: {}"))

    def calculateMADValue(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            future = self.executor.submit(self.calculateMAD, num_list)
            future.add_done_callback(self.on_calculation_done("Mean Absolute Deviation is: {}"))

    def calculateSDValue(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            future = self.executor.submit(self.calculateSD, num_list)
            future.add_done_callback(self.on_calculation_done("Standard Deviation is: {}"))



    def calculateMin(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            min_value = num_list[0]
            for num in num_list:
                if num < min_value:
                    min_value = num
            self.display_result(f"Minimum is: {int(min_value)}")
            info = (
                "Minimum number in the list: ",
                num_list,
                "is",
                min_value
            )
            logging.info(info)
            return min_value

    def calculateMax(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            max_value = num_list[0]
            for num in num_list:
                if num > max_value:
                    max_value = num
            self.display_result(f"Maximum is: {int(max_value)}")
            info = (
                "Maximum number in the list: ",
                num_list,
                "is",
                max_value
            )
            logging.info(info)
            return max_value

    def calculateMean(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            total = 0
            count = 0
            for num in num_list:
                total += num
                count += 1
            mean = total / count
            self.display_result(f"Mean is: {mean}")
            info = (
                "Mean value in the list: ",
                num_list,
                "is",
                mean
            )
            logging.info(info)
            return mean

    def calculateMode(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
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
            self.display_result(f"Mode is: {modes}")
            info = (
                "Mode/modes in the list: ",
                num_list,
                "is/are",
                modes
            )
            logging.info(info)
            return modes


    def calculateMedian(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            num_list.sort()
            n = len(num_list)
            if n % 2 == 0:
                median = (num_list[n // 2 - 1] + num_list[n // 2]) / 2
            else:
                median = num_list[n // 2]
            self.display_result(f"Median is: {median}")
            info = (
                "Median in the list: ",
                num_list,
                "is",
                median
            )
            logging.info(info)
            return median


    def calculateMAD(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            mean = 0
            count = 0
            for num in num_list:
                mean += num
                count += 1
            mean /= count
            mad = sum(abs(num - mean) for num in num_list)
            mad /= count
            self.display_result(f"Mean Absolute Deviation is: {mad}")
            info = (
                "Mean absolute deviation in the list: ",
                num_list,
                "is",
                mad
            )
            logging.info(info)
            return mad

    def calculateSD(self):
        input_str = self.num_entry.get()
        if num_list := self.split_numbers(input_str):
            mean = 0
            count = 0
            for num in num_list:
                mean += num
                count += 1
            mean /= count
            variance = sum((num - mean) ** 2 for num in num_list)
            variance /= count
            std_deviation = variance ** 0.5
            self.display_result(f"Standard Deviation is: {std_deviation}")
            info = (
                "Standard deviation in the list: ",
                num_list,
                "is",
                std_deviation
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
        with open(f"Output_{self.username}.csv", 'r') as file:
                content = file.read().strip()  # Remove any trailing whitespace or newline characters
                sets = content.split('\n\n')  # Splitting by double newline to get each set of data
                return self.display_result(sets[-1]) if sets else  self.display_result("No content found")  # Return the last set of data

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
            else :
                # wt.writerow(['Statistic', 'Value'])
                wt.writerow(['Minimum', min_value])
                wt.writerow(['Maximum', max_value])
                wt.writerow(['Mode', mode_value])
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
        with open(f"data_{self.username}.csv", 'w', newline='') as data:
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


