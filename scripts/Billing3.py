from brownie import Penalty, Billing, accounts
import time
import matplotlib.pyplot as plt

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

def plot_metrics(all_data):
    plt.figure(figsize=(15, 7))

    # Plot for Latency
    plt.subplot(1, 2, 1)
    for function_name, data in all_data.items():
        x_users, y_latency, _ = data  # Unpack all three elements here
        plt.plot(x_users, y_latency, marker='o', label=f"{function_name} Latency")
    plt.title("Latency Comparison for Smart Contract Functions")
    plt.xlabel('Number of Users')
    plt.ylabel('Latency (s)')
    plt.legend()

    # Plot for TPS
    plt.subplot(1, 2, 2)
    for function_name, data in all_data.items():
        x_users, _, y_tps = data  # Unpack all three elements here
        plt.plot(x_users, y_tps, marker='s', label=f"{function_name} TPS")
    plt.title("TPS Comparison for Smart Contract Functions")
    plt.xlabel('Number of Users')
    plt.ylabel('TPS')
    plt.legend()

    plt.tight_layout()
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
    
    plot_metrics(all_data)
