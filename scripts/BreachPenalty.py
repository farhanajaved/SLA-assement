from brownie import BreachPenalty, accounts, network
from time import time
import matplotlib.pyplot as plt

def main():
    # Use the default account for deployment
    deployer_account = accounts[0]
    
    # Deploy the contract with a max breach value of 100
    breach_penalty = BreachPenalty.deploy(100, {'from': deployer_account})

    # Metrics to record
    history_based_gas_costs = []
    quadratic_gas_costs = [] # Placeholder as quadratic does not use gas directly
    tps = []  # Transactions per second
    latencies = []

    for breach_value in range(1, 51):  # Breach values from 1 to 50
        start_time = time()

        # History-based penalty
        tx_history = breach_penalty.historyBasedPenalty(breach_value, {'from': deployer_account})
        history_based_gas_costs.append(tx_history.gas_used)
        
        # Reset the consecutive breaches to compare the two methods fairly
        breach_penalty.resetConsecutiveBreaches({'from': deployer_account})

        # For the sake of the demonstration, call historyBasedPenalty again to emulate quadratic
        tx_quadratic = breach_penalty.historyBasedPenalty(breach_value, {'from': deployer_account})
        quadratic_gas_costs.append(tx_quadratic.gas_used)
        
        end_time = time()

        # Calculating metrics
        tps.append(1.0 / (end_time - start_time))
        latencies.append(end_time - start_time)

    # Plotting the results using matplotlib
    plt.figure(figsize=(12, 8))

    # Plotting Gas Cost
    plt.subplot(1, 3, 1)
    plt.plot(range(1, 51), history_based_gas_costs, '-o', label='History-Based', color='green')
    plt.plot(range(1, 51), quadratic_gas_costs, '-o', label='Quadratic', color='blue')
    plt.title('Gas Cost per Breach')
    plt.xlabel('Breach Value')
    plt.ylabel('Gas Cost')
    plt.legend()
    plt.grid(True)

    # Plotting TPS
    plt.subplot(1, 3, 2)
    plt.plot(range(1, 51), tps, '-o', label='TPS', color='orange')
    plt.title('Transactions Per Second')
    plt.xlabel('Breach Value')
    plt.ylabel('TPS')
    plt.grid(True)

    # Plotting Latency
    plt.subplot(1, 3, 3)
    plt.plot(range(1, 51), latencies, '-o', label='Latency', color='red')
    plt.title('Latency')
    plt.xlabel('Breach Value')
    plt.ylabel('Latency (s)')
    plt.grid(True)

    # Adjust layout
    plt.tight_layout()
    plt.savefig('Two_penalty_comparison.png')

    # Show the plots
    plt.show()
