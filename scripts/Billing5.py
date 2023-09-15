from brownie import Billing, Penalty, accounts, network, Wei
import matplotlib.pyplot as plt
import numpy as np
import csv

def annotate_bars(ax, values):
    for i, value in enumerate(values):
        ax.text(i, value, f"{value:.4f}", ha='center', va='bottom')

def main():
    # Set constants and initialize arrays
    ETH_PRICE = 1853.76
    MATIC_PRICE = 0.68
    GAS_PRICE = Wei("20 gwei")
    functions = ["calculateTotalPenalty", "transferFunds", "requestFunds"]
    
    # Deploy the Penalty contract
    penalty_contract = Penalty.deploy({'from': accounts[0]})
    
    # Deploy the Billing contract
    billing_contract = Billing.deploy(penalty_contract.address, {'from': accounts[0]})
    
    # Lists to hold gas costs for each function
    calculate_penalties = []
    transfer_funds = []
    request_funds = []
    
    for _ in range(50):
        provider = accounts[1]
        consumer = accounts[2]
        amount = 10**18  # 1 ether in wei
        
        # Record the transaction costs
        calculate_penalties.append(billing_contract.calculateTotalPenalty.estimate_gas(provider, {'from': accounts[0]}) * GAS_PRICE)
        transfer_funds.append(billing_contract.transferFunds.estimate_gas(provider, consumer, amount, {'from': accounts[0]}) * GAS_PRICE)
        request_funds.append(billing_contract.requestFunds.estimate_gas(consumer, amount, {'from': accounts[0]}) * GAS_PRICE)

    # Calculate the average costs and populate the lists
    avg_costs_eth = [np.mean(calculate_penalties) / 10**18,
                     np.mean(transfer_funds) / 10**18,
                     np.mean(request_funds) / 10**18]
    avg_costs_usd_eth = [x * ETH_PRICE for x in avg_costs_eth]
    avg_costs_matic = [x * (ETH_PRICE / MATIC_PRICE) for x in avg_costs_eth]
    avg_costs_usd_matic = [x * MATIC_PRICE for x in avg_costs_matic]
    # Save the average costs to a CSV file
    with open('avg_costs_billing.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Function', 'Avg Cost in ETH', 'Avg Cost in USD (ETH)', 'Avg Cost in MATIC', 'Avg Cost in USD (MATIC)'])
        for func, eth, usd_eth, matic, usd_matic in zip(functions, avg_costs_eth, avg_costs_usd_eth, avg_costs_matic, avg_costs_usd_matic):
         csvwriter.writerow([func, eth, usd_eth, matic, usd_matic])
            
            
    #fig, axs = plt.subplots(2, 2, figsize=(16, 8))
    #bar_width = 0.4



    # Plot and add legends for each subplot
    #axs[0, 0].bar(functions, avg_costs_eth, color='blue', width=bar_width)
    #axs[0, 0].set_ylabel("Average Cost")
   # axs[0, 0].legend(['Avg Cost in ETH'], loc='upper right')
    #annotate_bars(axs[0, 0], avg_costs_eth)

    #axs[0, 1].bar(functions, avg_costs_usd_eth, color='green', width=bar_width)
    #axs[0, 1].legend(['Avg Cost in USD (ETH)'], loc='upper right')
    #axs[0, 1].set_ylabel("Average Cost")
    #annotate_bars(axs[0, 1], avg_costs_usd_eth)

    #axs[1, 0].bar(functions, avg_costs_matic, color='red', width=bar_width)
    #axs[1, 0].set_ylabel("Average Cost")
    #axs[1, 0].legend(['Avg Cost in MATIC'], loc='upper right')
    #annotate_bars(axs[1, 0], avg_costs_matic)
 
   # axs[1, 1].bar(functions, avg_costs_usd_matic, color='purple', width=bar_width)
    #axs[1, 1].legend(['Avg Cost in USD (MATIC)'], loc='upper right')
    #axs[1, 1].set_ylabel("Average Cost")
    #annotate_bars(axs[1, 1], avg_costs_usd_matic)

    # Adjust layout
    #plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Save and show plot
    #plt.savefig("combined_costs_updated_billing.png")
    #plt.show()

main()
