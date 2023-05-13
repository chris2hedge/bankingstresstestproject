# *Bank Run Simulation and Risk Calculation Library*

This library contains two Python scripts for performing bank run simulations and various risk calculations related to banking operations.
```bank_run.py```

This script contains the ```BankRun``` class, which is used to simulate a bank run. The class is initialized with the bank's total capital, risk-weighted assets (RWA), initial cash on hand, and the number of simulations to run.

The main method in this class is ```bank_run_sim```, which performs the bank run simulations. In each simulation, a random amount of deposit withdrawals is sampled, and the bank tries to meet this demand either from its available capital or by selling off assets at a discount. The bank's remaining capital and assets, CET1 ratio, and success (whether the CET1 ratio stayed above 8%) are recorded for each simulation.
The results of the simulations are stored in a pandas DataFrame for easy manipulation and analysis.
utility.py
This script provides several functions for calculating various risk measures, as well as some utility functions:

- ```rwa(credit_risk, market_risk, op_risk)```: Returns the total risk-weighted assets, which is the sum of the risk-weighted values of credit, market, and operational assets.

- ```cet1(cet1_capital, rwa)```: Calculates the CET1 (Common Equity Tier 1) ratio, a key measure of a bank's financial strength.

- ```calc_credit_risk(credit_list)```: Calculates the total credit risk from a list of credit assets.

- ```calc_market_risk(value_at_risk, s_var)```: Calculates the market risk based on the value at risk and the stressed value at risk.

- ```csv_to_dataframe(folder_path)```: Converts all CSV files in a folder to pandas DataFrames and stores them in a dictionary. It assumes that the CSV files contain numeric data with possibly dollar signs and commas, which are removed during the conversion. Missing values are filled with zero.

- ```is_num(x)```: Checks if a variable is a number (int or float).

-----------------------

## *Technologies*

- Operating Systems: Mac OS, Windows

- Programming Languages: Python

- Frameworks: Python, JupyterLab, VS code, Streamlit

- Libraries: Pandas, Numpy, Pathlib, Streamlit, Rich
-----------------------

## *Installation*

- Step 1: Install [jupyter lab](https://jupyter.org/install) or [VS code](https://code.visualstudio.com/download) (up to preference)

- Step 2: Install all packages/libraries required for the code to run. Refer to the libraries above and the picture below, repeat until all libraries have been installed.

![Screenshot 2023-05-11 164451](https://github.com/chris2hedge/bankingstresstestproject/assets/127170402/fb5febdc-7433-423f-ac0c-f4b867723f82)

- Step 3: Grab the repository, navigate to your folder of choice (can be a premade or a new folder anywhere on your computer), and clone the repository. Refer to the photos 

![remake](https://github.com/chris2hedge/bankingstresstestproject/assets/127170402/559d1cc5-1046-494a-84ba-99c6ee45e75d)![projectgitclone](https://github.com/chris2hedge/bankingstresstestproject/assets/127170402/8a393390-fbbd-46d5-b748-0e995a4b31d6)
-----------------------

## *Usage*

- Step 1: import the required classes and functions:
 ```
python

from bank_run import BankRun from utility import rwa, cet1, calc_credit_risk, calc_market_risk, csv_to_dataframe, is_num 
```
- Step 2: you can create an instance of BankRun and run simulations:
```
python

br = BankRun(total_capital=1000000, rwa=500000, initial_cash_on_hand=200000, num_iterations=1000) results = br.bank_run_sim() 
```
- The utility functions can also be used separately:
```
python

total_rwa = rwa(credit_risk=200000, market_risk=150000, op_risk=150000) cet1_ratio = cet1(cet1_capital=300000, rwa=total_rwa) 
```
- The csv_to_dataframe function can be used to load data from CSV files:
```
python

dfs = csv_to_dataframe(folder_path='path/to/your/csv/folder')
```
Note: This is a simple usage guide. The actual usage may vary depending on the specific details of the data and the requirements of the analysis.

- After all of this you can also choose to run the code simply through streamlit or Jupyterlab. In order to do so you need to open a terminal and navigate into your project folder
```C:user/desktop/project1```
or wherever you may have your project stored. Once there you need to simply type in ```Jupyter lab``` or ```Streamlit run wells_fargo_bank_run.py```and the website should open perfectly fine. Note:you dont have to open the streamlit with that .py, it can be any of the 4 simulations.

-----------------------

## *Contributors*

- Chris Cummock
- Email: ccummock@gmail.com

- Gregory Krulin
- Email: grgr279@gmail.com

- Mark Beers
- Email: beers.mark@gmail.com

- John Garcia
- Email: Jdganna222@gmail.com

- Samuel Jew
- Email: samjew95@gmail.com

- Eyasu Alemu
- Email: bekaqa01@gmail.com
