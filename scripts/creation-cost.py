
from brownie import Marketplace, accounts
import random
import string
import time
import matplotlib.pyplot as plt

def random_string(length=5):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def random_digit(length=3):
    return ''.join(random.choice(string.digits) for _ in range(length))

def main():
    # Prices
    ETH_PRICE = 1853.76
    MATIC_PRICE = 0.68
    functions = ["calculateTotalPenalty", "transferFunds", "requestFunds"]
    avg_costs_eth = []
    avg_costs_usd_eth = []
    avg_costs_matic = []
    avg_costs_usd_matic = []


    # Deploying the contract
    account = accounts[0]
    marketplace = Marketplace.deploy({'from': account})

    # Lists to store costs in ETH, MATIC, and USD
    registration_costs_eth = []
    service_addition_costs_eth = []
    service_selection_costs_eth = []

    registration_costs_matic = []
    service_addition_costs_matic = []
    service_selection_costs_matic = []

    # Assuming gas price in wei (for the sake of computation, you might want to update with real gas prices from the network)
    GAS_PRICE = 20 * 10**9

    last_registered_index = 0

    for num_users in range(2, 51):
        users = accounts[1:num_users+1]

        reg_cost_eth, serv_add_cost_eth, serv_sel_cost_eth = [], [], []
        reg_cost_matic, serv_add_cost_matic, serv_sel_cost_matic = [], [], []

        # Register only the newly added users
        for i in range(last_registered_index, num_users):
            user = users[i]
            providerProfile = random_string() + random_digit()
            consumerProfile = random_string() + random_digit()
            tx = marketplace.registerUser(providerProfile, consumerProfile, {'from': user})
            cost_eth = (tx.gas_used * GAS_PRICE) / 10**18
            cost_matic = cost_eth * MATIC_PRICE / ETH_PRICE
            reg_cost_eth.append(cost_eth)
            reg_cost_matic.append(cost_matic)

        last_registered_index = num_users

        # Add services for each user
        for user in users:
            for _ in range(5):
                service = random_string() + random_digit()
                try:
                    tx = marketplace.addService(service, {'from': user})
                    cost_eth = (tx.gas_used * GAS_PRICE) / 10**18
                    cost_matic = cost_eth * MATIC_PRICE / ETH_PRICE
                    serv_add_cost_eth.append(cost_eth)
                    serv_add_cost_matic.append(cost_matic)
                except:
                    break

        # A random user selects a service from another random user
        consumer = random.choice(users)
        provider = random.choice(users)
        while provider == consumer:
            provider = random.choice(users)

        serviceIndex = random.randint(0, 4)
        tx = marketplace.selectService(provider, serviceIndex, {'from': consumer})
        cost_eth = (tx.gas_used * GAS_PRICE) / 10**18
        cost_matic = cost_eth * MATIC_PRICE / ETH_PRICE
        serv_sel_cost_eth.append(cost_eth)
        serv_sel_cost_matic.append(cost_matic)

        # Append average costs in ETH and MATIC
        registration_costs_eth.append(sum(reg_cost_eth) / len(reg_cost_eth))
        service_addition_costs_eth.append(sum(serv_add_cost_eth) / len(serv_add_cost_eth))
        service_selection_costs_eth.append(sum(serv_sel_cost_eth) / len(serv_sel_cost_eth))

        registration_costs_matic.append(sum(reg_cost_matic) / len(reg_cost_matic))
        service_addition_costs_matic.append(sum(serv_add_cost_matic) / len(serv_add_cost_matic))
        service_selection_costs_matic.append(sum(serv_sel_cost_matic) / len(serv_sel_cost_matic))

    # Plotting costs in ETH

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.bar(functions, avg_costs_eth, color='blue')
    ax1.set_title("Average Function Costs in ETH")
    ax1.set_xlabel("Functions")
    ax1.set_ylabel("Cost (ETH)")
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("avg_costs_eth.png")
    plt.show()

    # Plotting costs in USD (Conversion from ETH)
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.bar(functions, avg_costs_usd_eth, color='green')
    ax2.set_title("Average Function Costs in USD (Conversion from ETH)")
    ax2.set_xlabel("Functions")
    ax2.set_ylabel("Cost (USD)")
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("avg_costs_usd_eth.png")
    plt.show()

    # Plotting costs in MATIC
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.bar(functions, avg_costs_matic, color='red')
    ax3.set_title("Average Function Costs in MATIC")
    ax3.set_xlabel("Functions")
    ax3.set_ylabel("Cost (MATIC)")
    ax3.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("avg_costs_matic.png")
    plt.show()

    # Plotting costs in USD (Conversion from MATIC)
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    ax4.bar(functions, avg_costs_usd_matic, color='purple')
    ax4.set_title("Average Function Costs in USD (Conversion from MATIC)")
    ax4.set_xlabel("Functions")
    ax4.set_ylabel("Cost (USD)")
    ax4.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("avg_costs_usd_matic.png")
    plt.show()
