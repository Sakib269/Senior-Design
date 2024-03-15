import math

def calculate_deltaT():
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
    # Calculate the Qjh from the new equation
    # Qjh = Q_h + Q_p
    # Get inputs for the heated probe current and the Ron value
    I_H = float(input("Enter the heated probe current in microamps: "))
    # convert from microamps to amps
    I_H = I_H * 10**-6
    Ron_H = float(input("Enter the Ron value for heated probe in miliamps: "))
    # Get inputs from probing cell
    I_P = float(input("Enter the probing cell current: "))
    # convert from milliamps to amps
    I_P = I_P * 10**-6
    Ron_P = float(input("Enter the Ron value for probing cell: "))
    # Get time in seconds
    time = float(input("Enter time in seconds: "))
    # Calculate the Q_h
    Q_h = (I_H**2) * Ron_H * time
    print("The calculated Q_h is: ", Q_h)
    # Calculate the Q_p
    Q_p = (I_P**2) * Ron_P * time
    print("The calculated Q_p is: ", Q_p)
    # Calculate the DeltaQ
    DeltaQ = Q_h + Q_p
    print("The calculated DeltaQ is: ", DeltaQ)
    # Get electrode width
    width = float(input("Enter electrode width: "))
    # Ask for the material of the electrode
    electrode_material = input("Enter the material of the electrode (Platinum or Copper): ")
    # Choose K from boolean variables based on the user selection
    if electrode_material.lower() == "platinum":
        K = thermal_conductivity_platinum
        Across = (width * 10**-6) * (50 * 10**-9) # use meters
    elif electrode_material.lower() == "copper":
        K = thermal_conductivity_copper
        Across = (width * 10**-6) * (150 * 10**-9) # use meters
    else:
        print("Invalid material entered. Please enter either 'Platinum' or 'Copper'.")
        return
    print ("The selected K is: ", K)
    print ("The selected Across is: ", Across)
    # Get electrode width
    width = float(input("Enter electrode width: "))
    # convert width from microns to meters
    width = width * 10**-6
    print ("The selected width is: ", width)
    # Get the order of the filament
    filament_order = float(input("Enter the order of the filament: "))
    distance = (width + electrode_distance) * filament_order
    DeltaT = (DeltaQ * distance) / (K * Across * time)
    #convert distance from meters to microns
    distance = distance * 10**6
    print("The calculated distance is: ", distance)
    print("The calculated DeltaT is: ", DeltaT)


    
if __name__ == "__main__":
    calculate_deltaT()