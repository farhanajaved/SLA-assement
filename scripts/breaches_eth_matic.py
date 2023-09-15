from brownie import AgreementsContract, accounts, web3
import matplotlib.pyplot as plt
import time
import random

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
    tx_costs_eth_list = []
    tx_costs_usd_eth_list = []
    tx_costs_matic_list = []
    tx_costs_usd_matic_list = []
    cumulative_penalty = 0

    ETH_TO_USD = 1853.76
    MATIC_TO_USD = 0.677816

    ETH_GAS_PRICE = 22e-9  # 22 Gwei
    MATIC_GAS_PRICE = 121.1e-9  # 121.1 Gwei

    print("Starting loop...")
    for i in range(1, 51):
        penalties.append(cumulative_penalty)
        print(f"Penalty for iteration {i}: {cumulative_penalty}")
        severity = get_tiered_severity(i)
        start_time = time.time()
        tx_receipt = agreement_contract.reportBreach(accounts[1], severity, {'from': deployer})
        end_time = time.time()

        latency = end_time - start_time
        latencies.append(latency)

        gas_used = tx_receipt.gas_used
        gas_used_list.append(gas_used)

        tx_cost_eth = gas_used * ETH_GAS_PRICE
        tx_costs_eth_list.append(tx_cost_eth)
        tx_costs_usd_eth_list.append(tx_cost_eth * ETH_TO_USD)

        tx_cost_matic = gas_used * MATIC_GAS_PRICE
        tx_costs_matic_list.append(tx_cost_matic)
        tx_costs_usd_matic_list.append(tx_cost_matic * MATIC_TO_USD)

        breach_count = agreement_contract.getBreachCount(deployer, accounts[1])
        breach_data = agreement_contract.breachHistory(agreement_contract.createAgreementId(deployer, accounts[1]), breach_count - 1)
        penalty = breach_data[1]
        cumulative_penalty += penalty  

    # Plotting
    fig, axs = plt.subplots(2, 3, figsize=(20, 10))

    # Cumulative Penalty
    axs[0, 0].plot(range(1, 51), penalties, 'o-', color='blue')
    axs[0, 0].set_title("Cumulative Penalty vs. Breach Severity")
    axs[0, 0].set_xlabel("Breach Number")
    axs[0, 0].set_ylabel("Cumulative Penalty")

    # Gas used
    axs[0, 1].plot(range(1, 51), gas_used_list, 'o-', color='red')
    axs[0, 1].set_title("Gas Used per Breach Report")
    axs[0, 1].set_xlabel("Breach Number")
    axs[0, 1].set_ylabel("Gas Used (in units)")

    # Transaction Costs in both ETH and MATIC
    axs[0, 2].plot(range(1, 51), tx_costs_eth_list, 'o-', color='cyan', label='ETH')
    axs[0, 2].plot(range(1, 51), tx_costs_matic_list, 'o-', color='green', label='MATIC')
    axs[0, 2].set_title("Transaction Cost per Breach Report (in ETH & MATIC)")
    axs[0, 2].set_xlabel("Breach Number")
    axs[0, 2].set_ylabel("Transaction Cost")
    axs[0, 2].legend()

    # Transaction Costs in USD (ETH & MATIC)
    axs[1, 0].plot(range(1, 51), tx_costs_usd_eth_list, 'o-', color='purple', label='ETH to USD')
    axs[1, 0].plot(range(1, 51), tx_costs_usd_matic_list, 'o-', color='green', label='MATIC to USD')
    axs[1, 0].set_title("Transaction Cost per Breach Report (in USD)")
    axs[1, 0].set_xlabel("Breach Number")
    axs[1, 0].set_ylabel("Transaction Cost (in USD)")
    axs[1, 0].legend()

    # Latency
    axs[1, 1].plot(range(1, 51), latencies, 'o-', color='orange')
    axs[1, 1].set_title("Latency per Breach Report")
    axs[1, 1].set_xlabel("Breach Number")
    axs[1, 1].set_ylabel("Latency (in seconds)")

    plt.tight_layout()
    plt.savefig('analytics_plot_2.png')
    plt.close()

