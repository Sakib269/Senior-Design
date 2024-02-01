# Parse Excel Data and determine the QJh value for each data point
# QJh = (Vreset^3 * Icc) / (3 * RR * C)
# Determine Vreset from Data
# Pass Excel file name and Compliance current as arguments
# def determine_QJh(file_name, Icc):
# Open Excel file
import tkinter as tk
from tkinter import filedialog, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import openpyxl
import os

def QJH_calc():
    global output_text
    global canvas
    # Open Excel file
    file_name = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
    if not file_name:
        return

    wb = openpyxl.load_workbook(file_name)
    ws = wb['Sheet1']

    column_names = [cell.value for cell in ws[1]]
    
    # Find the indices of the columns you're interested in
    try:
        voltage_column_index = column_names.index('AV') + 1  # +1 because openpyxl uses 1-based indexing
        current_column_index = column_names.index('AI') + 1
        time_column_index = column_names.index('Time') + 1
    except ValueError:
        tk.messagebox.showerror("Error", "Excel file does not contain 'AV' and 'AI' columns")
        return
    
    # Grab Voltage from column AV
    voltage = []
    for i in range(2, ws.max_row + 1):
        voltage.append(float(ws.cell(row=i, column=voltage_column_index).value))

    # Grab Current from Column AI
    current = []
    for i in range(2, ws.max_row + 1):
        current.append(float(ws.cell(row=i, column=current_column_index).value))

    # Grab Time from Column Time
    time = []
    for i in range(2, ws.max_row + 1):
        time.append(float(ws.cell(row=i, column=time_column_index).value))

    # The reset voltage is the voltage where the current suddenly drops in value
    # find the reset voltage
    for i in range(1, len(current)):
        if current[i] > current[0]:
            reset_voltage = - (voltage[i + 1])
            break
    
    # Calculate the QJh value for user defined compliance current
    F_dissipation = simpledialog.askfloat("Input", "Enter the fraction of heat dissipated by convection and thermal radiation as a decimal:")
    # Icc = simpledialog.askfloat("Input", "Enter the compliance current in uA:")
    RR = simpledialog.askfloat("Input", "Enter the Ramping Rate in V/s:")
    Ron = simpledialog.askfloat("Input", "Enter the Ron value in Ohms:")
    # Icc = -(Icc * 10**(-6))
    Qjh = ((reset_voltage**3 ) / (3 * RR * Ron)) * (1 - F_dissipation)
    Qjh = round(Qjh * 10**6, 2)
    # Clear the text widget
    output_text.delete(1.0, tk.END)
    # Clear the plot widget
    plt.clf()
    # Icc = round(Icc * 10**6, 2)
    reset_voltage = round(reset_voltage, 2)
    # Display the output in the text widget
    #display the file name
    output_text.insert(tk.END, "File Name: " + os.path.basename(file_name) + "\n")
    # output_text.insert(tk.END, "The compliance current is: " + str(Icc) + " uA\n")
    output_text.insert(tk.END, "The fraction of heat dissipated by convection and thermal radiation is: " + str(F_dissipation) + "\n")
    output_text.insert(tk.END, "The ramping rate is: " + str(RR) + " V/s\n")
    output_text.insert(tk.END, "The reset voltage is: " + str(reset_voltage) + " volts\n")
    output_text.insert(tk.END, "Qjh is: " + str(Qjh) + " micro Joules\n")

    # Plot the data
    fig, ax = plt.subplots()
    ax.plot(voltage, current)
    ax.set(xlabel='Voltage (V)', ylabel='Current (uA)', title='Voltage vs Current')

    # Create a canvas that can fit the above plot
    if 'canvas' in globals():
        canvas.get_tk_widget().pack_forget()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    button = tk.Button(root, text="Open File", command=QJH_calc)
    button.pack()
    # Create a text widget and pack it
    output_text = tk.Text(root)
    output_text.pack()
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()