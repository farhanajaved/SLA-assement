import matplotlib.pyplot as plt
import csv
import numpy as np

def annotate_bars(ax, values):
    for i, value in enumerate(values):
        ax.text(i, value, f"{value:.4f}", ha='center', va='bottom')

def plot_from_csv():
    # Initialize lists to hold the CSV data
    functions = []
    avg_costs_eth = []
    avg_costs_usd_eth = []
    avg_costs_matic = []
    avg_costs_usd_matic = []

    # Read data from the CSV file
    with open('../csv/avg_costs_billing.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            functions.append(row[0])
            avg_costs_eth.append(float(row[1]))
            avg_costs_usd_eth.append(float(row[2]))
            avg_costs_matic.append(float(row[3]))
            avg_costs_usd_matic.append(float(row[4]))

    # Plotting
    fig, axs = plt.subplots(2, 2, figsize=(16, 8))
    bar_width = 0.4
    

    # Academic colors
    eth_color = '#6baed6'
    usd_eth_color = '#fc9272'
    matic_color = '#31a354'
    usd_matic_color = '#756bb1'

    

    axs[0, 0].bar(functions, avg_costs_eth, color=eth_color, width=bar_width)
    axs[0, 0].set_ylabel("Average Cost")
    axs[0, 0].legend(['Avg Cost in ETH'], loc='upper right')
    annotate_bars(axs[0, 0], avg_costs_eth)

    axs[0, 1].bar(functions, avg_costs_usd_eth, color=usd_eth_color, width=bar_width)
    axs[0, 1].legend(['Avg Cost in USD (ETH)'], loc='upper right')
    axs[0, 1].set_ylabel("Average Cost")
    annotate_bars(axs[0, 1], avg_costs_usd_eth)

    axs[1, 0].bar(functions, avg_costs_matic, color=matic_color, width=bar_width)
    axs[1, 0].set_ylabel("Average Cost")
    axs[1, 0].legend(['Avg Cost in MATIC'], loc='upper right')
    annotate_bars(axs[1, 0], avg_costs_matic)

    axs[1, 1].bar(functions, avg_costs_usd_matic, color=usd_matic_color, width=bar_width)
    axs[1, 1].legend(['Avg Cost in USD (MATIC)'], loc='upper right')
    axs[1, 1].set_ylabel("Average Cost")
    annotate_bars(axs[1, 1], avg_costs_usd_matic)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("combined_costs_billing_functions.png")
    plt.show()

if __name__ == "__main__":
    plot_from_csv()
