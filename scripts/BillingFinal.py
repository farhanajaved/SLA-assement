import brownie
from brownie.network import web3
from brownie.network.transaction import TransactionReceipt
import time
from brownie import Penalty, Billing, accounts
import matplotlib.pyplot as plt
from decimal import Decimal

functions = [
    {"name": "calculateTotalPenalty", "color": "blue"},
    {"name": "requestFunds", "color": "red"},
    {"name": "transferFunds", "color": "green"},
]

MATIC_TO_USD = Decimal("0.62")
ETH_TO_USD = Decimal("1845.13")
MATIC_TO_ETH = Decimal("0.62") / Decimal("1845.13")  # Matic value in terms of ETH

def main():
    domain_counts = list(range(2, 51))
    test_accounts = accounts[0:51]

    penalty_contract = Penalty.deploy({"from": test_accounts[0]})
    billing_contract = Billing.deploy(penalty_contract.address, {"from": test_accounts[0]})

    all_gas_costs = {func["name"]: [] for func in functions}
    all_gas_costs_matic = {func["name"]: [] for func in functions}
    all_gas_costs_usd = {func["name"]: [] for func in functions}

    all_latencies = {func["name"]: [] for func in functions}
    all_tps = {func["name"]: [] for func in functions}

    for domain_count in domain_counts:
        for i in range(domain_count):
            penalty_contract.recordBreach(test_accounts[i], {"from": test_accounts[0]})

        for func in functions:
            start_time = time.time()

            if func["name"] == "calculateTotalPenalty":
                tx = getattr(billing_contract, func["name"])(test_accounts[domain_count - 1], {"from": test_accounts[0]})
                
            elif func["name"] == "requestFunds":
                tx = getattr(billing_contract, func["name"])(test_accounts[domain_count - 1], web3.toWei(0.01, 'ether'), {"from": test_accounts[0]})
                
            elif func["name"] == "transferFunds":
                provider_address = test_accounts[domain_count - 1]
                consumer_address = test_accounts[(domain_count) % len(test_accounts)]
                service_cost = web3.toWei(0.02, 'ether')
                tx = getattr(billing_contract, func["name"])(provider_address, consumer_address, service_cost, {"from": test_accounts[0]})

            if isinstance(tx, TransactionReceipt):
                gas_used = tx.gas_used
            else:
                gas_used = web3.eth.getTransactionReceipt(brownie.network.history[-1].txid)["gasUsed"]

            gas_cost_eth = gas_used * web3.eth.gasPrice / 1e18
            gas_cost_matic = gas_cost_eth * MATIC_TO_ETH
            gas_cost_usd_eth = gas_cost_eth * ETH_TO_USD
            gas_cost_usd_matic = gas_cost_matic * MATIC_TO_USD

            all_gas_costs[func["name"]].append(gas_cost_eth)
            all_gas_costs_matic[func["name"]].append(gas_cost_matic)
            all_gas_costs_usd[func["name"]].append((gas_cost_usd_eth, gas_cost_usd_matic))

            end_time = time.time()
            all_latencies[func["name"]].append(end_time - start_time)
            all_tps[func["name"]].append(1.0 / (end_time - start_time))

    plot_combined_metrics(domain_counts, all_gas_costs, "Gas Costs in ETH per Domain")
    plot_combined_metrics(domain_counts, all_gas_costs_matic, "Gas Costs in MATIC per Domain")
    plot_combined_metrics_usd(domain_counts, all_gas_costs_usd, "Gas Costs in USD per Domain")

def plot_combined_metrics(x, all_metrics, title):
    plt.figure()
    for function_name, metrics in all_metrics.items():
        function_info = next(item for item in functions if item["name"] == function_name)
        plt.plot(x, metrics, "o-", label=function_name, color=function_info["color"])

    plt.xlabel("Number of Domains")
    plt.ylabel(title)
    plt.legend()
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{title}.png")
    plt.show()

def plot_combined_metrics_usd(x, all_metrics, title):
    plt.figure()
    for function_name, metrics in all_metrics.items():
        function_info = next(item for item in functions if item["name"] == function_name)
        eth_values, matic_values = zip(*metrics)
        plt.plot(x, eth_values, "o-", label=f"{function_name} (ETH)", color=function_info["color"])
        plt.plot(x, matic_values, "x--", label=f"{function_name} (MATIC)", color=function_info["color"])

    plt.xlabel("Number of Domains")
    plt.ylabel(title)
    plt.legend()
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{title}.png")
    plt.show()

if __name__ == "__main__":
    main()
