from brownie import Marketplace, accounts
import random
import string
import matplotlib.pyplot as plt

ETH_GAS_PRICE = 31  # in Gwei, updated
ETH_PRICE = 1853.76  # in USD

MATIC_GAS_PRICE = 84.1  # in Gwei, updated
MATIC_PRICE = 0.68  # in USD

def random_string(min_length=5, max_length=10):
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def calculate_average_cost(costs):
    return sum(costs) / len(costs)
def annotate_bars(ax, bar_objects):
    for bar in bar_objects:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval, round(yval, 4), ha='center', va='bottom')

def main():
    account = accounts[0]
    marketplace = Marketplace.deploy({'from': account})

    registration_costs = []
    service_addition_costs = []
    service_selection_costs = []

    for i, user in enumerate(accounts[1:51], 1):
        provider_profile = random_string()
        consumer_profile = random_string()

        tx1 = marketplace.registerUser(provider_profile, consumer_profile, {'from': user})
        registration_costs.append(tx1.gas_used)

        num_services = random.randint(1, 5)
        for j in range(num_services):
            service_description = random_string()
            tx2 = marketplace.addService(service_description, {'from': user})
            service_addition_costs.append(tx2.gas_used)

        provider = random.choice(accounts[1:51])
        num_provider_services = marketplace.getServiceCount(provider)

        if num_provider_services > 1:
            num_selected_services = random.randint(1, num_provider_services)
        else:
            num_selected_services = 1

        for j in range(num_selected_services):
            try:
                service_index = random.randint(0, num_provider_services - 1)
                tx3 = marketplace.selectService(provider, service_index, {'from': user})
                service_selection_costs.append(tx3.gas_used)
            except Exception as e:
                print(f"Failed to select service: {e}")

    # Plotting
    labels = ['Registration', 'Service Addition', 'Service Selection']
    avg_costs_eth = [calculate_average_cost(registration_costs) * ETH_GAS_PRICE / 1e9,
                     calculate_average_cost(service_addition_costs) * ETH_GAS_PRICE / 1e9,
                     calculate_average_cost(service_selection_costs) * ETH_GAS_PRICE / 1e9]

    avg_costs_matic = [calculate_average_cost(registration_costs) * MATIC_GAS_PRICE / 1e9,
                       calculate_average_cost(service_addition_costs) * MATIC_GAS_PRICE / 1e9,
                       calculate_average_cost(service_selection_costs) * MATIC_GAS_PRICE / 1e9]

    avg_costs_usd_eth = [x * ETH_PRICE for x in avg_costs_eth]
    avg_costs_usd_matic = [x * MATIC_PRICE for x in avg_costs_matic]

      # Plotting
    fig, axs = plt.subplots(2, 2, figsize=(15, 15))

    bar_width = 0.35
    index = range(len(labels))
    
    colors = ['blue', 'green', 'red', 'purple']

    bar1 = axs[0, 0].bar(index, avg_costs_eth, bar_width, label='Avg Cost in ETH', color=colors[0])
    bar2 = axs[0, 1].bar(index, avg_costs_usd_eth, bar_width, label='Avg Cost in USD (ETH)', color=colors[1])
    bar3 = axs[1, 0].bar(index, avg_costs_matic, bar_width, label='Avg Cost in MATIC', color=colors[2])
    bar4 = axs[1, 1].bar(index, avg_costs_usd_matic, bar_width, label='Avg Cost in USD (MATIC)', color=colors[3])

    for ax in axs.flat:
        ax.set_xlabel('Operations')
        ax.set_ylabel('Average Cost')
        ax.legend()
        #ax.grid(True, linestyle='--', linewidth=0.5)
        ax.set_xticks([p for p in index])
        ax.set_xticklabels(labels)
        
    annotate_bars(axs[0, 0], bar1)
    annotate_bars(axs[0, 1], bar2)
    annotate_bars(axs[1, 0], bar3)
    annotate_bars(axs[1, 1], bar4)

    #axs[0, 0].set_title('Average Cost in ETH')
    #axs[0, 1].set_title('Average Cost in USD (ETH)')
    #axs[1, 0].set_title('Average Cost in MATIC')
    #axs[1, 1].set_title('Average Cost in USD (MATIC)')

    plt.tight_layout()
    plt.show()

main()

