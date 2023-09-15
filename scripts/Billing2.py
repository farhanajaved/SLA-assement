from brownie import Penalty, accounts
import time
import matplotlib.pyplot as plt

def main():
    # Initialize plotting lists
    x_users = []
    y_latency = []
    y_tps = []

    # Initialize deployer and contract
    deployer = accounts[0]
    penalty = Penalty.deploy({'from': deployer})

    for num_users in range(2, 51):  # Loop from 2 to 50 users
        x_users.append(num_users)

        # Initialize time trackers
        start_time = time.time()
        num_transactions = 0

        # Simulate breaches
        for user in accounts[1:num_users+1]:  # Start from accounts[1] because accounts[0] is deployer
            tx = penalty.recordBreach(user, {'from': deployer})
            num_transactions += 1
            tx.wait(1)  # Wait for 1 confirmation

        # Measure latency and TPS
        end_time = time.time()
        latency = (end_time - start_time) / num_users
        tps = num_users / (end_time - start_time)

        y_latency.append(latency)
        y_tps.append(tps)

        print(f"{num_users} users: Latency = {latency} s, TPS = {tps}")

    # Plotting
    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()
    ax1.plot(x_users, y_latency, 'g-')
    ax2.plot(x_users, y_tps, 'b-')

    ax1.set_xlabel('Number of Users')
    ax1.set_ylabel('Latency (s)', color='g')
    ax2.set_ylabel('TPS', color='b')

    plt.show()
