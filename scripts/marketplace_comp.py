from brownie import Marketplace, accounts
import random
import string
import matplotlib.pyplot as plt

def random_string(min_length=5, max_length=10):
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def main():
    account = accounts[0]
    marketplace = Marketplace.deploy({'from': account})

    registration_costs = []
    service_addition_costs = []
    service_selection_costs = []

    # Register users and add services
    for i, user in enumerate(accounts[1:51], 1):  # Assuming accounts[0] is deployer
        provider_profile = random_string()
        consumer_profile = random_string()

        tx1 = marketplace.registerUser(provider_profile, consumer_profile, {'from': user})
        registration_costs.append((i, tx1.gas_used))
        
        print(f"{i}. User registered: {user}, gas used: {tx1.gas_used}")

        num_services = random.randint(1, 5)
        for j in range(num_services):
            service_description = random_string()
            tx2 = marketplace.addService(service_description, {'from': user})
            service_addition_costs.append((i, tx2.gas_used))
            print(f"{i}. Service added for user: {user}, gas used: {tx2.gas_used}")

    # Select services
    for i, user in enumerate(accounts[1:51], 1):  # Loop over users
        provider = random.choice(accounts[1:51])
        num_provider_services = marketplace.getServiceCount(provider)
        
        num_selected_services = random.randint(1, num_provider_services)
        for j in range(num_selected_services):
            try:
                service_index = random.randint(0, num_provider_services - 1)
                tx3 = marketplace.selectService(provider, service_index, {'from': user})
                service_selection_costs.append((i, tx3.gas_used))
                print(f"{i}. Service selected by user: {user}, gas used: {tx3.gas_used}")

            except Exception as e:
                print(f"Failed to select service: {e}")

    # Plotting
    plot_combined_data('Combined Costs', registration_costs, service_addition_costs, service_selection_costs)

def plot_combined_data(title, reg_data, add_data, sel_data):
    plt.figure(figsize=(15, 10))

    reg_x, reg_y = zip(*reg_data)
    add_x, add_y = zip(*add_data)
    sel_x, sel_y = zip(*sel_data)

    plt.plot(reg_x, reg_y, color='blue', marker='o', label='Registration Costs')
    plt.plot(add_x, add_y, color='green', marker='x', label='Service Addition Costs')
    plt.plot(sel_x, sel_y, color='red', marker='s', label='Service Selection Costs')

    plt.xlabel('User')
    plt.ylabel('Gas Used')
    plt.title(title)

    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(loc="upper left")

    plt.tight_layout()

    plt.show()