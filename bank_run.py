import numpy as np
import pandas as pd
import utility


class BankRun:
    """
    
    
    """

    def __init__(self, total_capital, rwa, initial_cash_on_hand, num_iterations = 1000):
        """
        rwa: dict
            rwa will is a dictionary that contains keys credit_risk, market_risk, and operational_risk that have float, list, or dict as values depending on complexity of rwa calculation user wishes to do.
        
        """

        self.total_capital = total_capital
        #self.rwa = rwa
        self.initial_cash = initial_cash_on_hand
        self.num_iterations = num_iterations
        self.credit_risk_assets = rwa#['credit_risk']


    def bank_run_sim(self):
        """
        Need to add the calculation of cet1 below. The function will take intial cash, subtract it from total capital, then have a random chance of how much money will be withdrawn.
        Will then calculate the new cet1 by adding initial capital with remaining capital divded by rwa. This will be calculated with utility code. If the new cet1 is or above 8% then they survived, if below failed.
        Will return how many times succedded, how many failures, and the distrubtion of CET1 after bankrun.

        For simplicity will just subtract needed cash for bank run from rwa as whole. it will need to be more complicated for furture computations.


        Return:
        ----------
        Dataframe with the following paratameters:
            list of success
        
        """

        p_withdrawal = np.array([0.1, 0.2, 0.3, 0.4, 0.5])

        probabilities = np.array([0.2, 0.3, 0.3, 0.1, 0.1])

        discount_rates = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])

        sim_index = []

        withdrawel_list = []

        capital_remaining = []

        risk_assets_remaining = []

        discount_rate_list = []

        cet1_list = []
        
        success = []

        
        
        

        #succes_fail_list = []

        for n in range(self.num_iterations):
            sim_index.append(n)

            credit_risk_assets = self.credit_risk_assets
            capital = self.total_capital

            #if (n%100 == 0):
                #print(f"Attempt number: {n}" )

            # Sample deposit withdrawals based on probabilities
            deposit_withdrawals = np.random.choice(p_withdrawal, p=probabilities) * self.initial_cash

            withdrawel_list.append(deposit_withdrawals)

            # Calculate remaining cash
            #remaining_cash = self.initial_cash - deposit_withdrawals

            #remaining_cash_list = remaining_cash_list.append(remaining_cash)

            if deposit_withdrawals> self.total_capital:

                #cash_needed is how much cash is needed to cover withrdrawels
                cash_needed = (deposit_withdrawals - self.total_capital)

                discount_rate = np.random.choice(discount_rates)
                discount_rate_list.append(discount_rate)

                #since bank will be selling at discount, will need to sell loans whose face value is more than what it will sell for. Since it is being sold at discount_rate, will need to find amount that will equal to cash_needed.
                assests_to_sell = cash_needed/(1-discount_rate)
            
                if assests_to_sell > credit_risk_assets:
                    #bank failure neeed to implement
                    capital_remaining.append(0)

                    risk_assets_remaining.append(credit_risk_assets - assests_to_sell)

                    cet1_list.append(0)
                    success.append(False)

                    break
                    

                #The bank sells of loans, reducing it's total risk_assests
                credit_risk_assets  -= assests_to_sell
                # The bank incurs a loss equal to the discount on the sold loans, which reduces its capital
                capital -= assests_to_sell * discount_rate

            
            else:
                #Bank has enough cash at hand to cover withdrawal and stay within proper capital ratios, however this will cause a hit to their capital.
                capital -= deposit_withdrawals
                discount_rate_list.append(0)

            # Check if bank meets minimum cash reserve requirements

            capital_remaining.append(capital)
            risk_assets_remaining.append(credit_risk_assets)

            cet1 = utility.cet1(capital, credit_risk_assets)

            
           
            cet1_list.append(cet1)

            success.append((cet1*100 >= 8.00))
                

        data = [sim_index, withdrawel_list, capital_remaining, risk_assets_remaining, discount_rate_list, cet1_list, success]
        results = pd.DataFrame(data)#, columns=['simulation_number', 'withdrawal_amt', 'capital', 'credit_risk_assets', 'discount_rate',  'cet1_ratio', 'success'])  
        results = results.transpose()
        results.columns = ['simulation_number', 'withdrawal_amt', 'capital_left', 'credit_risk_assets_left', 'discount_rate',  'cet1_ratio', 'success']
        results = results.set_index('simulation_number')

        return results