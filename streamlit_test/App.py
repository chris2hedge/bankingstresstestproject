import pandas as pd
import streamlit as st
from pathlib import Path
import pydeck as pdk
import numpy as np
import datetime
import time

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

#Data

####### graph##############
import altair as alt





#page_bg_img = """
#<style>
#[data-testid="stAppViewContainer"]
#background-color: #000000;
#secondaryBackgroundColor="#F0F2F6"
#textColor="#262730"
#font="sans serif"
#</style>
#"""
# primaryColor="#F63366"
# backgroundColor="#FFFFFF"
# secondaryBackgroundColor="#F0F2F6"
# textColor="#262730"
# font="sans serif"

################################################# Date field with Calander selection ###########################


d = st.date_input(
    "Review Date Start From",
    datetime.date(2019,1, 2, ))
st.write('Review date from:', d)

###################################### Table in the form of dataframe ##################################
st.write("Whale_navs top 100")
whale_navs = Path('../Streamlit/whale_navs.csv')
whale_navs = pd.read_csv(whale_navs, index_col='date')
st.dataframe(whale_navs.head(100))

######################################### Download file as a csv file###############################
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(whale_navs.head(100))

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)

###################################### Plot ############################################################
st.write("Daily Return")
daily_return = whale_navs.pct_change().dropna()
daily_return.head(5)

# myplot=daily_return.plot(figsize=(15,7), title="Daily Return", rot=90).figure

df_myplot = st.pyplot(daily_return.plot(figsize=(15,7), title="Daily Return", rot=90).figure)


################################## Data with tabs ##########################################################
st.write("Cumulative Return")
cumulative_return = (1 + daily_return).cumprod() - 1
# st.pyplot(cumulative_return.plot(figsize=(15,7), title="Cumulative Return", rot=90).figure)

tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
tab1_data = st.pyplot(cumulative_return.plot(figsize=(15,7), title="Daily Return", rot=90).figure)
tab2_data = cumulative_return

tab1.subheader("A tab with a chart")
tab1.tab1_data

tab2.subheader("A tab with the data")
tab2.write(tab2_data)


######################################## Slied bar###################################################################
low_volatility, high_volatility = st.select_slider(
    'Select a range of volatility wavelength',
    options=['low', 'medium', 'high' ],
    value=('low', 'high'))
st.write('You selected wavelengths between', low_volatility, 'and', high_volatility)

################################ sidebar load graph  ######################################################################

# st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")


############################################## Sidebar Map ##################################################



# st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

# st.markdown("# Mapping Demo")
# st.sidebar.header("Mapping Demo")
# st.write(
#     """This demo shows how to use
# [`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
# to display geospatial data."""
# )


@st.cache_data
def from_data_file(filename):
    url = (
        "http://raw.githubusercontent.com/streamlit/"
        "example-data/master/hello/v1/%s" % filename
    )
    return pd.read_json(url)


try:
    ALL_LAYERS = {
        "Wells Fargo": pdk.Layer(
            "HexagonLayer",
            data=from_data_file("bike_rental_stats.json"),
            get_position=["lon", "lat"],
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            extruded=True,
        ),
        "JP Morgan": pdk.Layer(
            "ScatterplotLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius="[exits]",
            radius_scale=0.05,
        ),
        "Bank of America": pdk.Layer(
            "TextLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_text="name",
            get_color=[0, 0, 0, 200],
            get_size=15,
            get_alignment_baseline="'bottom'",
        ),
        "Silcon Vally Bank": pdk.Layer(
            "ArcLayer",
            data=from_data_file("bart_path_stats.json"),
            get_source_position=["lon", "lat"],
            get_target_position=["lon2", "lat2"],
            get_source_color=[200, 30, 0, 160],
            get_target_color=[200, 30, 0, 160],
            auto_highlight=True,
            width_scale=0.0001,
            get_width="outbound",
            width_min_pixels=3,
            width_max_pixels=30,
        ),
           "Silcon Vally Bank": pdk.Layer(
            "ArcLayer",
            data=from_data_file("bart_path_stats.json"),
            get_source_position=["lon", "lat"],
            get_target_position=["lon2", "lat2"],
            get_source_color=[200, 30, 0, 160],
            get_target_color=[200, 30, 0, 160],
            auto_highlight=True,
            width_scale=0.0001,
            get_width="outbound",
            width_min_pixels=3,
            width_max_pixels=30,
        ),
    }
    st.sidebar.markdown("### Bank List")
    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)
    ]
    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": 37.76,
                    "longitude": -122.4,
                    "zoom": 11,
                    "pitch": 50,
                },
                layers=selected_layers,
            )
        )
    else:
        st.error("Please choose at least one layer above.")
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )


    ################################## graph ###################################



# st.set_page_config(page_title="DataFrame Demo", page_icon="📊")

st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)


@st.cache_data
def get_UN_data():
    AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")


try:
    df = get_UN_data()
    countries = st.multiselect(
        "Choose countries", list(df.index), ["China", "United States of America"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        data /= 1000000.0
        st.write("### Gross Agricultural Production ($B)", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="year:T",
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )
