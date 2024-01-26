import math

def calculate_mass():
    # Density of copper in g/cm^3
    copper_density = 8.96
    # Specific heat of copper in J/gC
    specific_heat_copper = 0.385
    #specific heat capacity of platinum in J/gC
    specific_heat_platinum = 0.133

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
    pad_volume = ((100 * 10**(-4))**2) * (150 * 10**(-7))
    pad_mass = pad_volume * copper_density
    
    # Calculate mass of copper electrode in grams
    # 800um  >> 0.08 cm
    volume_copper_electrode = .08 * (10 * 10**(-4)) * (150 * 10**(-7))
    mass_copper_electrode = volume_copper_electrode * copper_density
    total_mass = ( 2 * mass_filament) + (2* pad_mass) + mass_copper_electrode
   
    # Testing value for Qjh is 10uJ
    Qjh = 10 * 10**(-6)
    tempC = (Qjh / (total_mass * specific_heat_copper))

    print("The temperature change of the filament is: " + str(tempC) + " degrees C")
    

    
if __name__ == "__main__":
    calculate_mass()