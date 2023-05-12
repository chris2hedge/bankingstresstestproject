import numpy as np
import pandas as pd
import utility
import bank_run
import streamlit as st
import time
import datetime


st.markdown(
    """
    <style>
     /* Define font size and color for st.write text */
    body {
        color: grey;
        text-shadow: 2px 2px white;
        font-size: 24 px;
    }
    </style>
    """,
    unsafe_allow_html=True)

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url(https://c0.wallpaperflare.com/preview/968/798/549/5be98a7d18e35.jpg);
background-position: bottom;
background-size: cover;
}

[data-testid="stSidebar"] {
background-image: url(https://coolbackgrounds.io/images/backgrounds/white/white-unsplash-9d0375d2.jpg);
background-size: cover;
background-position: right;
}

[data-testid="stHeader"] {
background-color: rgba(0, 0, 0, 0);
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.sidebar.header("Banks")

#Header
def main():
    st.title("Banking Stress Testing and Capital Reserve Requirements Comparisons")
    st.write("*Mark Beers, Gregory Kulin, Samuel Jew, Eyasu Alemu, John Garcia, and Chris Cummock*", unsafe_allow_html=True)
    st.write('---', unsafe_allow_html=True)
   
if __name__ == '__main__':
    main()
    
#Outline
st.write("In this research project, we will analyze how each banks' capital reserve and loan loss limits would be affected in various economic scenarios and each banks ability to weather the storm, or need to recapitalize.", unsafe_allow_html=True)
st.write("Running **Monte Carlo Simulations** and **Macro economic scenarios** of: interest rate rise, treasury rates rise/fall, large loan losses increase, capital run scenarios and the subsequent capital and reserve capital ratio difficulties of their liquidity vs basel or fed requirements.", unsafe_allow_html=True)

#columns
Banks = ["- First Republic Bank", "- JP Morgan", "- Bank of America", "- Silicon Valley Bank", "- Big Banking Sector ETF"]
stress_tests = ["- Inflation", "- Reserve Capital and Ratios Changes", "- GDP Changes", "- Interest Rates and Mortgage Rates Change", "- Treasury Yields", "- Loan Loss Scenarios"]

col1, col2 = st.columns(2)
with col1:
    st.write("**Comparing capital level & testing different macro economic scenarios of:**", unsafe_allow_html=True)
    for item in Banks:
        st.write(item)

with col2:
    st.write("**Stress Tests on:**", unsafe_allow_html=True)
    for item in stress_tests:
        st.write(item)

st.write('---', unsafe_allow_html=True)



################################ sidebar load graph  ######################################################################

# st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Banking Stress Test Comparisons")
st.sidebar.header("Banking Stress Test Comparisons")
st.write(
    """In this banking stress test project we will use 4 different banks to test and see how or why 1 bank died off and how the others survived. Throughout the course of this project you will see a lot of information from the[Federal Reserve Website](https://www.federalreserve.gov/supervisionreg/dfa-stress-tests-2023.htm) and different Basel reports of our banks. Enjoy!"""
)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    # chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")







################################## Solution #############################################################

wells_fargo_dfs = utility.csv_to_dataframe("WellsFargoCSV")


for a in wells_fargo_dfs.keys():
    print(a)
    # display(wells_fargo_dfs[a])



nsim = 100000
wf_br = bank_run.BankRun(177686*10**6 ,1119518*10**6,555.56*10**9,num_iterations = nsim ) 
#Most numbers are in millions, expect cash_at_hand which is in billions


wf_bank_run_df  = wf_br.bank_run_sim()

################################# Bank run simulation #####################################

st.header('Bank run simulation')
st.dataframe(wf_bank_run_df)

################################# Download Bank run simulation as a csv file #####################################
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


download_data = convert_df(wf_bank_run_df)

st.download_button(
    label="Download data as CSV",
    data=download_data,
    file_name='Bank_run_simulation.csv',
    mime='text/csv',
)

################################# Bank run simulation by using simulation_number, withdrawal_amt, capital, credit_risk_assets, discount_rate, cet1_ratio, success #####################################
st.header('Bank run simulation by using cet1_ratio and discount_rate')
st.pyplot(wf_bank_run_df .plot.scatter(y = ['cet1_ratio'], x = ['discount_rate']).figure)

st.header('Bank run simulation by using cet1_ratio and withdrawal_amt')
st.pyplot(wf_bank_run_df .plot.scatter(y = ['cet1_ratio'], x = ['withdrawal_amt']).figure)

st.header('Bank run simulation by using cet1_ratio and capital')
st.pyplot(wf_bank_run_df .plot.scatter(y = ['cet1_ratio'], x = ['capital']).figure)

st.header('Bank run simulation by using cet1_ratio and credit_asset')
st.pyplot(wf_bank_run_df .plot.scatter(y = ['cet1_ratio'], x = ['credit_risk_assets']).figure)


st.write(wf_bank_run_df ['success'].value_counts())



################################# Download the result #####################################

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

download_data = convert_df(wf_bank_run_df ['success'].value_counts())

st.download_button(
    label="Download data as CSV",
    data=download_data,
    file_name='large_df.csv',
    mime='text/csv',
)







