import numpy as np
import matplotlib as plt
import pandas as pd
import os
from rich import print as rprint


def rwa(credit_risk, market_risk, op_risk):
    """
    Returns the total Risk-weighted assets of the different assest components

    Parameters
    --------
    credit_risk: float
        Ipso espo ixi
    market_risk: float
        Ipso espo ixi
    op_risk: float
        Ipso espo ixi
    """
    return credit_risk + market_risk + op_risk


def cet1( cet1_capital, rwa ):
    """
    Parameters
    --------
    cet1_capital: float
        Ipso espo ixi
    rwa: float
        Ipso espo ixi
    """
    if rwa != 0:
        return cet1_capital/rwa
    else:
        return float('inf')


def calc_credit_risk(credit_list):
    """
    Parameters
    --------
    credit_list: data object
        Can be int or a float, or a list with dictionary with being keys of assests with values of a list of assest_value and risk_weight.
    """
    credit_risk = 0
    if is_num(credit_list):
        return credit_list

    #for credit_asset in credit_list:
        #credit_risk += asset_value(credit_asset) * risk_weight(credit_asset)
    return credit_risk

def calc_market_risk(value_at_risk, s_var):
    """
    Parameters
    --------
    value_at_risk: float
        Ipso espo ixi
    s_var: float
        Stressed value at risked
    """
    return np.max(value_at_risk, 3* s_var) * 12.5





def csv_to_dataframe(folder_path):
    dataframes = {}

    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            file_name, _ = os.path.splitext(file)
            folder_name = os.path.basename(os.path.abspath(folder_path))
            df_name = f"{folder_name}_{file_name}_df"

            try:
                df = pd.read_csv(file_path, index_col=0)
                df = df.replace({'\$': '', ',': ''}, regex=True)
                df.fillna(0, inplace=True)
                dataframes[df_name] = df
            except Exception as e:
                print(f"Error reading file '{file}': {e}")

    return dataframes


def is_num(x):
    if isinstance(x, int):
        return True
    elif isinstance(x, float):
        return True
    else:
        return False
    

###def assest_value():
