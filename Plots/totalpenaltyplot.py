import matplotlib.pyplot as plt
import csv
import numpy as np

# Initialize lists to hold the CSV data
num_breaches = []
total_penalty_traditional = []
total_penalty_hybrid = []
total_gas_traditional = []
total_gas_hybrid = []

# Read data from the CSV file
with open('../csv/total_penalty_and_gas.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        num_breaches.append(int(row[0]))
        total_penalty_traditional.append(float(row[1]))
        total_penalty_hybrid.append(float(row[2]))
        total_gas_traditional.append(float(row[3]))
        total_gas_hybrid.append(float(row[4]))

# Convert lists to NumPy arrays for plotting
num_breaches = np.array(num_breaches)
total_penalty_traditional = np.array(total_penalty_traditional)
total_penalty_hybrid = np.array(total_penalty_hybrid)
total_gas_traditional = np.array(total_gas_traditional)
total_gas_hybrid = np.array(total_gas_hybrid)

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

# First y-axis for total penalty
ax1.set_xlabel('Number of Breaches')
ax1.set_ylabel('Total Penalty in ETH')
ax1.plot(num_breaches, total_penalty_traditional, 'bo-', label="Total Penalty Using Linear Model", marker='o', color='#6baed6')
ax1.plot(num_breaches, total_penalty_hybrid, 'rx-', label="Total Penalty Using Quadratic-History Hybrid Model", marker='x', color='#fc9272')
ax1.legend(loc='upper left')

# Second y-axis for total gas
ax2 = ax1.twinx()
ax2.set_ylabel('Total Gas (Gwei)')
ax2.plot(num_breaches, total_gas_traditional, 'bo--', label="Gas Consumption Using Linear Model", marker='s', color='#6baed6')
ax2.plot(num_breaches, total_gas_hybrid, 'rx--', label="Gas Consumption Using Quadratic-History Hybrid Model", marker='^', color='#fc9272')
ax2.legend(loc='upper left', bbox_to_anchor=(0, 0.9))

#plt.title('Comparison of Total Penalty and Total Gas vs total nu')
plt.tight_layout()
plt.savefig('Comparison of total penalty and Gas Costs for penalties.png', format='png', dpi=300)

plt.show()
