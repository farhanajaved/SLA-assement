import brownie
from brownie.network import web3
from brownie.network.transaction import TransactionReceipt
import time
from brownie import Penalty, Billing, accounts
import matplotlib.pyplot as plt

def main():
    domain_counts = list(range(2, 51))
    test_accounts = accounts[0:51]
    
    penalty_contract = Penalty.deploy({"from": test_accounts[0]})
    billing_contract = Billing.deploy(penalty_contract.address, {"from": test_accounts[0]})
    
    functions = [
        {
            "func": billing_contract.calculateTotalPenalty,
            "name": "calculateTotalPenalty",
            "color": "red"
        },
        {
            "func": billing_contract.requestFunds,
            "name": "requestFunds",
            "color": "blue"
        },
        {
            "func": billing_contract.transferFunds,
            "name": "transferFunds",
            "color": "green"
        }
    ]
    
    all_gas_costs = {}
    all_latencies = {}
    all_tps = {}
    
    for function in functions:
        gas_costs = []
        latencies = []
        tps = []
        
        for domain_count in domain_counts:
            for i in range(domain_count):
                penalty_contract.recordBreach(test_accounts[i], {"from": test_accounts[0]})
            
            start_time = time.time()
            
            if function["name"] == "transferFunds":
                provider_balance = web3.eth.getBalance(test_accounts[domain_count - 1].address)
                print(f"Provider balance: {provider_balance}")
                
                serviceCost = 100000
                penalty_amount = billing_contract.calculateTotalPenalty(test_accounts[domain_count - 1], {"from": test_accounts[0]})
                print(f"Calculated Penalty: {penalty_amount}")
                print(f"Service Cost: {serviceCost}")
                
                try:
                    tx = function["func"](test_accounts[domain_count - 1], test_accounts[domain_count - 2], serviceCost, {"from": test_accounts[0]})
                except Exception as e:
                    print(f"Exception caught: {e}")
                    
            elif function["name"] == "requestFunds":
                tx = function["func"](test_accounts[domain_count - 1], 100, {"from": test_accounts[0]})
                
            else:
                tx = function["func"](test_accounts[domain_count - 1], {"from": test_accounts[0]})
            
            end_time = time.time()
            
            if isinstance(tx, TransactionReceipt):
                gas_used = tx.gas_used
            else:
                gas_used = web3.eth.getTransactionReceipt(brownie.network.history[-1].txid)["gasUsed"]
            
            gas_costs.append(gas_used)
            latencies.append(end_time - start_time)
            tps.append(1.0 / (end_time - start_time))
            
        all_gas_costs[function["name"]] = gas_costs
        all_latencies[function["name"]] = latencies
        all_tps[function["name"]] = tps
        
    plot_combined_metrics(domain_counts, all_gas_costs, "Gas Costs per Domain", functions)
    plot_combined_metrics(domain_counts, all_latencies, "Latencies per Domain", functions)
    plot_combined_metrics(domain_counts, all_tps, "TPS per Domain", functions)

def plot_combined_metrics(x, all_metrics, title, functions):
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

if __name__ == "__main__":
    main()
