# Constants
density_copper = 8.96  # g/cm^3
specific_heat_capacity = float(input("Enter the specific heat capacity in J/g°C: "))

# Rectangular prisms
masses = []
for i in range(1, 4):
    length = float(input(f"Enter the length of rectangular prism {i} in cm: "))
    width = float(input(f"Enter the width of rectangular prism {i} in cm: "))
    height = float(input(f"Enter the height of rectangular prism {i} in cm: "))
    volume = length * width * height
    mass = volume * density_copper
    masses.append(mass)

# Cylinder
radius = float(input("Enter the radius of the cylinder in cm: "))
height = float(input("Enter the height of the cylinder in cm: "))
volume = 3.14159 * radius**2 * height
mass = volume * density_copper
masses.append(mass)

# Energy
energy = float(input("Enter the energy in Joules: "))

# Calculate temperature change
total_mass = sum(masses)
temperature_change = energy / (total_mass * specific_heat_capacity)

print("The change in temperature is", temperature_change, "Celcius.")
