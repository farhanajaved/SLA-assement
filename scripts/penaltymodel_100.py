from brownie import accounts, TraditionalModel, HybridModel
import time
import csv

def measure_function(contract, func_name, *args):
    start = time.time()
    tx = getattr(contract, func_name)(*args)
    gas = tx.gas_used
    end = time.time()
    return gas

def main():
    deployer = accounts[0]
    max_breaches = 100

    gas_traditional, gas_hybrid = [], []
    total_penalty_traditional, total_penalty_hybrid = [], []

    with open('total_penalty_and_gas.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Number of Breaches", "Total Gas Traditional", "Total Gas Hybrid", "Total Penalty Traditional", "Total Penalty Hybrid"])

        traditional_contract = TraditionalModel.deploy({'from': deployer})
        hybrid_contract = HybridModel.deploy({'from': deployer})

        total_gas_traditional, total_gas_hybrid = 0, 0
        total_penalty_traditional_value, total_penalty_hybrid_value = 0, 0

        for breaches in range(1, max_breaches + 1):
            user = accounts[1]

            gas = measure_function(traditional_contract, "registerBreach", 1, {'from': user})
            total_gas_traditional += gas
            total_penalty_traditional_value += traditional_contract.calculatePenalty(user)

            gas = measure_function(hybrid_contract, "registerBreach", 1, {'from': user})
            total_gas_hybrid += gas
            total_penalty_hybrid_value += hybrid_contract.calculatePenalty(user)

            writer.writerow([breaches, total_gas_traditional, total_gas_hybrid, total_penalty_traditional_value, total_penalty_hybrid_value])

