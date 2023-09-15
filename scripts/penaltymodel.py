from brownie import accounts, TraditionalModel, HybridModel
import time
import matplotlib.pyplot as plt
import csv

def measure_function(contract, func_name, *args):
    start = time.time()
    tx = getattr(contract, func_name)(*args)
    gas = tx.gas_used
    end = time.time()
    latency = end - start
    return latency, gas

def main():
    deployer = accounts[0]
    num_users_range = range(2, 51)

    latency_traditional, gas_traditional, latency_hybrid, gas_hybrid = [], [], [], []
    
    # Open the CSV file before starting the for-loop
    with open('latency_and_gas.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Number of Users", "Avg Latency Traditional", "Avg Latency Hybrid", "Avg Gas Traditional", "Avg Gas Hybrid"])

        traditional_contract = TraditionalModel.deploy({'from': deployer})
        hybrid_contract = HybridModel.deploy({'from': deployer})

        for num_users in num_users_range:
            avg_latency_traditional, avg_gas_traditional = 0, 0
            avg_latency_hybrid, avg_gas_hybrid = 0, 0

            for user in accounts[1:num_users + 1]:
                breaches = 1  # you can randomize this
                latency, gas = measure_function(traditional_contract, "registerBreach", breaches, {'from': user})
                avg_latency_traditional += latency
                avg_gas_traditional += gas

                latency, gas = measure_function(hybrid_contract, "registerBreach", breaches, {'from': user})
                avg_latency_hybrid += latency
                avg_gas_hybrid += gas

            # Average the latencies and gas usage
            avg_latency_traditional /= num_users
            avg_latency_hybrid /= num_users
            avg_gas_traditional /= num_users
            avg_gas_hybrid /= num_users

            # Write the averaged data to the CSV file
            writer.writerow([num_users, avg_latency_traditional, avg_latency_hybrid, avg_gas_traditional, avg_gas_hybrid])
