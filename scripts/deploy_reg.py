from brownie import UserRegistry, accounts, network
import matplotlib.pyplot as plt
import time

def main():
    # Check if you're on a local development network
    if network.show_active() not in ['development']:
        print("You are not on the local development network!")
        return

    # Deploying the contract
    account = accounts[0]
    user_registry = UserRegistry.deploy({'from': account})

    registration_gas_used_list = []

    # Register users and measure the gas used
    for user in accounts[1:51]:
        gas_before = user_registry.register.estimate_gas({'from': user})
        tx = user_registry.register({'from': user})
        gas_after = tx.gas_used
        registration_gas_used_list.append(gas_after - gas_before)
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 7))

    # Gas used for Registration plot
    ax.plot(registration_gas_used_list)
    ax.set_title("Gas Used for User Registration & Token Assignment")
    ax.set_xlabel("Transaction")
    ax.set_ylabel("Gas Used")

    plt.tight_layout()
    plt.show()
