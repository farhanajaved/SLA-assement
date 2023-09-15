# SLA Assessment

## Description

This project aims to provide a comprehensive framework for Service Level Agreement (SLA) assessment. It employs a hybrid model combining Quadratic and History-Based Penalties to offer a balanced and adaptive response to SLA violations.

## Installation

### Prerequisites

- Python 3.6 or above
- [Brownie](https://github.com/eth-brownie/brownie)
- [Ganache](https://www.trufflesuite.com/ganache)
- [Node.js and npm](https://nodejs.org/en/)

### Installation Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/farhanajaved/SLA-assement.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd SLA-assement
    ```

3. **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install Brownie if you haven't**:
    ```bash
    pip install eth-brownie
    ```

5. **Download and install Ganache**:  
   - You can download it from [here](https://www.trufflesuite.com/ganache).
   - Run Ganache and create a workspace with 55 accounts.

6. **Add a custom network in Brownie if needed**:
    ```bash
    brownie networks add Ethereum ganache-local host=http://localhost:7545 chainid=1337
    ```

7. **Compile contracts**:
    ```bash
    brownie compile
    ```

8. **Run tests to make sure everything is set up correctly**:
    ```bash
    brownie test
    ```

## Usage

1. **Deploy contracts**:
    ```bash
    brownie run deploy --network ganache-local
    ```

2. **Execute specific scripts or interact as needed**.

## Contributing

Contributions are welcome! Please create an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).





Billing 4 has TPS and latencies. 
Billing 5 has costs. 

marketplace_comp for TPS 
marketplace_eth_matic for cost analysis. 


totalpenaltyplots.py is the total breahes 
penaltyplots.py is the num of users
