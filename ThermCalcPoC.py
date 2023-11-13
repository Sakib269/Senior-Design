    import sys
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

    class TemperatureChangeCalculator(QWidget):
        def __init__(self):
            super().__init__()
            self.density_copper = 8.96  # g/cm^3
            self.initUI()

        def initUI(self):
            # Main layout
            layout = QVBoxLayout()

            # Specific heat capacity input
            self.specific_heat_capacity_input = QLineEdit(self)
            layout.addWidget(QLabel('Enter the specific heat capacity in J/g°C:'))
            layout.addWidget(self.specific_heat_capacity_input)

            # Rectangular prisms inputs
            self.length_inputs = []
            self.width_inputs = []
            self.height_inputs = []
            for i in range(1, 4):
                layout.addWidget(QLabel(f'Rectangular prism {i} dimensions in cm (length, width, height):'))
                h_layout = QHBoxLayout()
                
                length_input = QLineEdit(self)
                self.length_inputs.append(length_input)
                h_layout.addWidget(length_input)

                width_input = QLineEdit(self)
                self.width_inputs.append(width_input)
                h_layout.addWidget(width_input)

                height_input = QLineEdit(self)
                self.height_inputs.append(height_input)
                h_layout.addWidget(height_input)

                layout.addLayout(h_layout)

            # Cylinder inputs
            self.radius_input = QLineEdit(self)
            layout.addWidget(QLabel('Enter the radius of the cylinder in cm:'))
            layout.addWidget(self.radius_input)

            self.height_cyl_input = QLineEdit(self)
            layout.addWidget(QLabel('Enter the height of the cylinder in cm:'))
            layout.addWidget(self.height_cyl_input)

            # Energy input
            self.energy_input = QLineEdit(self)
            layout.addWidget(QLabel('Enter the energy in Joules:'))
            layout.addWidget(self.energy_input)

            # Calculate button
            self.calculate_button = QPushButton('Calculate', self)
            self.calculate_button.clicked.connect(self.calculateTemperatureChange)
            layout.addWidget(self.calculate_button)

            # Result display
            self.result_label = QLabel('')
            layout.addWidget(self.result_label)

            # Set layout
            self.setLayout(layout)
            self.setWindowTitle('Temperature Change Calculator')

        def calculateTemperatureChange(self):
            try:
                specific_heat_capacity = float(self.specific_heat_capacity_input.text())

                # Rectangular prisms
                masses = []
                for length_input, width_input, height_input in zip(self.length_inputs, self.width_inputs, self.height_inputs):
                    length = float(length_input.text())
                    width = float(width_input.text())
                    height = float(height_input.text())
                    volume = length * width * height
                    mass = volume * self.density_copper
                    masses.append(mass)

                # Cylinder
                radius = float(self.radius_input.text())
                height_cyl = float(self.height_cyl_input.text())
                volume_cyl = 3.14159 * radius**2 * height_cyl
                mass_cyl = volume_cyl * self.density_copper
                masses.append(mass_cyl)

                # Energy
                energy = float(self.energy_input.text())

                # Calculate temperature change
                total_mass = sum(masses)
                temperature_change = energy / (total_mass * specific_heat_capacity)

                self.result_label.setText(f"The change in temperature is {temperature_change:.2f} Celsius.")
            except ValueError:
                self.result_label.setText("Invalid input. Please enter numerical values.")

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = TemperatureChangeCalculator()
        ex.show()
        sys.exit(app.exec_())
