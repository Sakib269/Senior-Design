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
    global output_text
    global Ron_H_entry
    global I_H_entry
    global I_P_entry
    global Ron_P_entry
    global time_entry
    global DeltaQ
    global width_entry
    global filament_order_entry
    global eletrode_material
    global K
    # Constants
    # electrode distance in microns
    electrode_distance = 150 * (10**-6) # 150 um to meters
    # Density of copper in g/cm^3
    copper_density = 8.96
    # Specific heat of copper in J/gC        
    specific_heat_copper = 0.385
    # Thermal conductivity of copper in W/mC or W/mK
    thermal_conductivity_copper = 385
    # specific heat capacity of platinum in J/gC
    specific_heat_platinum = 0.134
    # density of platinum in g/cm^3
    platinum_density = 21.45
    # Thermal conductivity of platinum in W/mC or W/mK
    thermal_conductivity_platinum = 69.1
    # specific heat capacity of Silcon Dioxide in J/gC
    specific_heat_silicon_dioxide = 0.703
    # density of silicon dioxide in g/cm^3
    silicon_dioxide_density = 8.2

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
    
    # Clear the text widget
    output_text.delete(1.0, tk.END)

    # round the values to 2 decimal places
    Q_h = round(Q_h, 5)
    Q_p = round(Q_p, 5)
    DeltaQ = round(DeltaQ, 5)
    DeltaT = round(DeltaT, 2)
    # Concatenate all the strings
    output_text_str = (
        "The calculated Q_h is: " + str(Q_h) + "\n" +
        "The calculated Q_p is: " + str(Q_p) + "\n" +
        "The calculated DeltaQ is: " + str(DeltaQ) + "\n" +
        "The selected material is: " + str(eletrode_material) + "\n" +
        "DeltaT: " + str(DeltaT) + "\n" 
        )
    
    # Insert the result into the text widget
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output_text_str)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("GUI")
    root.configure(bg='gray14')

    # Create label and entry for the I_H value
    I_H_label = tk.Label(root, text="I_H (microamps)", bg='gray14', fg='SpringGreen2')
    I_H_label.grid(row=0, column=0)
    I_H_entry = tk.Entry(root)
    I_H_entry.grid(row=0, column=1)

    # Create label and entry for the Ron_H value
    Ron_H_label = tk.Label(root, text="Ron_H ", bg='gray14', fg='SpringGreen2')
    Ron_H_label.grid(row=1, column=0)
    Ron_H_entry = tk.Entry(root)
    Ron_H_entry.grid(row=1, column=1)

    # Create label and entry for the I_P value
    I_P_label = tk.Label(root, text="I_P (microamps)", bg='gray14', fg='SpringGreen2')
    I_P_label.grid(row=2, column=0)
    I_P_entry = tk.Entry(root)
    I_P_entry.grid(row=2, column=1)

    # Create label and entry for the Ron_P value
    Ron_P_label = tk.Label(root, text="Ron_P", bg='gray14', fg='SpringGreen2')
    Ron_P_label.grid(row=3, column=0)
    Ron_P_entry = tk.Entry(root)
    Ron_P_entry.grid(row=3, column=1)

    # Create label and entry for the time value
    time_label = tk.Label(root, text="Time (seconds)", bg='gray14', fg='SpringGreen2')
    time_label.grid(row=4, column=0)
    time_entry = tk.Entry(root)
    time_entry.grid(row=4, column=1)

    # Create label and entry for the width value
    width_label = tk.Label(root, text="Width (microns)", bg='gray14', fg='SpringGreen2')
    width_label.grid(row=5, column=0)
    width_entry = tk.Entry(root)
    width_entry.grid(row=5, column=1)

    # Create label and entry for the filament order value
    filament_order_label = tk.Label(root, text="Filament Order", bg='gray14', fg='SpringGreen2')
    filament_order_label.grid(row=6, column=0)
    filament_order_entry = tk.Entry(root)
    filament_order_entry.grid(row=6, column=1)

    # Create a BooleanVar to hold the state of the checkbox
    Platinum_electrode = BooleanVar()
    Copper_electrode = BooleanVar()
    
    # Create a label and checkbutton for the Platinum electrode
    Platinum_electrode_label = tk.Label(root, text="Platinum Electrode", bg='gray14', fg='SpringGreen2')
    Platinum_electrode_label.grid(row=7, column=0)
    Platinum_electrode_checkbutton = tk.Checkbutton(root, variable=Platinum_electrode, bg='gray14', fg='blue')
    Platinum_electrode_checkbutton.grid(row=7, column=1)

    # Create a label and checkbutton for the Copper electrode
    Copper_electrode_label = tk.Label(root, text="Copper Electrode", bg='gray14', fg='SpringGreen2')
    Copper_electrode_label.grid(row=8, column=0)
    Copper_electrode_checkbutton = tk.Checkbutton(root, variable=Copper_electrode, bg='gray14', fg='blue')
    Copper_electrode_checkbutton.grid(row=8, column=1)

    # Create a button to calculate the DeltaT
    calculate_button = tk.Button(root, text="Calculate DeltaT", command=QJH_calc, bg='gray14', fg='SpringGreen2')
    calculate_button.grid(row=9, column=0)

    # Create a text widget to display the output
    output_text = tk.Text(root, width=50, height=15, wrap=tk.WORD, bg='gray14', fg='SpringGreen2')
    output_text.grid(row=10, column=0, columnspan=2)

    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()