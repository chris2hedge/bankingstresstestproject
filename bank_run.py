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
        self.rwa = rwa
        self.initial_cash = initial_cash_on_hand
        self.num_iterations = num_iterations
        self.credit_risk_assets = rwa['credit_risk']


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

        remaining_cash_list = []

        cet1_list = []

        discount_rates = []
        
        

        #succes_fail_list = []

        for _ in range(self.num_iterations):
            risk_assests = self.credit_risk_assets
            capital = self.total_capital

            # Sample deposit withdrawals based on probabilities
            deposit_withdrawals = np.random.choice(p_withdrawal, p=probabilities) * self.initial_cash

            # Calculate remaining cash
            remaining_cash = self.initial_cash - deposit_withdrawals

            #remaining_cash_list = remaining_cash_list.append(remaining_cash)

            if deposit_withdrawals> self.total_capital:
                discount_rate = np.random.choice(discount_rates)
                assests_to_sell = (deposit_withdrawals - self.total_capital)/(1-discount_rate)
            
                if assests_to_sell > risk_assests:
                    #bank failure neeed to implement
                    pass

                risk_assests -= assests_to_sell
            
            else:
                capital -= deposit_withdrawals

            # Check if bank meets minimum cash reserve requirements
            cet1 = utility.cet1(capital, risk_assests)


           
            cet1_list = cet1_list.append(cet1)

            if (cet1*100) >= 8.00:
                

        return {"survival_count" :successful_iterations, "faliure_count": (self.num_iterations-successful_iterations), "remaining_cash_list": remaining_cash_list, "cet1_list": cet1_list}