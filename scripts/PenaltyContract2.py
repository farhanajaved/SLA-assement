from brownie import Penalty, accounts, network, config
import time
import matplotlib.pyplot as plt

def main():
    deployer = accounts[0]  # Using the first Ganache account
    penalty_contract = Penalty.deploy({'from': deployer})

    provider = accounts[1]  # Using the second Ganache account as a sample provider

    gas_costs = []
    timestamps = []
    quadratic_penalties = []
    history_based_penalties = []  # Uncomment if you have a history-based penalty function

    for i in range(100):
        tx = penalty_contract.recordBreach(provider, {'from': deployer})
        gas_costs.append(tx.gas_used)
        timestamps.append(time.time())
        # Instead of using tx.return_value, directly get the latest penalties from the contract
        quadratic_penalties.append(penalty_contract.getQuadraticPenalty(provider, {'from': deployer}))
  # Assuming the recordBreach function returns the calculated penalty
        history_based_penalties.append(penalty_contract.getHistoryBasedPenalty(provider, {'from': deployer}))

    latencies = [timestamps[i] - timestamps[i - 1] for i in range(1, 100)]
    tps = [1 / latency for latency in latencies]
    eth_costs = [(cost * 1845.13) / (10 ** 9) for cost in gas_costs]
    matic_costs = [(cost * 0.62) / (10 ** 9) for cost in gas_costs]

    plt.style.use('seaborn-darkgrid')
    palette = plt.get_cmap('Set1')

    fig, axs = plt.subplots(6, figsize=(10, 20))
    fig.suptitle("Analysis of Penalty Contract", fontsize=20, y=1.03)

    # Graphs from the original script
    axs[0].plot(gas_costs, label="Gas Costs", color=palette(1), marker='o', linestyle='-')
    axs[0].set(ylabel="Gas Used")
    axs[0].legend(loc="upper left")
    axs[0].grid(True)

    axs[1].plot(latencies, label="Latencies", color=palette(2), marker='o', linestyle='-')
    axs[1].set(ylabel="Latency (seconds)")
    axs[1].legend(loc="upper left")
    axs[1].grid(True)

    axs[2].plot(tps, label="TPS", color=palette(3), marker='o', linestyle='-')
    axs[2].set(ylabel="Transactions Per Second")
    axs[2].legend(loc="upper left")
    axs[2].grid(True)

    axs[3].plot(eth_costs, label="ETH Costs (in USD)", color=palette(4), marker='o', linestyle='-')
    axs[3].plot(matic_costs, label="MATIC Costs (in USD)", color=palette(5), marker='o', linestyle='-')
    axs[3].legend(loc="upper left")
    axs[3].set(ylabel="Cost (USD)")
    axs[3].grid(True)

    eth_price = 1845.13
    matic_price = 0.62
    axs[4].bar(["ETH", "MATIC"], [eth_price, matic_price], color=[palette(6), palette(7)])
    axs[4].set_yscale('log')
    axs[4].set(ylabel="Price (USD, Log Scale)", title="ETH vs MATIC Prices")
    axs[4].grid(axis='y')

    # Comparative graph between quadratic and history-based penalties
    axs[5].plot(quadratic_penalties, label="Quadratic Penalties", color='blue', marker='o', linestyle='-')
    axs[5].plot(history_based_penalties, label="History-Based Penalties", color='red', marker='x', linestyle='--')
    axs[5].legend(loc="upper left")
    axs[5].set(ylabel="Penalty Value")
    axs[5].grid(True)


    plt.tight_layout()
    plt.savefig("PenaltyContractAnalysis1.png")
    plt.show()

if __name__ == "__main__":
    main()
