from brownie import AgreementsContract, accounts
import matplotlib.pyplot as plt
import matplotlib
import random

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

    for i in range(1, 51):
        severity = get_tiered_severity(i)
        
        # Capture the transaction receipt when reporting a breach
        tx_receipt = agreement_contract.reportBreach(accounts[1], severity, {'from': deployer})
        gas_used = tx_receipt.gas_used  # Extract gas used from the transaction receipt
        gas_used_list.append(gas_used)  # Append to our gas_used_list

        breach_count = agreement_contract.getBreachCount(deployer, accounts[1])
        breach_data = agreement_contract.breachHistory(agreement_contract.createAgreementId(deployer, accounts[1]), breach_count - 1)
        penalty = breach_data[1]
        penalties.append(penalty)

    # Plotting the penalty results
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
   
    plt.plot(range(1, 51), penalties, 'o-', color='blue')
    plt.title("Penalty Amount vs. Breach Severity")
    plt.xlabel("Breach Number")
    plt.ylabel("Penalty Amount")

    # Plotting the gas used
    plt.subplot(1, 2, 2)
    plt.plot(range(1, 51), gas_used_list, 'o-', color='red')
    plt.title("Gas Used per Breach Report")
    plt.xlabel("Breach Number")
    plt.ylabel("Gas Used (in units)")

    plt.tight_layout()
    plt.savefig('penalties_and_gas_plot.png')
    plt.close()