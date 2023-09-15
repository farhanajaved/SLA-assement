from brownie import AgreementsContract, accounts, web3
import matplotlib.pyplot as plt
import random
import time

def get_tiered_severity(breach_count):
    base_severity = (breach_count - 1) // 10 + 1
    random_factor = random.uniform(-0.5, 0.5)
    return base_severity + random_factor

def main():
    deployer = accounts[0]
    agreement_contract = AgreementsContract.deploy({'from': deployer})

    print(f"AgreementsContract deployed at: {agreement_contract.address}")
    
    agreement_contract.createAgreement(accounts[1], {'from': deployer})

    penalties = []
    gas_used_list = []
    latencies = []
    tx_costs = []  # in Wei
    tx_costs_eth_list = []  # in ETH
    cumulative_penalty = 0

    for i in range(1, 51):
        severity = get_tiered_severity(i)
        start_time = time.time()
        tx_receipt = agreement_contract.reportBreach(accounts[1], severity, {'from': deployer})
        end_time = time.time()
        
        latency = end_time - start_time
        latencies.append(latency)
        
        gas_used = tx_receipt.gas_used
        gas_used_list.append(gas_used)
        
        tx_cost = gas_used * web3.eth.gasPrice  # Calculate transaction cost in Wei
        tx_costs.append(tx_cost)
        
        tx_cost_eth = web3.fromWei(tx_cost, 'ether')  # Convert transaction cost to ETH
        tx_costs_eth_list.append(tx_cost_eth)
        
        breach_count = agreement_contract.getBreachCount(deployer, accounts[1])
        breach_data = agreement_contract.breachHistory(agreement_contract.createAgreementId(deployer, accounts[1]), breach_count - 1)
        penalty = breach_data[1]
        cumulative_penalty += penalty  # Update cumulative penalty
        penalties.append(cumulative_penalty)  # Use this for cumulative penalties

    avg_latency = sum(latencies) / len(latencies)
    print(f"Average Latency: {avg_latency:.2f} seconds")

    # Plotting using matplotlib
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # Cumulative Penalty vs. Breach Severity
    axs[0, 0].plot(range(1, 51), penalties, 'o-', color='blue')
    axs[0, 0].set_title("Cumulative Penalty vs. Breach Severity")
    axs[0, 0].set_xlabel("Breach Number")
    axs[0, 0].set_ylabel("Cumulative Penalty")

    # Gas Used per Breach Report
    axs[0, 1].plot(range(1, 51), gas_used_list, 'o-', color='red')
    axs[0, 1].set_title("Gas Used per Breach Report")
    axs[0, 1].set_xlabel("Breach Number")
    axs[0, 1].set_ylabel("Gas Used (in units)")

    # Latency per Breach Report
    axs[1, 0].plot(range(1, 51), latencies, 'o-', color='green')
    axs[1, 0].set_title("Latency per Breach Report")
    axs[1, 0].set_xlabel("Breach Number")
    axs[1, 0].set_ylabel("Latency (in seconds)")

    # Transaction Cost in ETH
    axs[1, 1].plot(range(1, 51), tx_costs_eth_list, 'o-', color='purple')
    axs[1, 1].set_title("Transaction Cost per Breach Report (in ETH)")
    axs[1, 1].set_xlabel("Breach Number")
    axs[1, 1].set_ylabel("Transaction Cost (in ETH)")

    plt.tight_layout()
    plt.savefig('analytics_plot.png')
    plt.show()

