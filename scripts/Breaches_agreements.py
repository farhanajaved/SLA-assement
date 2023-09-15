from brownie import AgreementsContract, accounts, web3
import matplotlib.pyplot as plt
import matplotlib
import random
import time

matplotlib.use('Agg')

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

    # Plotting
    plt.figure(figsize=(30, 6))

    # Cumulative Penalty
    plt.subplot(1, 5, 1)
    plt.plot(range(1, 51), penalties, 'o-', color='blue')
    plt.title("Cumulative Penalty vs. Breach Severity")
    plt.xlabel("Breach Number")
    plt.ylabel("Cumulative Penalty")

    # Gas used
    plt.subplot(1, 5, 2)
    plt.plot(range(1, 51), gas_used_list, 'o-', color='red')
    plt.title("Gas Used per Breach Report")
    plt.xlabel("Breach Number")
    plt.ylabel("Gas Used (in units)")

    # Latency
    plt.subplot(1, 5, 3)
    plt.plot(range(1, 51), latencies, 'o-', color='green')
    plt.title("Latency per Breach Report")
    plt.xlabel("Breach Number")
    plt.ylabel("Latency (in seconds)")

    # Transaction Cost in Wei
    plt.subplot(1, 5, 4)
    plt.plot(range(1, 51), tx_costs, 'o-', color='purple')
    plt.title("Transaction Cost per Breach Report (in Wei)")
    plt.xlabel("Breach Number")
    plt.ylabel("Transaction Cost (in Wei)")

    # Transaction Cost in ETH
    plt.subplot(1, 5, 5)
    plt.plot(range(1, 51), tx_costs_eth_list, 'o-', color='cyan')
    plt.title("Transaction Cost per Breach Report (in ETH)")
    plt.xlabel("Breach Number")
    plt.ylabel("Transaction Cost (in ETH)")

    plt.tight_layout()
    plt.savefig('analytics_plot.png')
    plt.close()
