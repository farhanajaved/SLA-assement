from brownie import Marketplace, accounts
import random
import string
import csv

def random_string(length=5):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def random_digit(length=3):
    return ''.join(random.choice(string.digits) for _ in range(length))

def main():
    ETH_PRICE = 1853.76
    MATIC_PRICE = 0.68
    functions = ["calculateTotalPenalty", "transferFunds", "requestFunds"]
    
    # Deploying the contract
    account = accounts[0]
    marketplace = Marketplace.deploy({'from': account})

    # Open a CSV file for writing
    with open('cost_data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write header
        csvwriter.writerow(['Num_Users', 'Action', 'Cost_ETH', 'Cost_USD_ETH', 'Cost_MATIC', 'Cost_USD_MATIC'])

        GAS_PRICE = 20 * 10**9
        last_registered_index = 0

        for num_users in range(2, 51):
            users = accounts[1:num_users+1]
            for i in range(last_registered_index, num_users):
                user = users[i]
                providerProfile = random_string() + random_digit()
                consumerProfile = random_string() + random_digit()
                tx = marketplace.registerUser(providerProfile, consumerProfile, {'from': user})
                cost_eth = (tx.gas_used * GAS_PRICE) / 10**18
                cost_usd_eth = cost_eth * ETH_PRICE
                cost_matic = cost_eth * MATIC_PRICE / ETH_PRICE
                cost_usd_matic = cost_matic * MATIC_PRICE

                csvwriter.writerow([num_users, 'Register User', cost_eth, cost_usd_eth, cost_matic, cost_usd_matic])

            last_registered_index = num_users

            for user in users:
                for _ in range(5):
                    service = random_string() + random_digit()
                    try:
                        tx = marketplace.addService(service, {'from': user})
                    except Exception:
                        break
                    cost_eth = (tx.gas_used * GAS_PRICE) / 10**18
                    cost_usd_eth = cost_eth * ETH_PRICE
                    cost_matic = cost_eth * MATIC_PRICE / ETH_PRICE
                    cost_usd_matic = cost_matic * MATIC_PRICE

                    csvwriter.writerow([num_users, 'Add Service', cost_eth, cost_usd_eth, cost_matic, cost_usd_matic])

            consumer = random.choice(users)
            provider = random.choice(users)
            while provider == consumer:
                provider = random.choice(users)

            serviceIndex = random.randint(0, 4)
            tx = marketplace.selectService(provider, serviceIndex, {'from': consumer})
            cost_eth = (tx.gas_used * GAS_PRICE) / 10**18
            cost_usd_eth = cost_eth * ETH_PRICE
            cost_matic = cost_eth * MATIC_PRICE / ETH_PRICE
            cost_usd_matic = cost_matic * MATIC_PRICE

            csvwriter.writerow([num_users, 'Select Service', cost_eth, cost_usd_eth, cost_matic, cost_usd_matic])
