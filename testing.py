import math

def calculate_deltaT():
    # Density of copper in g/cm^3
    copper_density = 8.96
    # Specific heat of copper in J/gC        
    specific_heat_copper = 0.385
    # specific heat capacity of platinum in J/gC
    specific_heat_platinum = 0.134
    # density of platinum in g/cm^3
    platinum_density = 21.45
    # specific heat capacity of Silcon Dioxide in J/gC
    specific_heat_silicon_dioxide = 0.703
    # density of silicon dioxide in g/cm^3
    silicon_dioxide_density = 8.2

    #The radii of the filament in nanometers can be user defined. Currently hard coded as the 10-25 filament
    # dimensions of the truncated cone in nanometers >> centimeters
    r1 = 12.5 * 10**(-7)
    r2 = 5 * 10**(-7)
    h = 25 * 10**(-7)

    # Calculate volume of truncated cone in nm^3
    # R1 is the radius of the larger base        
    # R2 is the radius of the smaller base
    volume_filament = (1/3) * math.pi * h * (r1**2 + r2**2 + r1*r2)

    # Calculate filament mass in grams
    mass_filament = volume_filament * copper_density

    # Copper electrode consists of a single rectangle prism with two pads on the end
    # Copper layer is 150 nm thick
    # Pad is 100um by 100um
    # convert to cm
    #               100um = 100 * 10**(-4) cm, 150nm = 150 * 10**(-7) cm
    copper_pad_volume = ((100 * 10**(-4))**2) * (150 * 10**(-7))
    copper_pad_mass = copper_pad_volume * copper_density
    # Calculate mass of copper electrode in grams
    # 800um  >> 0.08 cm
    volume_copper_electrode = .08 * (10 * 10**(-4)) * (150 * 10**(-7))
    mass_copper_electrode = volume_copper_electrode * copper_density
    total_mass_copper = ( 2 * mass_filament) + (2* copper_pad_mass) + mass_copper_electrode

    # Platinum electrode consists of a single rectangle prism with two pads on the end
    # Platinum layer is 50 nm thick
    # Pad is 100um by 100um
    plat_pad_volume = ((100 * 10**(-4))**2) * (50 * 10**(-7))
    plat_pad_mass = plat_pad_volume * platinum_density
    # Calculate mass of platinum electrode in grams
    volume_platinum_electrode = .08 * (10 * 10**(-4)) * (50 * 10**(-7))
    mass_platinum_electrode = volume_platinum_electrode * platinum_density
    total_mass_platinum = mass_platinum_electrode + (2 * plat_pad_mass)

    # silicon dioxide layer is 25 nm thick
    # silicon dioxide is a single sheet 
    # Calculate mass of silicon dioxide in grams
    # Oxide is 1030um by 750um
    volume_silicon_dioxide = (1030 * 10**(-4)) * (750 * 10**(-4)) * (25 * 10**(-7))
    mass_silicon_dioxide = volume_silicon_dioxide * silicon_dioxide_density
    
    Qjh = float(input("Enter the Qjh value in microJoules: "))
    Qjh = Qjh * 10**(-6)
    tempCopper = round((Qjh / (total_mass_copper * specific_heat_copper)), 2)
    tempPlatinum = round((Qjh / (total_mass_platinum * specific_heat_platinum)), 2)
    tempSiliconDioxide = round((Qjh / (mass_silicon_dioxide * specific_heat_silicon_dioxide)), 2)
        

    Qjh = round(Qjh * 10**6, 2)
    # DISPLAY THESE RESULTS IN GUI
    print("Qjh is: " + str(Qjh) + " micro Joules")
    print("Accounting for heat removed by convection and thermal radiation, the maxiumum change in temperature the unheated filament and the copper electrode could experience is : " + str(tempCopper) + " degrees C")
    print("The platinum electrode could experience a maximum change in temperature of: " + str(tempPlatinum) + " degrees C")
    print("The Silicon Dioxide layer could experience a maximum change in temperature of: " + str(tempSiliconDioxide) + " degrees C")
    
if __name__ == "__main__":
    calculate_deltaT()