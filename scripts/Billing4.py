from brownie import Penalty, Billing, accounts
import time
import matplotlib.pyplot as plt
import csv

def benchmark_calculateTotalPenalty(billing, deployer, num_users):
    start_time = time.time()
    for user in accounts[1:num_users + 1]:
        billing.calculateTotalPenalty(user, {'from': deployer})
    end_time = time.time()
    return (end_time - start_time) / num_users, num_users / (end_time - start_time)

def benchmark_transferFunds(billing, deployer, num_users):
    start_time = time.time()
    for user in accounts[1:num_users + 1]:
        billing.transferFunds(deployer, user, 1000, {'from': deployer})
    end_time = time.time()
    return (end_time - start_time) / num_users, num_users / (end_time - start_time)

def benchmark_requestFunds(billing, deployer, num_users):
    start_time = time.time()
    for user in accounts[1:num_users + 1]:
        billing.requestFunds(user, 1000, {'from': deployer})
    end_time = time.time()
    return (end_time - start_time) / num_users, num_users / (end_time - start_time)

# Generate CSV file
    with open('benchmark_data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write header
        csvwriter.writerow(['Function', 'Num_Users', 'Latency(s)', 'TPS'])
        
        for function_name, data in all_data.items():
            x_users, y_latency, y_tps = data
            for i in range(len(x_users)):
                csvwriter.writerow([function_name, x_users[i], y_latency[i], y_tps[i]])


def plot_metrics(all_data):
    # Create a new figure for Latency
    plt.figure(figsize=(10, 7))

    color_marker_map = {
        "calculateTotalPenalty": ('blue', 'o'),
        "transferFunds": ('green', 'x'),
        "requestFunds": ('red', 's'),
    }

    for function_name, data in all_data.items():
        color, marker = color_marker_map.get(function_name, ('black', 'o'))
        x_users, y_latency, _ = data
        plt.plot(x_users, y_latency, color=color, marker=marker, linestyle='-', linewidth=2, markersize=8, label=f"{function_name}")
    plt.title("Latency Comparison", fontsize=16)
    plt.xlabel('Number of Users', fontsize=14)
    plt.ylabel('Latency (s)', fontsize=14)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig('latency_billing.png', format='png', dpi=300)
    plt.show()

    # Create a new figure for TPS
    plt.figure(figsize=(10, 7))

    for function_name, data in all_data.items():
        color, marker = color_marker_map.get(function_name, ('black', 'o'))
        x_users, _, y_tps = data
        plt.plot(x_users, y_tps, color=color, marker=marker, linestyle='-', linewidth=2, markersize=8, label=f"{function_name}")
    plt.title("TPS Comparison", fontsize=16)
    plt.xlabel('Number of Users', fontsize=14)
    plt.ylabel('TPS', fontsize=14)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig('TPS_billing.png', format='png', dpi=300)
    plt.show()


def main():
    deployer = accounts[0]
    penalty = Penalty.deploy({'from': deployer})
    billing = Billing.deploy(penalty.address, {'from': deployer})

    all_data = {}
    for function_name, benchmark_function in [
        ("calculateTotalPenalty", benchmark_calculateTotalPenalty),
        ("transferFunds", benchmark_transferFunds),
        ("requestFunds", benchmark_requestFunds)
    ]:
        x_users = []
        y_latency = []
        y_tps = []
        for num_users in range(2, 51):
            x_users.append(num_users)
            latency, tps = benchmark_function(billing, deployer, num_users)
            y_latency.append(latency)
            y_tps.append(tps)
            print(f"{num_users} users: Latency = {latency} s, TPS = {tps}")

        all_data[function_name] = (x_users, y_latency, y_tps)

    # Generate CSV file (This part was moved into the main function)
    with open('billing-tps-latency.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write header
        csvwriter.writerow(['Function', 'Num_Users', 'Latency(s)', 'TPS'])
        
        for function_name, data in all_data.items():
            x_users, y_latency, y_tps = data
            for i in range(len(x_users)):
                csvwriter.writerow([function_name, x_users[i], y_latency[i], y_tps[i]])

    plot_metrics(all_data)

if __name__ == "__main__":
    main()
