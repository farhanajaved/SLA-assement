from brownie import UserRegistry, accounts
import matplotlib.pyplot as plt
import time

def main():
    # Deploying the contract
    account = accounts[0]
    user_registry = UserRegistry.deploy({'from': account})

    gas_used_list = []
    eth_cost_list = []
    latency_list = []

    # Register users and measure the gas used
    for user in accounts[1:51]:  # Assuming you have 50 accounts in Ganache
        start_time = time.time()
        tx = user_registry.register({'from': user})
        end_time = time.time()  # Capture the system time after tx is mined
        latency = end_time - start_time
        
        gas_used_list.append(tx.gas_used)
        eth_cost_list.append(tx.gas_used * tx.gas_price)
        latency_list.append(latency)

    avg_gas_used = sum(gas_used_list) / len(gas_used_list)

    # Plotting
    fig, ax = plt.subplots(3, 1, figsize=(10, 15))

    # Gas used plot
    ax[0].plot(gas_used_list)
    ax[0].set_title("Gas Used for Registration Transactions")
    ax[0].set_xlabel("Transaction")
    ax[0].set_ylabel("Gas Used")

    # ETH cost plot
    ax[1].plot(eth_cost_list)
    ax[1].set_title("ETH Cost for Registration Transactions")
    ax[1].set_xlabel("Transaction")
    ax[1].set_ylabel("ETH Cost")

    # Latency plot
    ax[2].plot(latency_list)
    ax[2].set_title("Latency for Registration Transactions")
    ax[2].set_xlabel("Transaction")
    ax[2].set_ylabel("Latency (Seconds)")

    plt.tight_layout()

    # Save the plot as an image file
    plt.savefig("registration_metrics.png", dpi=300)
    print("Plots saved as registration_metrics.png")

    print(f"Average gas used per registration: {avg_gas_used:.2f}")
