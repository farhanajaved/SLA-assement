from brownie import Marketplace, accounts
import random
import string
import time
import matplotlib.pyplot as plt
import numpy as np

def random_string(length=5):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def random_digit(length=3):
    return ''.join(random.choice(string.digits) for _ in range(length))

def main():
    # Prices
    ETH_PRICE = 1853.76
    MATIC_PRICE = 0.68

    # Deploying the contract
    account = accounts[0]
    marketplace = Marketplace.deploy({'from': account})

    # Lists to store costs in ETH and MATIC
    registration_costs_eth = []
    service_addition_costs_eth = []
    service_selection_costs_eth = []

    registration_costs_matic = []
    service_addition_costs_matic = []
    service_selection_costs_matic = []

    # Assuming gas price in wei
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

         # Append average costs
        registration_costs_eth.append(sum(reg_cost_eth) / len(reg_cost_eth))
        service_addition_costs_eth.append(sum(serv_add_cost_eth) / len(serv_add_cost_eth))
        service_selection_costs_eth.append(sum(serv_sel_cost_eth) / len(serv_sel_cost_eth))

        registration_costs_matic.append(sum(reg_cost_matic) / len(reg_cost_matic))
        service_addition_costs_matic.append(sum(serv_add_cost_matic) / len(serv_add_cost_matic))
        service_selection_costs_matic.append(sum(serv_sel_cost_matic) / len(serv_sel_cost_matic))

    # Dual Y-Axis Bar Chart
    fig, ax1 = plt.subplots(figsize=(15, 7))
    x = list(range(2, 51))

    ax1.set_title("Function Costs in ETH and MATIC")
    ax1.set_xlabel("Number of Users")

    # ETH Bars
    ax1.set_ylabel("Cost (ETH)", color='tab:blue')
    bar_width = 0.35
    x_indices = np.arange(len(x))

    ax1.bar(x_indices - bar_width / 2, registration_costs_eth, bar_width, label="Registration (ETH)", color='blue')
    ax1.bar(x_indices + bar_width / 2, service_addition_costs_eth, bar_width, label="Service Addition (ETH)", color='green')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.legend(loc="upper left")

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    # MATIC Bars
    ax2.set_ylabel("Cost (MATIC)", color='tab:orange')
    ax2.bar(x_indices - bar_width / 2, registration_costs_matic, bar_width, label="Registration (MATIC)", color='orange', alpha=0.6)
    ax2.bar(x_indices + bar_width / 2, service_addition_costs_matic, bar_width, label="Service Addition (MATIC)", color='purple', alpha=0.6)
    ax2.tick_params(axis='y', labelcolor='tab:orange')
    ax2.legend(loc="upper right")

    ax1.set_xticks(x_indices)
    ax1.set_xticklabels(x)

    fig.tight_layout()  # to ensure the right y-label is not slightly clipped
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.savefig("dual_axis_costs_bar_chart.png")
    plt.show()