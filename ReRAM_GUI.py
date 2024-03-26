# Select an excel file with the voltage and current data
# Calculate the QJh value for the user defined Ron value
# Calculate the temperature of the copper, platinum, and silicon dioxide
# Plot the voltage vs current data
import math
import tkinter as tk
from tkinter import filedialog, simpledialog, BooleanVar
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import openpyxl
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import os



def QJH_calc():
    global text_to_file_str
    # Constants
    # electrode distance in microns
    electrode_distance = 150 * (10**-6) # 150 um to meters
    # Thermal conductivity of copper in W/mC or W/mK
    thermal_conductivity_copper = 385
    # Thermal conductivity of platinum in W/mC or W/mK
    thermal_conductivity_platinum = 69.1
    if Copper_electrode.get() and Platinum_electrode.get():
        tk.messagebox.showerror("Error", "Both Copper and Platinum electrodes cannot be selected at the same time.")
        return
    # Calculate the Qjh from the new equation
    # Qjh = Q_h + Q_p
    # Get inputs for the heated probe current and the Ron value
    I_H = (float(I_H_entry.get()) * 10**-6) # convert from microamps to amps
    Ron_H = float(Ron_H_entry.get())
    # Get inputs from probing cell
    I_P = (float(I_P_entry.get()) * 10**-6) # convert from microamps to amps
    Ron_P = float(Ron_P_entry.get())
    # Get time in seconds
    time = float(time_entry.get())
    # Calculate the Q_h
    Q_h = (I_H**2) * Ron_H * time
    # Calculate the Q_p
    Q_p = (I_P**2) * Ron_P * time
    # Calculate the DeltaQ
    DeltaQ = Q_h + Q_p
    # Get electrode width
    width = (float(width_entry.get()) * 10**-6) # convert width to meters
    # Get the order of the filament
    filament_order = float(filament_order_entry.get())
    distance = (width + electrode_distance) * filament_order
    # Choose K from boolean variables based on the user selection
    if Platinum_electrode.get():
        K = thermal_conductivity_platinum
        Across = (width) * (50 * 10**-9) # use meters
        eletrode_material = "Platinum"

    if Copper_electrode.get():
        K = thermal_conductivity_copper
        Across = (width) * (150 * 10**-9) # use meters
        eletrode_material = "Copper"
    # Calculate the DeltaT
    DeltaT = (DeltaQ * distance) / (K * Across * time)
    # round the values to 2 decimal places
    Q_h = round(Q_h, 5)
    Q_p = round(Q_p, 5)
    DeltaQ = round(DeltaQ, 5)
    DeltaT = round(DeltaT, 2)
    input_text_str = (
        "I_H: " + str(I_H) + "\n" +
        "Ron_H: " + str(Ron_H) + "\n" +
        "I_P: " + str(I_P) + "\n" +
        "Ron_P: " + str(Ron_P) + "\n" +
        "Time: " + str(time) + "\n" +  
        "Width: " + str(width) + "\n" +
        "Filament Order: " + str(filament_order) + "\n"
    )
    # Concatenate all the strings
    output_text_str = (
        "The selected material is: " + str(eletrode_material) + "\n" +
        "DeltaT: " + str(DeltaT) + "\n" 
        )
    # combine the input and output strings
    text_to_file_str = (input_text_str + "\n" + output_text_str)
    # Create a text widget to display the output
    output_text = tk.Text(root, width=35, height=15, wrap=tk.WORD, bg='gray14', fg='SpringGreen2')
    output_text.grid(row=10, column=0, columnspan=2)
    # Insert the result into the text widget
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output_text_str)

def save_to_file():
    global text_to_file_str
    # Get the filename to save the text to
    file_name = filedialog.asksaveasfilename(filetypes=[("Text files", "*.txt")])
    if file_name:
        # Ensure the file has a .txt extension
        if not file_name.endswith('.txt'):
            file_name += '.txt'
        with open(file_name, "w") as file:
            file.write(text_to_file_str)

def Graph_from_Excel():
    file_name = askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
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
    # Covert microamps to nanoamps for graph
    current = [i * 10**3 for i in current]
    # Plot the voltage vs current data
    fig, ax = plt.subplots()
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('gray')
    ax.set_facecolor('gray')
    ax.spines['bottom'].set_color('darkblue')
    ax.spines['top'].set_color('darkblue') 
    ax.spines['right'].set_color('darkblue')
    ax.spines['left'].set_color('darkblue')
    ax.xaxis.label.set_color('darkblue')
    ax.yaxis.label.set_color('darkblue')
    ax.tick_params(axis='x', colors='darkblue')
    ax.tick_params(axis='y', colors='darkblue')
    ax.plot(voltage, current, 'r')
    ax.set(xlabel='Voltage (V)', ylabel='Current (nA)', title='Voltage vs Current')
    ax.grid()
    # Create the canvas to display the graph
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=11, column=0, rowspan = 1, columnspan=2)
    # Create a text widget to display the output
    output_text = tk.Text(root, width=30, height=1, wrap=tk.WORD, bg='black', fg='deep sky blue')
    output_text.grid(row=10, column=0, rowspan = 1, columnspan=1)
    output_text.delete(1.0, tk.END)
    reset_voltage = round(reset_voltage, 2)
    output_text.insert(tk.END, "The reset voltage is: " + str(reset_voltage) + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("GUI")
    root.configure(bg='black')

    # Create a menubar
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Create a file menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    # Add a command to plot the voltage vs current data
    file_menu.add_command(label="Plot From Excel", command=Graph_from_Excel)
    # Add a command to save the output to a file
    file_menu.add_command(label="Save Output", command=save_to_file)

    # Create label and entry for the I_H value
    I_H_label = tk.Label(root, text="I_H (microamps)", bg='black', fg='SpringGreen2')
    I_H_label.grid(row=0, column=0)
    I_H_entry = tk.Entry(root)
    I_H_entry.grid(row=0, column=1)

    # Create label and entry for the Ron_H value
    Ron_H_label = tk.Label(root, text="Ron_H ", bg='black', fg='firebrick1')
    Ron_H_label.grid(row=1, column=0)
    Ron_H_entry = tk.Entry(root)
    Ron_H_entry.grid(row=1, column=1)

    # Create label and entry for the I_P value
    I_P_label = tk.Label(root, text="I_P (microamps)", bg='black', fg='SpringGreen2')
    I_P_label.grid(row=2, column=0)
    I_P_entry = tk.Entry(root)
    I_P_entry.grid(row=2, column=1)

    # Create label and entry for the Ron_P value
    Ron_P_label = tk.Label(root, text="Ron_P", bg='black', fg='firebrick1')
    Ron_P_label.grid(row=3, column=0)
    Ron_P_entry = tk.Entry(root)
    Ron_P_entry.grid(row=3, column=1)

    # Create label and entry for the time value
    time_label = tk.Label(root, text="Time (seconds)", bg='black', fg='snow')
    time_label.grid(row=4, column=0)
    time_entry = tk.Entry(root)
    time_entry.grid(row=4, column=1)

    # Create label and entry for the width value
    width_label = tk.Label(root, text="Width (microns)", bg='black', fg='IndianRed1')
    width_label.grid(row=5, column=0)
    width_entry = tk.Entry(root)
    width_entry.grid(row=5, column=1)

    # Create label and entry for the filament order value
    filament_order_label = tk.Label(root, text="Filament Order", bg='black', fg='snow')
    filament_order_label.grid(row=6, column=0)
    filament_order_entry = tk.Entry(root)
    filament_order_entry.grid(row=6, column=1)

    # Create a BooleanVar to hold the state of the checkbox
    Platinum_electrode = BooleanVar()
    Copper_electrode = BooleanVar()
    
    # Create a label and checkbutton for the Platinum electrode
    Platinum_electrode_label = tk.Label(root, text="Platinum Electrode", bg='black', fg='azure4')
    Platinum_electrode_label.grid(row=7, column=0)
    Platinum_electrode_checkbutton = tk.Checkbutton(root, variable=Platinum_electrode, bg='black', fg='blue')
    Platinum_electrode_checkbutton.grid(row=7, column=1)

    # Create a label and checkbutton for the Copper electrode
    Copper_electrode_label = tk.Label(root, text="Copper Electrode", bg='black', fg='DarkOrange2')
    Copper_electrode_label.grid(row=8, column=0)
    Copper_electrode_checkbutton = tk.Checkbutton(root, variable=Copper_electrode, bg='black', fg='blue')
    Copper_electrode_checkbutton.grid(row=8, column=1)

    # Create a button to calculate the DeltaT
    calculate_button = tk.Button(root, text="Calculate DeltaT", command=QJH_calc, bg='black', fg='cyan2')
    calculate_button.grid(row=9, column=0)

    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()