from brownie import Marketplace, accounts
import random
import string
import time
import matplotlib.pyplot as plt
import csv

def random_string(length=5):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def random_digit(length=3):
    return ''.join(random.choice(string.digits) for _ in range(length))

def main():
    # Confirm the total number of available accounts
    print(f"Total accounts: {len(accounts)}")

    # Deploying the contract
    account = accounts[0]
    marketplace = Marketplace.deploy({'from': account})

    # Lists to store gas costs and latencies
    registration_gas_costs = []
    service_addition_gas_costs = []
    service_selection_gas_costs = []

    registration_latencies = []
    service_addition_latencies = []
    service_selection_latencies = []

    registration_tps = []
    service_addition_tps = []
    service_selection_tps = []

    last_registered_index = 0

    for num_users in range(2, 51):  # from 2 to 50 users
        users = accounts[1:num_users+1]
        print(f"For num_users = {num_users}, we have {len(users)} users.")
        
        reg_gas, serv_add_gas, serv_sel_gas = [], [], []
        reg_latency, serv_add_latency, serv_sel_latency = [], [], []

        # Register only the newly added users
        for i in range(last_registered_index, num_users):
            if i < len(users):
                user = users[i]
            else:
                print(f"Index i = {i} is out of range for users list.")
                continue

            providerProfile = random_string() + random_digit()
            consumerProfile = random_string() + random_digit()

            start_time = time.time()
            tx = marketplace.registerUser(providerProfile, consumerProfile, {'from': user})
            end_time = time.time()

            reg_gas.append(tx.gas_used)
            reg_latency.append(end_time - start_time)

        last_registered_index = num_users

        # Add services for each user
        for user in users:
            for _ in range(5):
                service = random_string() + random_digit()
                try:
                    start_time = time.time()
                    tx = marketplace.addService(service, {'from': user})
                    end_time = time.time()

                    serv_add_gas.append(tx.gas_used)
                    serv_add_latency.append(end_time - start_time)
                except:
                    break

        # A random user selects a service from another random user
        consumer = random.choice(users)
        provider = random.choice(users)
        while provider == consumer:
            provider = random.choice(users)

        serviceIndex = random.randint(0, 4)
        start_time = time.time()
        tx = marketplace.selectService(provider, serviceIndex, {'from': consumer})
        end_time = time.time()

        serv_sel_gas.append(tx.gas_used)
        serv_sel_latency.append(end_time - start_time)

        # Append average gas costs and latencies
        registration_gas_costs.append(sum(reg_gas) / len(reg_gas))
        service_addition_gas_costs.append(sum(serv_add_gas) / len(serv_add_gas))
        service_selection_gas_costs.append(sum(serv_sel_gas) / len(serv_sel_gas))

        registration_latencies.append(sum(reg_latency) / len(reg_latency))
        service_addition_latencies.append(sum(serv_add_latency) / len(serv_add_latency))
        service_selection_latencies.append(sum(serv_sel_latency) / len(serv_sel_latency))


# Calculate TPS (Transactions Per Second) from latency.
    # We assume that each latency measurement corresponds to one transaction,
    # so TPS is simply 1 / latency for each operation type.
    for reg_latency, add_latency, sel_latency in zip(registration_latencies, service_addition_latencies, service_selection_latencies):
        registration_tps.append(1 / reg_latency if reg_latency > 0 else 0)
        service_addition_tps.append(1 / add_latency if add_latency > 0 else 0)
        service_selection_tps.append(1 / sel_latency if sel_latency > 0 else 0)

# Create or open a CSV file for writing
    with open("creation-late-tps.csv", "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write the header
        csvwriter.writerow([
            "Number of Users",
            "Average Registration Gas",
            "Average Service Addition Gas",
            "Average Service Selection Gas",
            "Average Registration Latency",
            "Average Service Addition Latency",
            "Average Service Selection Latency",
            "Registration TPS",
            "Service Addition TPS",
            "Service Selection TPS"
        ])

        # Write the data
        for i in range(len(registration_gas_costs)):
            csvwriter.writerow([
                i + 2,  # Number of Users starts from 2
                registration_gas_costs[i],
                service_addition_gas_costs[i],
                service_selection_gas_costs[i],
                registration_latencies[i],
                service_addition_latencies[i],
                service_selection_latencies[i],
                registration_tps[i],
                service_addition_tps[i],
                service_selection_tps[i]
            ])
    # Rest of your plotting code remains the same


    # Plotting gas usage
    fig1, ax1 = plt.subplots(figsize=(15, 7))
    x = list(range(2, 51))
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
    plt.savefig("gas_usage_comparison.png")
    plt.show()

    # Plotting latencies
    fig2, ax2 = plt.subplots(figsize=(8, 7))
    max_latency = max(max(registration_latencies), max(service_addition_latencies), max(service_selection_latencies))
    ax2.set_ylim([0, max_latency + max_latency*0.1])
    ax2.plot(x, registration_latencies, label="Registration Latency", color='blue', marker='o')
    ax2.plot(x, service_addition_latencies, label="Service Addition Latency", color='green', marker='s')
    ax2.plot(x, service_selection_latencies, label="Service Selection Latency", color='red', marker='^')
    ax2.set_title("Latency Comparison for Different Operations")
    ax2.set_xlabel("Number of Users")
    ax2.set_ylabel("Latency (seconds)")
    ax2.legend(loc="upper left")
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("latency_comparison.png")
    plt.show()

# New code to plot TPS
    fig3, ax3 = plt.subplots(figsize=(8, 7))
    max_tps = max(max(registration_tps), max(service_addition_tps), max(service_selection_tps))
    ax3.set_ylim([0, max_tps + max_tps*0.1])
    ax3.plot(x, registration_tps, label="Registration TPS", color='blue', marker='o')
    ax3.plot(x, service_addition_tps, label="Service Addition TPS", color='green', marker='s')
    ax3.plot(x, service_selection_tps, label="Service Selection TPS", color='red', marker='^')
    ax3.set_title("Transactions Per Second (TPS) Comparison for Different Operations")
    ax3.set_xlabel("Number of Users")
    ax3.set_ylabel("TPS")
    ax3.legend(loc="upper left")
    ax3.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("tps_comparison.png")
    plt.show()