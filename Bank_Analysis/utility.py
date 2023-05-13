import numpy as np
import matplotlib as plt
import pandas as pd
import os
from rich import print as rprint

def rwa(credit_risk, market_risk, op_risk):
    """
    Returns the total Risk-weighted assets of the different asset components

    Parameters
    --------
    credit_risk: float
        The risk-weighted value of the credit assets.
    market_risk: float
        The risk-weighted value of the market assets.
    op_risk: float
        The risk-weighted value of the operational assets.
    """
    # Sum up the risk-weighted assets
    return credit_risk + market_risk + op_risk

def cet1(cet1_capital, rwa):
    """
    Calculates the CET1 (Common Equity Tier 1) ratio

    Parameters
    --------
    cet1_capital: float
        The value of the bank's CET1 capital.
    rwa: float
        The value of the bank's Risk-Weighted Assets.
    """
    # Calculate the CET1 ratio, but return infinity if the denominator is zero to avoid division by zero
    if rwa != 0:
        return cet1_capital/rwa
    else:
        return float('inf')

def calc_credit_risk(credit_list):
    """
    Calculates the total credit risk

    Parameters
    --------
    credit_list: list-like object
        A list of credit assets.
    """
    credit_risk = 0
    if is_num(credit_list):
        return credit_list

    # Calculate the total credit risk by summing up the product of the asset value and the risk weight for each credit asset
    for credit_asset in credit_list:
        credit_risk += asset_value(credit_asset) * risk_weight(credit_asset)
    return credit_risk

def calc_market_risk(value_at_risk, s_var):
    """
    Calculates the market risk

    Parameters
    --------
    value_at_risk: float
        The value at risk.
    s_var: float
        The stressed value at risk.
    """
    # Calculate the market risk by taking the maximum of the value at risk and 3 times the stressed value at risk, then multiplying by 12.5
    return np.max(value_at_risk, 3* s_var) * 12.5

def csv_to_dataframe(folder_path):
    """
    Convert all CSV files in a folder to pandas DataFrames and store them in a dictionary

    Parameters
    --------
    folder_path: str
        The path to the folder containing the CSV files.
    """
    # Create an empty dictionary to hold the dataframes
    dataframes = {}

    # Loop over all files in the folder
    for file in os.listdir(folder_path):
        # Check if the file is a CSV file
        if file.endswith('.csv'):
            # Construct the full file path by joining the folder path and the file name
            file_path = os.path.join(folder_path, file)
            # Separate the file name from its extension
            file_name, _ = os.path.splitext(file)
            # Get the name of the folder
            folder_name = os.path.basename(os.path.abspath(folder_path))
            # Construct the dataframe name by combining the folder name, file name and a suffix
            df_name = f"{folder_name}_{file_name}_df"

            try:
                # Try to read the CSV file into a pandas DataFrame
                df = pd.read_csv(file_path, index_col=0)
                # Remove dollar signs and commas from the DataFrame (assuming these are in string format)
                df = df.replace({'\$': '', ',': ''}, regex=True)
                # Fill any missing values with 0
                df.fillna(0, inplace=True)
                # Store the DataFrame in the dictionary using the constructed name as the key
                dataframes[df_name] = df
            except Exception as e:
                # If there was an error reading the file, print an error message
                print(f"Error reading file '{file}': {e}")

    # Return the dictionary of DataFrames
    return dataframes


def is_num(x):
    """
    Checks if a variable is a number (int or float)

    Parameters
    --------
    x: any
    """

    if isinstance(x, int):
        return True
    elif isinstance(x, float):
        return True
    else:
        return False