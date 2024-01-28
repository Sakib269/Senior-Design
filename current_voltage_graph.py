import matplotlib.pyplot as plt
import numpy as np

Vres = np.linspace(-3.0, -0.4, 5)
# temp values used to find a Qjh value
print("Enter absolute values for for a Reset Scenario")
Vres_t = ( input("Enter Vreset value in volts: "))
Icc_t = (input("Enter Icc value in microamps: "))
Vres_t = -float(Vres_t)
Icc_t = -(float(Icc_t) * 10**(-6))

RR = 0.276
C = 0.29
points = 5

# calculates JH
JH = ((Vres_t**3) * (Icc_t) ) / (3 * RR * C)

# calculates Icc
Icc = ((JH * 3 * RR * C) / (Vres**3))

# Plotting the graph
plt.plot(Vres, (Icc*10**6), marker='o')
Icc_t = round(Icc_t *10**6, 2)
JH = round(JH * 10**6, 2)
# Adding labels and title
plt.xlabel('Vres (V)')
plt.ylabel('Icc (uA)')
plt.title('Vres vs Icc @ ' + str(JH) + ' uJ, from Vres_t = ' + str(Vres_t) + ' V, Icc_t = ' + str(Icc_t) + ' uA')


# Displaying the plot
plt.grid(True)
plt.show()