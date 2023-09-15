import csv
import matplotlib.pyplot as plt

def plot_metrics_from_csv():
    all_data = {}
    with open('../csv/billing-tps-latency.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header
        for row in csvreader:
            function, num_users, latency, tps = row
            if function not in all_data:
                all_data[function] = {'x_users': [], 'y_latency': [], 'y_tps': []}
            all_data[function]['x_users'].append(int(num_users))
            all_data[function]['y_latency'].append(float(latency))
            all_data[function]['y_tps'].append(float(tps))
    return all_data

def plot_metrics(all_data):
    plt.figure(figsize=(10, 7))
    # Updated color and marker mappings
    color_marker_map = {
        "calculateTotalPenalty": ('#6baed6', 'o'),
        "transferFunds": ('#fc9272', 'x'),
        "requestFunds": ('#31a354', 's'),
    }

    for function_name, data in all_data.items():
        color, marker = color_marker_map.get(function_name, ('#000000', 'o'))
        x_users, y_latency, _ = data['x_users'], data['y_latency'], data['y_tps']

        plt.plot(x_users, y_latency, color=color, marker=marker, linestyle='-', linewidth=2, markersize=8, label=f"{function_name}")

    #plt.title("Latency Comparison", fontsize=16)
    plt.xlabel('Number of Users')
    plt.ylabel('Latency (seconds)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(loc='upper left', title='Functions')    
    plt.tight_layout()
    plt.savefig('latency_billing.png', format='png', dpi=300)
    plt.show()

    # Create a new figure for TPS
    plt.figure(figsize=(10, 7))

    for function_name, data in all_data.items():
        color, marker = color_marker_map.get(function_name, ('black', 'o'))
        x_users, _, y_tps = data['x_users'], data['y_latency'], data['y_tps']  # Corrected this line
        plt.plot(x_users, y_tps, color=color, marker=marker, linestyle='-', linewidth=2, markersize=8, label=f"{function_name}")
    
    #plt.title("TPS Comparison", fontsize=16)
    plt.xlabel('Number of Users')
    plt.ylabel('Transactions Per Second (TPS)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(loc='upper left', title='Functions')
    plt.tight_layout()
    plt.savefig('TPS_billing.png', format='png', dpi=300)
    plt.show()

if __name__ == "__main__":
    all_data = plot_metrics_from_csv()
    plot_metrics(all_data)