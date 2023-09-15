import matplotlib.pyplot as plt
import csv

# Define color and marker mappings
color_marker_map = {
    "Registration": ('#6baed6', 'o'),
    "Service Addition": ('#fc9272', 'x'),
    "Service Selection": ('#31a354', 's'),
}

def plot_data_from_csv():
    registration_gas_costs = []
    service_addition_gas_costs = []
    service_selection_gas_costs = []
    registration_latencies = []
    service_addition_latencies = []
    service_selection_latencies = []
    registration_tps = []
    service_addition_tps = []
    service_selection_tps = []
    x = []

    with open("../csv/creation-late-tps.csv", 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)  # Skip the header row
        for row in csvreader:
            x.append(int(row[0]))
            registration_gas_costs.append(float(row[1]))
            service_addition_gas_costs.append(float(row[2]))
            service_selection_gas_costs.append(float(row[3]))
            registration_latencies.append(float(row[4]))
            service_addition_latencies.append(float(row[5]))
            service_selection_latencies.append(float(row[6]))
            registration_tps.append(float(row[7]))
            service_addition_tps.append(float(row[8]))
            service_selection_tps.append(float(row[9]))

    # Your plotting code here, similar to the plotting code in the original file.
    # For example:
    """""
    fig1, ax1 = plt.subplots(figsize=(15, 7))
    
    max_gas = max(max(registration_gas_costs), max(service_addition_gas_costs), max(service_selection_gas_costs))
    ax1.set_ylim([0, max_gas + max_gas*0.1])
    ax1.plot(x, registration_gas_costs, label="Registration", color='blue', marker='o')
    ax1.plot(x, service_addition_gas_costs, label="Service Addition", color='green', marker='s')
    ax1.plot(x, service_selection_gas_costs, label="Service Selection", color='red', marker='^')
    ax1.set_title("Gas Usage Comparison for Different Operations")
    ax1.set_xlabel("Number of Users")
    ax1.set_ylabel("Gas Used")
    ax1.legend(loc="upper left")
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("gas_usage_comparison_from_csv.png")
    plt.show()
    """
    # Plotting latencies
   # Plotting latencies
    fig2, ax2 = plt.subplots(figsize=(8, 7))
    max_latency = max(max(registration_latencies), max(service_addition_latencies), max(service_selection_latencies))
    ax2.set_ylim([0, max_latency + max_latency * 0.1])

    for name, latencies in [("Registration", registration_latencies), ("Service Addition", service_addition_latencies), ("Service Selection", service_selection_latencies)]:
        color, marker = color_marker_map.get(name, ('#000000', 'o'))
        ax2.plot(x, latencies, label=f"{name}", color=color, marker=marker, linestyle='-', linewidth=2, markersize=8)
    
   # ax2.set_title("Latency Comparison for Different Operations")
    ax2.set_xlabel("Number of Users")
    ax2.set_ylabel("Latency (seconds)")
    ax2.legend(loc='upper left', title='Functions')  
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("latency_comparison.png")
    plt.show()

# New code to plot TPS
    fig3, ax3 = plt.subplots(figsize=(8, 7))
    max_tps = max(max(registration_tps), max(service_addition_tps), max(service_selection_tps))
    ax3.set_ylim([0, max_tps + max_tps * 0.1])

    for name, tps in [("Registration", registration_tps), ("Service Addition", service_addition_tps), ("Service Selection", service_selection_tps)]:
        color, marker = color_marker_map.get(name, ('#000000', 'o'))
        ax3.plot(x, tps, label=name, color=color, marker=marker, linestyle='-', linewidth=2, markersize=8)

    #ax3.set_title("Transactions Per Second (TPS) Comparison for Different Operations")
    ax3.set_xlabel("Number of Users")
    ax3.set_ylabel("Transactions Per Second (TPS)")
    ax3.legend(loc='upper right', title='Functions')  
    ax3.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("tps_comparison.png")
    plt.show()

# Run the function
plot_data_from_csv()
