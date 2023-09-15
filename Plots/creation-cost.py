import matplotlib.pyplot as plt
import csv
from collections import defaultdict

def annotate_bars(ax, values, fmt='.4f'):
    for i, value in enumerate(values):
        if value < 1e-4:
            fmt = '.1e'  # Use scientific notation for very small numbers
        ax.text(i, value, f"{value:{fmt}}", ha='center', va='bottom')

def average(lst):
    return sum(lst) / len(lst)

def plot_from_csv():
    actions = defaultdict(lambda: defaultdict(list))

    # Read data from the CSV file
    with open('../csv/cost_data.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            _, action, cost_eth, cost_usd_eth, cost_matic, cost_usd_matic = row
            actions[action]['cost_eth'].append(float(cost_eth))
            actions[action]['cost_usd_eth'].append(float(cost_usd_eth))
            actions[action]['cost_matic'].append(float(cost_matic))
            actions[action]['cost_usd_matic'].append(float(cost_usd_matic))

    # Calculate average costs
    avg_costs = defaultdict(lambda: defaultdict(float))
    for action, costs in actions.items():
        for cost_type, values in costs.items():
            avg_costs[action][cost_type] = average(values)

    # Academic colors
    eth_color = '#6baed6'
    usd_eth_color = '#fc9272'
    matic_color = '#31a354'
    usd_matic_color = '#756bb1'

    # Plotting
    fig, axs = plt.subplots(2, 2, figsize=(16, 8))
    bar_width = 0.4

    action_names = list(avg_costs.keys())
    eth_values = [avg_costs[action]['cost_eth'] for action in action_names]
    usd_eth_values = [avg_costs[action]['cost_usd_eth'] for action in action_names]
    matic_values = [avg_costs[action]['cost_matic'] for action in action_names]
    usd_matic_values = [avg_costs[action]['cost_usd_matic'] for action in action_names]

    axs[0, 0].bar(action_names, eth_values, color=eth_color, width=bar_width)
    axs[0, 0].set_ylabel("Average Cost")
    axs[0, 0].legend(['Avg Cost in ETH'], loc='upper right')
    annotate_bars(axs[0, 0], eth_values)

    axs[0, 1].bar(action_names, usd_eth_values, color=usd_eth_color, width=bar_width)
    axs[0, 1].set_ylabel("Average Cost")
    axs[0, 1].legend(['Avg Cost in USD (ETH)'], loc='upper right')
    annotate_bars(axs[0, 1], usd_eth_values)

    axs[1, 0].bar(action_names, matic_values, color=matic_color, width=bar_width)
    axs[1, 0].set_ylabel("Average Cost")
    axs[1, 0].legend(['Avg Cost in MATIC'], loc='upper right')
    annotate_bars(axs[1, 0], matic_values)

    axs[1, 1].bar(action_names, usd_matic_values, color=usd_matic_color, width=bar_width)
    axs[1, 1].set_ylabel("Average Cost")
    axs[1, 1].legend(['Avg Cost in USD (MATIC)'], loc='upper right')
    annotate_bars(axs[1, 1], usd_matic_values)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("average_costs_per_action.png")
    plt.show()

if __name__ == "__main__":
    plot_from_csv()
