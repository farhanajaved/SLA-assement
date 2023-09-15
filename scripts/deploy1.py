from brownie import AgreementsContract, accounts
import matplotlib.pyplot as plt
import matplotlib
import random
import time

matplotlib.use('Agg')

def get_tiered_severity(breach_count):
    base_severity = (breach_count - 1) // 10 + 1
    random_factor = random.uniform(-0.5, 0.5)
    return base_severity + random_factor

def main():
    deployer = accounts[0]
    agreement_contract = AgreementsContract.deploy({'from': deployer})

    print(f"AgreementsContract deployed at: {agreement_contract.address}")
    
    agreement_contract.createAgreement(accounts[1], {'from': deployer})

    penalties = []
    gas_used_list = []  # List to store the gas used for each transaction
    latencies = []  # List to store the latency for each transaction

    for i in range(1, 51):
        severity = get_tiered_severity(i)

        # Record time before transaction
        start_time = time.time()
        
        # Send the transaction
        tx_receipt = agreement_contract.reportBreach(accounts[1], severity, {'from': deployer})
        
        # Record time after receiving the receipt
        end_time = time.time()

        # Calculate and store the latency
        latency = end_time - start_time
        latencies.append(latency)

        gas_used = tx_receipt.gas_used  # Extract gas used from the transaction receipt
        gas_used_list.append(gas_used)  # Append to our gas_used_list

        breach_count = agreement_contract.getBreachCount(deployer, accounts[1])
        breach_data = agreement_contract.breachHistory(agreement_contract.createAgreementId(deployer, accounts[1]), breach_count - 1)
        penalty = breach_data[1]
        penalties.append(penalty)

    # You can now also calculate the average latency
    avg_latency = sum(latencies) / len(latencies)
    print(f"Average Latency: {avg_latency:.2f} seconds")

    # Plotting
    plt.figure(figsize=(18, 6))

    # Penalty results
    plt.subplot(1, 3, 1)
    plt.plot(range(1, 51), penalties, 'o-', color='blue')
    plt.title("Penalty Amount vs. Breach Severity")
    plt.xlabel("Breach Number")
    plt.ylabel("Penalty Amount")

    # Gas used
    plt.subplot(1, 3, 2)
    plt.plot(range(1, 51), gas_used_list, 'o-', color='red')
    plt.title("Gas Used per Breach Report")
    plt.xlabel("Breach Number")
    plt.ylabel("Gas Used (in units)")

    # Latency
    plt.subplot(1, 3, 3)
    plt.plot(range(1, 51), latencies, 'o-', color='green')
    plt.title("Latency per Breach Report")
    plt.xlabel("Breach Number")
    plt.ylabel("Latency (in seconds)")

    plt.tight_layout()
    plt.savefig('penalties_gas_and_latency_plot.png')
    plt.close()
