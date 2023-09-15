import matplotlib.pyplot as plt
import csv
import numpy as np

# Initialize lists to hold the CSV data
num_users = []
avg_latency_traditional = []
avg_latency_hybrid = []
avg_gas_traditional = []
avg_gas_hybrid = []

# Read data from the CSV file
with open('../csv/latency_and_gas_penalty.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        num_users.append(int(row[0]))
        avg_latency_traditional.append(float(row[1]))
        avg_latency_hybrid.append(float(row[2]))
        avg_gas_traditional.append(float(row[3]))
        avg_gas_hybrid.append(float(row[4]))

# Convert lists to NumPy arrays for plotting
num_users = np.array(num_users)
avg_latency_traditional = np.array(avg_latency_traditional)
avg_latency_hybrid = np.array(avg_latency_hybrid)
avg_gas_traditional = np.array(avg_gas_traditional)
avg_gas_hybrid = np.array(avg_gas_hybrid)

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

# First y-axis for latency
ax1.set_xlabel('Number of Users')
ax1.set_ylabel('Avg Latency (ms)')
ax1.plot(num_users, avg_latency_traditional, 'bo-', label="Average Latency Using Linear Model (ms)", marker='o', color='#6baed6')
ax1.plot(num_users, avg_latency_hybrid, 'rx-', label="Average Latency Using Quadratic-History Hybrid Model (ms)", marker='x', color='#fc9272')
ax1.legend(loc='upper center')

# Second y-axis for gas
ax2 = ax1.twinx()
ax2.set_ylabel('Avg Gas (Gwei)')
ax2.plot(num_users, avg_gas_traditional, 'bo--', label="Average Gas Consumption Using Linear Model (Gwei)", marker='s', color='#6baed6')
ax2.plot(num_users, avg_gas_hybrid, 'rx--', label="Average Gas Consumption Using Quadratic-History Hybrid Model (Gwei)", marker='^', color='#fc9272')
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 0.9))



#plt.title('Comparison of Latency and Gas Costs')
plt.tight_layout()
plt.savefig('Comparison of Latency and Gas Costs for penalties.png', format='png', dpi=300)
plt.show()
