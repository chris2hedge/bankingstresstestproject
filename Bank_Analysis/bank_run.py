import numpy as np
import pandas as pd
import utility  # Importing utility module, contains code to calculate regulatory cet1 ratio and also code to turn folder of csvs into dataframes. 
class BankRun:
    # This class is intended to simulate a bank run situation

    def __init__(self, total_capital, rwa, initial_cash_on_hand, num_iterations = 1000):
        """
        Parameters:
        total_capital (float): The total initial capital of the bank.
        rwa (float): The total risk weighted assets (RWA) of the bank. 
        initial_cash_on_hand (float): The initial amount of cash the bank has.
        num_iterations (int, optional): The number of iterations for the simulation. Default is 1000.
        """

        self.total_capital = total_capital  # Total initial capital
        self.initial_cash = initial_cash_on_hand  # Initial cash on hand
        self.num_iterations = num_iterations  # Number of iterations for the simulation
        self.credit_risk_assets = rwa  # Risk weighted assets

    def bank_run_sim(self):
        """
        This function simulates a bank run.

        Returns:
        pandas.DataFrame: A DataFrame containing the results of the bank run simulation. The DataFrame includes the following columns: 'simulation_number', 'withdrawal_amt', 'capital_left', 'credit_risk_assets_left', 'discount_rate',  'cet1_ratio', and 'success'.
        """

        # Define possible withdrawal probabilities and their corresponding probabilities
        p_withdrawal = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        probabilities = np.array([0.2, 0.3, 0.3, 0.1, 0.1])

        # Define possible discount rates
        discount_rates = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])

        # Initialize lists to store simulation results
        sim_index = []
        withdrawel_list = []
        capital_remaining = []
        risk_assets_remaining = []
        discount_rate_list = []
        cet1_list = []
        success = []

        for n in range(self.num_iterations):
            sim_index.append(n)

            credit_risk_assets = self.credit_risk_assets
            capital = self.total_capital

            # Sample deposit withdrawals based on probabilities
            deposit_withdrawals = np.random.choice(p_withdrawal, p=probabilities) * self.initial_cash
            withdrawel_list.append(deposit_withdrawals)

            if deposit_withdrawals > self.total_capital:
                # If the withdrawal amount is greater than the total capital calculate how much cash is needed to cover withdrawals
                
                cash_needed = (deposit_withdrawals - self.total_capital)

                # Choose a random discount rate
                discount_rate = np.random.choice(discount_rates)
                discount_rate_list.append(discount_rate)

                # Calculate the amount of assets to sell to cover the cash needed
                assests_to_sell = cash_needed/(1-discount_rate)

                # The bank sells of loans, reducing its total risk assets
                credit_risk_assets  -= assests_to_sell

                # The bank incurs a loss equal to the discount on the sold loans, which reduces its capital
                capital -= assests_to_sell * discount_rate

            else:
                # If the bank has enough cash to cover the withdrawal
                # The withdrawal will cause a reduction in their capital.
                capital -= deposit_withdrawals
                discount_rate_list.append(0)

            # Store remaining capital and risk assets after withdrawal
            capital_remaining.append(capital)
            risk_assets_remaining.append(credit_risk_assets)

            # Calculate cet1 ratio and store it
            cet1 = utility.cet1(capital, credit_risk_assets)
            cet1_list.append(cet1)

            #Store whether the bank was successful (maintained a cet1 ratio above 8%) in the current simulation
            success.append((cet1*100 >= 8.00))

        # Combine all the result lists into a list of lists
        data = [sim_index, withdrawel_list, capital_remaining, risk_assets_remaining, discount_rate_list, cet1_list, success]

        # Convert the data into a pandas DataFrame for easier manipulation and analysis
        results = pd.DataFrame(data)

        # Transpose the DataFrame so that each inner list in 'data' becomes a column instead of a row
        results = results.transpose()

        # Assign column names to the DataFrame
        results.columns = ['simulation_number', 'withdrawal_amt', 'capital', 'credit_risk_assets', 'discount_rate',  'cet1_ratio', 'success']

        # Set the 'simulation_number' column as the index of the DataFrame
        results = results.set_index('simulation_number')

        # Return the resulting DataFrame
        return results