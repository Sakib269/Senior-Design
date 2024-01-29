# Parse Excel Data and determine the QJh value for each data point
# QJh = (Vreset^3 * Icc) / (3 * RR * C)
# Determine Vreset from Data
# Pass Excel file name and Compliance current as arguments
# def determine_QJh(file_name, Icc):
# Open Excel file
import numpy as np
import math
import matplotlib.pyplot as plt
import openpyxl
def QJH_calc():
    # Open Excel file
    # file_name = 'data.xlsx'
    file_name = 'data.xlsx'
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
    F_dissipation = float(input("Enter the fraction of heat dissipated by convection and thermal radiation as a decimal: "))
    Icc = float(input("Enter the compliance current in uA: "))
    Icc = -(Icc * 10**(-6))
    RR = .276
    C = .29
    Qjh = ((reset_voltage**3 * Icc) / (3 * RR * C)) * (1 - F_dissipation)
    Qjh = round(Qjh * 10**6, 2)
    print("The reset voltage is: " + str(reset_voltage) + " volts")
    print("Qjh is: " + str(Qjh) + " micro Joules")

    # Plot the data
    # Create a figure and axis
    fig, ax = plt.subplots()
    # Plot voltage vs current
    ax.plot(voltage, current)
    # Set title and labels for axes
    ax.set(xlabel='Voltage (V)', ylabel='Current (uA)', title='Voltage vs Current')
    # ax.grid()
    plt.show()

if __name__ == "__main__":
    QJH_calc()