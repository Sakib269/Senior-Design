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

def QJH_calc():
    # Open Excel file
    file_name = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
    if not file_name:
        return

    wb = openpyxl.load_workbook(file_name)
    ws = wb.active
    
    # Grab Voltage from Column 1
    voltage = []
    for i in range(2, ws.max_row + 1):
        voltage.append(float(ws.cell(row=i, column=1).value))

    # Grab Current from Column 2
    current = []
    for i in range(2, ws.max_row + 1):
        current.append(float(ws.cell(row=i, column=2).value))

    # The reset voltage is the voltage where the current suddenly drops in value
    # find the reset voltage
    for i in range(1, len(current)):
        if current[i] < current [i+1]:
            reset_voltage = voltage[i + 1]
            break
    
    # Calculate the QJh value for user defined compliance current
    F_dissipation = simpledialog.askfloat("Input", "Enter the fraction of heat dissipated by convection and thermal radiation as a decimal:")
    Icc = simpledialog.askfloat("Input", "Enter the compliance current in uA:")
    Icc = -(Icc * 10**(-6))
    RR = .276
    C = .29
    Qjh = ((reset_voltage**3 * Icc) / (3 * RR * C)) * (1 - F_dissipation)
    Qjh = round(Qjh * 10**6, 2)
    
    # Display the output in the text widget
    output_text.insert(tk.END, "The reset voltage is: " + str(reset_voltage) + " volts\n")
    output_text.insert(tk.END, "Qjh is: " + str(Qjh) + " micro Joules\n")

    # Plot the data
    fig, ax = plt.subplots()
    ax.plot(voltage, current)
    ax.set(xlabel='Voltage (V)', ylabel='Current (uA)', title='Voltage vs Current')

    # Create a canvas that can fit the above plot
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